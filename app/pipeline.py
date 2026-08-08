"""End-to-end pipeline: ASR -> normalize -> retrieval -> router -> LLM -> TTS.

Privacy guarantees implemented here:
- Raw audio is deleted after the session when
  DELETE_RAW_AUDIO_AFTER_SESSION=true (only for files under DATA_DIR; we never
  delete user-provided files outside the project).
- Transcripts are not logged unless SAVE_TRANSCRIPTS=true.
- Only the transcript + needed chunks go to the LLM (never raw audio).
- In cloud mode (gemini/groq), the outbound query is PII-scrubbed first
  (PII_SCRUB_OUTBOUND=true); local rules, routing, and logging keep the
  original text.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from app.asr.base import BaseASR
from app.asr.mock_asr import MockASR
from app.config import Settings
from app.dialogue.state_machine import State
from app.llm.base import BaseLLM
from app.llm.mock_llm import MockLLM
from app.logging_utils import JsonlLogger, SessionStore, utc_now_iso
from app.retrieval.base import Retriever
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.document_loader import DocumentLoader
from app.safety.policy import Policy
from app.safety.router import SafetyRouter
from app.safety.rules import normalize_query
from app.schemas import GroundedAnswer, PipelineResult, UserQuery
from app.tts.base import BaseTTS
from app.tts.mock_tts import MockTTS

_MIN_QUERY_CHARS = 3


def make_asr(settings: Settings) -> BaseASR:
    if settings.asr_backend == "phowhisper":
        from app.asr.phowhisper_asr import PhoWhisperASR

        return PhoWhisperASR()
    return MockASR()


def make_retriever(settings: Settings) -> Retriever:
    chunks_file = settings.chunks_dir / "demo_chunks.jsonl"
    if settings.retrieval_backend == "hybrid":
        real_file = settings.chunks_dir / "real_chunks.jsonl"
        if real_file.exists():
            chunks_file = real_file
            cache_path = settings.chunks_dir / "real_embeddings.npz"
            exclude_demo = settings.app_mode != "mock"
        else:
            # F5 fix: demo fallback must not silently empty out. When a real
            # corpus is required (non-mock), fail loudly; in mock mode use
            # the demo chunks with their OWN cache and no demo filtering.
            if settings.app_mode != "mock":
                raise RuntimeError(
                    "RETRIEVAL_BACKEND=hybrid requires data/chunks/real_chunks.jsonl "
                    "(run scripts/crawl_vbpl.py + scripts/ocr_vbpl.py first)."
                )
            chunks_file = settings.chunks_dir / "demo_chunks.jsonl"
            cache_path = settings.chunks_dir / "demo_embeddings.npz"
            exclude_demo = False
        from app.retrieval.hybrid_retriever import HybridRetriever

        return HybridRetriever.from_chunks(
            DocumentLoader.load_chunks(chunks_file),
            cache_path=cache_path,
            exclude_demo=exclude_demo,
            rerank=settings.retriever_rerank,
            gate=settings.retriever_gate,
            bm25_gate=settings.bm25_gate,
            dense_gate=settings.dense_gate,
        )
    if settings.retrieval_backend != "bm25":
        raise ValueError(f"Unsupported retrieval backend: {settings.retrieval_backend}")
    return BM25Retriever.from_jsonl(chunks_file)


def make_llm(settings: Settings) -> BaseLLM:
    if settings.llm_backend == "gemini":
        from app.llm.gemini_llm import GeminiLLM

        llm: BaseLLM = GeminiLLM(api_key=settings.gemini_api_key)
        if not llm.available:  # type: ignore[attr-defined]
            raise RuntimeError("LLM_BACKEND=gemini but GEMINI_API_KEY is not set.")
        return llm
    if settings.llm_backend == "groq":
        from app.llm.groq_llm import GroqLLM

        llm = GroqLLM(api_key=settings.groq_api_key)
        if not llm.available:  # type: ignore[attr-defined]
            raise RuntimeError("LLM_BACKEND=groq but GROQ_API_KEY is not set.")
        return llm
    return MockLLM()


def make_tts(settings: Settings) -> BaseTTS:
    if settings.tts_backend == "edge":
        from app.tts.edge_tts import EdgeTTS

        return EdgeTTS(voice=settings.edge_tts_voice, rate=settings.edge_tts_rate)
    return MockTTS()


@dataclass
class Pipeline:
    settings: Settings = field(default_factory=Settings)
    asr: Optional[BaseASR] = None
    retriever: Optional[Retriever] = None
    llm: Optional[BaseLLM] = None
    tts: Optional[BaseTTS] = None
    router: Optional[SafetyRouter] = None
    store: Optional[SessionStore] = None
    logger: Optional[JsonlLogger] = None
    validator: object = None  # CitationValidator when app_mode != "mock"
    top_k: int = 5

    def __post_init__(self) -> None:
        self.settings.resolved_log_dir().mkdir(parents=True, exist_ok=True)
        if self.logger is None:
            self.logger = JsonlLogger(self.settings.resolved_log_dir())
        if self.store is None:
            self.store = SessionStore(self.settings.resolved_log_dir(), self.logger)
        if self.asr is None:
            self.asr = make_asr(self.settings)
        if self.retriever is None:
            self.retriever = make_retriever(self.settings)
        if self.llm is None:
            self.llm = make_llm(self.settings)
        if self.tts is None:
            self.tts = make_tts(self.settings)
        if self.router is None:
            self.router = SafetyRouter(settings=self.settings, policy=Policy())
        if self.validator is None and self.settings.app_mode != "mock":
            from app.validation.citation_validator import CitationValidator

            self.validator = CitationValidator(
                status_path=self.settings.resolved_data_dir() / "law_status.json"
            )

    # ---------- lifecycle ----------

    def create_session(self) -> str:
        session_id = self.store.create()
        self.store.record(
            session_id,
            "config_summary",
            app_mode=self.settings.app_mode,
            asr_backend=self.asr.name,
            llm_backend=self.llm.name,
            tts_backend=self.tts.name,
            retrieval_backend=self.retriever.name,
        )
        return session_id

    def delete_session(self, session_id: str) -> int:
        return self.store.delete_session(session_id)

    # ---------- core ----------

    def process_text(self, session_id: str, text: str) -> PipelineResult:
        """Full pipeline for a text query (no audio involved)."""
        if self.settings.save_transcripts:
            self.store.record(session_id, "transcript_saved", transcript=text)
        query = UserQuery(text=text, session_id=session_id, timestamp=utc_now_iso())
        return self._run(session_id, query)

    def process_audio(self, session_id: str, audio_path: str | Path) -> PipelineResult:
        """Full pipeline for an audio query (ASR first, audio privacy rules)."""
        audio = Path(audio_path)
        try:
            start = time.perf_counter()
            asr_result = self.asr.transcribe(audio)
            asr_ms = (time.perf_counter() - start) * 1000.0
            if self.settings.save_transcripts:
                self.store.record(session_id, "transcript_saved", transcript=asr_result.transcript)
            query = UserQuery(
                text=asr_result.transcript,
                session_id=session_id,
                timestamp=utc_now_iso(),
                audio_path=str(audio),
            )
            return self._run(session_id, query, precomputed_asr_ms=asr_ms)
        finally:
            # F13 fix: raw audio is deleted even when ASR or the pipeline
            # raises, so privacy deletion cannot be skipped by failures.
            self._apply_audio_privacy(audio)

    def _apply_audio_privacy(self, audio: Path) -> None:
        """Delete raw audio only when it lives inside the project data dir."""
        if not self.settings.delete_raw_audio_after_session:
            return
        data_dir = self.settings.resolved_data_dir()
        try:
            in_data = audio.resolve().is_relative_to(data_dir.resolve())
        except (OSError, ValueError):
            in_data = False
        if in_data:
            try:
                audio.unlink(missing_ok=True)
            except OSError:
                pass

    def _run(
        self,
        session_id: str,
        query: UserQuery,
        precomputed_asr_ms: float = 0.0,
    ) -> PipelineResult:
        lat: dict[str, float] = {}
        if precomputed_asr_ms:
            lat["asr_ms"] = round(precomputed_asr_ms, 1)

        t0 = time.perf_counter()
        normalized = normalize_query(query.text)
        lat["normalize_ms"] = round((time.perf_counter() - t0) * 1000.0, 1)

        t0 = time.perf_counter()
        chunks = self.retriever.search(query.text, top_k=self.top_k)
        lat["retrieval_ms"] = round((time.perf_counter() - t0) * 1000.0, 1)

        t0 = time.perf_counter()
        llm_classifier = None
        if self.settings.app_mode == "cloud" and hasattr(self.llm, "classify_safe"):
            # Outbound: scrub the query before it leaves the machine.
            if self.settings.pii_scrub_outbound:
                from app.privacy.scrubber import scrub_outbound

                def _scrubbed_classifier(q: str, ch: object) -> bool:
                    return self.llm.classify_safe(  # type: ignore[attr-defined]
                        scrub_outbound(q), ch  # type: ignore[arg-type]
                    )

                llm_classifier = _scrubbed_classifier
            else:
                llm_classifier = self.llm.classify_safe  # type: ignore[attr-defined]
        decision, normalized = self.router.route(query.text, chunks, llm_classifier)
        lat["safety_ms"] = round((time.perf_counter() - t0) * 1000.0, 1)

        answer: Optional[GroundedAnswer] = None
        if self.router.would_answer(decision):
            t0 = time.perf_counter()
            try:
                outbound_text = query.text
                if (
                    self.settings.llm_backend in {"gemini", "groq"}
                    and self.settings.pii_scrub_outbound
                ):
                    from app.privacy.scrubber import scrub_outbound

                    outbound_text = scrub_outbound(query.text)
                doc = self.llm.generate_answer(
                    outbound_text,
                    chunks[:3],
                    max_chars=self.settings.max_response_chars,
                )
                raw_ids = [str(s) for s in (doc.get("source_ids") or [])]
                answer = GroundedAnswer(
                    answer_text=str(doc.get("answer_text", "")).strip(),
                    spoken_citation=str(doc.get("spoken_citation", "")).strip(),
                    source_ids=raw_ids,
                    limitations=[str(s) for s in (doc.get("limitations") or [])],
                    next_step=str(doc.get("next_step", "")).strip(),
                )
            except Exception as exc:
                decision = self.router.policy.insufficient_decision()
                self.store.record(session_id, "llm_failure", reason=str(exc)[:500])
            lat["llm_ms"] = round((time.perf_counter() - t0) * 1000.0, 1)

            if answer is not None and not raw_ids:
                # Council T2: an answer with content but zero citations is
                # ungrounded — refuse instead of reading it out.
                decision = self.router.policy.insufficient_decision()
                self.store.record(
                    session_id,
                    "citation_rejected",
                    issues=[{"kind": "no_citation",
                             "message": "Câu trả lời không trích dẫn nguồn nào."}],
                )
                answer = None

            if answer is not None and self.validator is not None:
                # Validate RAW citations first (F2 fix): filtering before
                # validation would silently hide hallucinated source_ids.
                retrieved = {c.source_id for c in chunks}
                verdict = self.validator.validate(answer, retrieved)
                if not verdict.ok:
                    outdated = any(i.kind == "outdated" for i in verdict.issues)
                    decision = self.router.policy.citation_decision(
                        outdated=outdated
                    )
                    self.store.record(
                        session_id,
                        "citation_rejected",
                        issues=[vars(i) for i in verdict.issues],
                    )
                    answer = None
                else:
                    # Sanitize AFTER validation: keep only retrieved sources.
                    kept = [sid for sid in raw_ids if sid in retrieved]
                    answer = GroundedAnswer(
                        answer_text=answer.answer_text,
                        spoken_citation=answer.spoken_citation,
                        source_ids=kept,
                        limitations=answer.limitations,
                        next_step=answer.next_step,
                    )

        spoken = ""
        if answer is not None:
            spoken = self.tts.speak_result(result_for_tts(query, decision, answer))
            t0 = time.perf_counter()
            try:
                self.tts.synthesize(spoken, self._tts_output_path(session_id))
            except Exception as exc:
                self.store.record(session_id, "tts_failure", reason=str(exc)[:300])
            lat["tts_ms"] = round((time.perf_counter() - t0) * 1000.0, 1)

        result = PipelineResult(
            session_id=session_id,
            query=query.text,
            normalized_query=normalized,
            decision=decision,
            answer=answer,
            chunks=chunks,
            latencies_ms=lat,
            app_mode=self.settings.app_mode,
            tts_output=spoken,
        )
        self._log_result(result)
        return result

    def _tts_output_path(self, session_id: str) -> Path:
        return self.settings.resolved_results_dir() / f"{session_id}.wav"

    def _log_result(self, result: PipelineResult) -> None:
        payload = {
            "event": "pipeline_result",
            "decision_zone": result.decision.zone.value,
            "decision_action": result.decision.action.value,
            "reason_codes": list(result.decision.reason_codes),
            "source_ids": [c.source_id for c in result.chunks],
            "latencies_ms": result.latencies_ms,
            "app_mode": result.app_mode,
        }
        if self.settings.save_transcripts:
            payload["transcript"] = result.query
        self.store.record(result.session_id, **payload)

    def hold_state(self) -> State:
        """Return HOLDING; used by CLI/UI before speaking."""
        return State.HOLDING


def result_for_tts(
    query: str, decision: object, answer: Optional[GroundedAnswer]
) -> PipelineResult:
    """Build a minimal PipelineResult for TTS text generation."""
    return PipelineResult(
        session_id="",
        query=query,
        normalized_query="",
        decision=decision,  # type: ignore[arg-type]
        answer=answer,
        chunks=[],
        latencies_ms={},
        app_mode="",
        tts_output="",
    )
