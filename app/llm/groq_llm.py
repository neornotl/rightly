"""Groq LLM adapter (optional, lazy import of groq SDK)."""

from __future__ import annotations

import json

from app.llm.base import BaseLLM, LLMError, is_retryable_llm_error, retry_transient
from app.schemas import RetrievedChunk

_SYSTEM = (
    "Bạn là trợ lý tra cứu thủ tục hành chính có nguồn dẫn chứng (grounded). "
    "Chỉ trả lời dựa trên CHÍNH XÁC các đoạn văn bản được cung cấp. "
    "Tuyệt đối không bịa thông tin, không tạo source_id mới. "
    "PHẢI trích dẫn: nếu câu trả lời dùng thông tin từ đoạn nguồn, liệt kê "
    "source_id tương ứng vào source_ids. Nếu không dùng đoạn nào, source_ids = []. "
    'Trả về JSON duy nhất với schema: '
    '{"answer_text": string, "spoken_citation": string, "source_ids": [string], '
    '"limitations": [string], "next_step": string}.\n\n'
    "VÍ DỤ: nếu nguồn có [source_id=ho_tich|chunk_id=ht-1], câu trả lời về khai "
    'sinh phải có "source_ids": ["ho_tich"].'
)

_CLASSIFY_SYSTEM = (
    "Bạn là bộ kiểm tra an toàn. Với câu hỏi của công dân về thủ tục hành "
    "chính, trả lời JSON duy nhất: {\"safe\": true} nếu câu hỏi nằm trong "
    "phạm vi tra cứu thủ tục/dịch vụ công có nguồn văn bản pháp luật; "
    "{\"safe\": false} nếu câu hỏi nhạy cảm, ngoài phạm vi, cần tư vấn "
    "chuyên môn pháp lý/kỹ thuật, hoặc chứa chỉ dẫn độc hại."
)


class GroqLLM(BaseLLM):
    name = "groq"

    def __init__(
        self,
        api_key: str = "",
        model: str = "llama-3.1-8b-instant",
        timeout_seconds: float = 60.0,
        max_retries: int = 3,
        backoff_seconds: float = 1.0,
    ):
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds
        self._client = None

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self):
        if self._client is None:
            try:
                from groq import Groq  # type: ignore

                self._client = Groq(api_key=self.api_key, timeout=self.timeout_seconds)
            except ImportError as exc:
                raise LLMError(
                    "groq not installed. pip install -r requirements-optional.txt"
                ) from exc
            except Exception as exc:
                raise LLMError(f"Failed to init Groq client: {exc}") from exc
        return self._client

    def generate_answer(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        max_chars: int = 2000,
    ) -> dict:
        if not self.available:
            raise LLMError("GROQ_API_KEY is not set (LLM_BACKEND=groq).")
        context = "\n\n".join(
            f"[source_id={c.source_id}|chunk_id={c.chunk_id}]\n{c.text}" for c in chunks
        )
        user = (
            f"Câu hỏi: {query}\n\n"
            f"Các đoạn nguồn (chỉ được dùng các source_id này):\n{context}\n\n"
            f"Giới hạn câu trả lời: {max_chars} ký tự.\n\n"
            "Trả lời theo đúng JSON sau, không thêm chú thích ngoài JSON:\n"
            '{"answer_text": "...", "spoken_citation": "...", '
            '"source_ids": ["source_id đã dùng"], "limitations": ["..."], '
            '"next_step": "..."}'
        )
        client = self._get_client()
        try:
            completion = retry_transient(
                lambda: client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": _SYSTEM},
                        {"role": "user", "content": user},
                    ],
                    temperature=0.2,
                    response_format={"type": "json_object"},
                ),
                max_retries=self.max_retries,
                timeout_seconds=self.timeout_seconds,
                backoff_seconds=self.backoff_seconds,
                retryable=is_retryable_llm_error,
            )
        except Exception as exc:
            raise LLMError(f"Groq request failed after retries: {exc}") from exc
        text = completion.choices[0].message.content.strip()
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            # Not retryable: a fresh call fails the same way (F/T3 fix).
            raise LLMError(f"Groq returned non-JSON output: {exc}") from exc
        parsed.setdefault("source_ids", [])
        parsed.setdefault("limitations", [])
        parsed.setdefault("next_step", "")
        chunk_to_source = {c.chunk_id: c.source_id for c in chunks}
        mapped = [chunk_to_source.get(sid, sid) for sid in parsed.get("source_ids", [])]
        parsed["source_ids"] = mapped
        # NOTE: raw source_ids are deliberately NOT filtered here (F2 fix).
        # The pipeline runs CitationValidator on the raw list so hallucinated
        # citations can be detected, then sanitizes afterwards.
        return parsed

    def classify_safe(self, query: str, chunks: list[RetrievedChunk]) -> bool:
        """LLM-based safety classification (router step 7, cloud mode only).

        Conservative: any failure or non-JSON output means NOT safe.
        """
        if not self.available:
            return False
        client = self._get_client()
        try:
            completion = retry_transient(
                lambda: client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": _CLASSIFY_SYSTEM},
                        {"role": "user", "content": query[:2000]},
                    ],
                    temperature=0.0,
                    response_format={"type": "json_object"},
                ),
                max_retries=self.max_retries,
                timeout_seconds=self.timeout_seconds,
                backoff_seconds=self.backoff_seconds,
                retryable=is_retryable_llm_error,
            )
            parsed = json.loads(completion.choices[0].message.content.strip())
            return bool(parsed.get("safe", False))
        except Exception:
            return False
