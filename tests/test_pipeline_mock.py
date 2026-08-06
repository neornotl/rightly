"""End-to-end mock pipeline tests: text, audio privacy, logging, deletion."""

from __future__ import annotations

import json

from app.config import Settings
from app.pipeline import Pipeline
from app.schemas import Action, Zone


def _pipeline(tmp_path, **overrides) -> Pipeline:
    settings = Settings(
        data_dir=tmp_path / "data",
        results_dir=tmp_path / "results",
        log_dir=tmp_path / "logs",
        **overrides,
    )
    settings.chunks_dir.mkdir(parents=True, exist_ok=True)
    settings.resolved_log_dir().mkdir(parents=True, exist_ok=True)
    from app.retrieval.document_loader import DocumentLoader

    records = DocumentLoader(sources_dir="data/sources", chunks_dir=settings.chunks_dir).ingest()
    out = settings.chunks_dir / "demo_chunks.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec.__dict__, ensure_ascii=False) + "\n")
    return Pipeline(settings=settings)


def test_mock_pipeline_end_to_end(tmp_path):
    pipeline = _pipeline(tmp_path)
    session_id = pipeline.create_session()
    result = pipeline.process_text(
        session_id, "Thủ tục cấp giấy xác nhận hộ khẩu tại xã Bình Minh?"
    )
    assert result.decision.zone == Zone.YELLOW
    assert result.decision.action == Action.ANSWER
    assert result.answer is not None
    assert result.answer.source_ids == ["demo_binhminh_procedures"]
    assert "DEMO" in result.answer.limitations[0]
    assert result.latencies_ms.get("retrieval_ms", 0) >= 0
    assert result.tts_output
    pipeline.delete_session(session_id)


def test_pipeline_safe_query_cites_demo_only(tmp_path):
    pipeline = _pipeline(tmp_path)
    session_id = pipeline.create_session()
    result = pipeline.process_text(session_id, "Đăng ký khai sinh cần giấy gì?")
    assert set(result.answer.source_ids) == {"demo_binhminh_procedures"}


def test_pipeline_refuses_when_no_source(tmp_path):
    pipeline = _pipeline(tmp_path)
    session_id = pipeline.create_session()
    result = pipeline.process_text(session_id, "Tổng thống Mỹ tên là gì?")
    assert result.decision.action == Action.REFUSE
    assert result.answer is None


def test_pipeline_emergency_never_generates_answer(tmp_path):
    pipeline = _pipeline(tmp_path)
    session_id = pipeline.create_session()
    result = pipeline.process_text(session_id, "Tôi bị đau tim, cấp cứu giúp!")
    assert result.decision.zone == Zone.RED
    assert result.answer is None
    assert "khẩn cấp" in result.decision.user_message


def test_transcripts_not_saved_by_default(tmp_path):
    pipeline = _pipeline(tmp_path)
    session_id = pipeline.create_session()
    pipeline.process_text(session_id, "Thủ tục cấp hộ khẩu?")
    records = pipeline.store.logger.read_records()
    texts = json.dumps(records, ensure_ascii=False)
    assert "Thủ tục cấp hộ khẩu" not in texts


def test_transcripts_saved_when_enabled(tmp_path):
    pipeline = _pipeline(tmp_path, save_transcripts=True)
    session_id = pipeline.create_session()
    pipeline.process_text(session_id, "Thủ tục cấp hộ khẩu?")
    records = pipeline.store.logger.read_records()
    texts = json.dumps(records, ensure_ascii=False)
    assert "Thủ tục cấp hộ khẩu" in texts


def test_delete_session_removes_lines(tmp_path):
    pipeline = _pipeline(tmp_path)
    session_id = pipeline.create_session()
    pipeline.process_text(session_id, "Thủ tục cấp hộ khẩu?")
    before = len(pipeline.store.logger.read_records())
    removed = pipeline.delete_session(session_id)
    assert removed > 0
    after = pipeline.store.logger.read_records()
    assert len(after) < before
    assert all(r.get("session_id") != session_id for r in after)


def test_raw_audio_deleted_after_session_when_in_data_dir(tmp_path):
    pipeline = _pipeline(tmp_path)
    audio = pipeline.settings.resolved_data_dir() / "audio" / "sample.wav"
    audio.parent.mkdir(parents=True, exist_ok=True)
    audio.write_bytes(b"RIFF fake wav")
    session_id = pipeline.create_session()
    # MockASR reads sibling .txt; create transcript sidecar.
    (audio.with_suffix(".wav.txt")).write_text("Thủ tục cấp hộ khẩu?", encoding="utf-8")
    result = pipeline.process_audio(session_id, audio)
    assert not audio.exists(), "raw audio must be deleted after session"
    assert result.answer is not None


def test_audio_kept_when_outside_data_dir(tmp_path):
    pipeline = _pipeline(tmp_path)
    outside = tmp_path / "user_audio.wav"
    outside.write_bytes(b"RIFF fake wav")
    (tmp_path / "user_audio.wav.txt").write_text("Thủ tục cấp hộ khẩu?", encoding="utf-8")
    session_id = pipeline.create_session()
    pipeline.process_audio(session_id, outside)
    assert outside.exists(), "user files outside data dir must never be deleted"


def test_logs_do_not_contain_api_key(tmp_path):
    pipeline = _pipeline(tmp_path, gemini_api_key="FAKE_GEMINI_KEY_FOR_LOGGING_TEST")
    session_id = pipeline.create_session()
    pipeline.process_text(session_id, "Thủ tục cấp hộ khẩu?")
    logs = (pipeline.store.logger.path).read_text(encoding="utf-8")
    assert "FAKE_GEMINI_KEY_FOR_LOGGING_TEST" not in logs
