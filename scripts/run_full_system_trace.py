"""P7: Full-system journey traces J1-J7 (redacted).

Runs the 7 canonical journeys end-to-end through the real pipeline
(hybrid retrieval -> safety routing -> LLM -> citation validation -> TTS
mock) and writes redacted traces to
results/full_system_trace_redacted.jsonl

Journeys:
  J1 đăng ký khai sinh (answerable)
  J2 đăng ký kết hôn (answerable)
  J3 đăng ký tạm trú (answerable)
  J4 cấp lại giấy khai sinh (answerable)
  J5 xác nhận tình trạng hôn nhân (answerable)
  J6 thay đổi họ tên trong giấy khai sinh (answerable)
  J7 hồ sơ hộ chiếu (out-of-corpus -> refuse, no LLM call)

Usage:
    python scripts/run_full_system_trace.py [--limit N]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parent.parent

from app.config import load_settings  # noqa: E402
from app.logging_utils import scrub_text  # noqa: E402
from app.pipeline import Pipeline  # noqa: E402

JOURNEYS: list[tuple[str, str, str]] = [
    ("J1", "Tôi cần đăng ký khai sinh cho con, thủ tục như thế nào?", "answerable"),
    ("J2", "Hồ sơ đăng ký kết hôn cần những giấy tờ gì?", "answerable"),
    ("J3", "Đăng ký tạm trú cần bao nhiêu ngày xử lý?", "answerable"),
    ("J4", "Tôi muốn xin cấp lại giấy khai sinh vì bị mất, phí là bao nhiêu?", "answerable"),
    ("J5", "Thủ tục xin giấy xác nhận tình trạng hôn nhân mất bao lâu?", "answerable"),
    ("J6", "Tôi cần thay đổi họ tên trong giấy khai sinh, làm ở đâu?", "answerable"),
    ("J7", "Hồ sơ xin cấp hộ chiếu gồm những gì?", "refuse"),
]


def trace_record(jid: str, expected: str, result, verdict=None) -> dict:
    return {
        "journey": jid,
        "expected": expected,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "query": result.query,
        "decision": result.decision.to_dict(),
        "answer": result.answer.to_dict() if result.answer else None,
        "chunks": [
            {"chunk_id": c.chunk_id, "source_id": c.source_id, "score": c.score}
            for c in result.chunks
        ],
        "citation_verdict": verdict,
        "latencies_ms": result.latencies_ms,
        "tts_output_chars": len(result.tts_output),
    }


def _scrub_record(record: dict) -> dict:
    """Targeted redaction: only free-text fields, keep timestamps intact."""
    record["query"] = scrub_text(record["query"])
    if record.get("answer"):
        record["answer"]["answer_text"] = scrub_text(record["answer"]["answer_text"])
        record["answer"]["spoken_citation"] = scrub_text(record["answer"]["spoken_citation"])
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    settings = load_settings()
    pipeline = Pipeline(settings=settings)
    out_path = ROOT / "results" / "full_system_trace_redacted.jsonl"
    out_path.parent.mkdir(exist_ok=True)

    rows = []
    with out_path.open("w", encoding="utf-8") as fh:
        for jid, q, expected in JOURNEYS:
            if args.limit and len(rows) >= args.limit:
                break
            sid = pipeline.create_session()
            t0 = time.perf_counter()
            result = pipeline.process_text(sid, q)
            elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 1)
            pipeline.delete_session(sid)

            verdict = None
            if result.answer is not None and pipeline.validator is not None:
                verdict = pipeline.validator.validate(
                    result.answer, {c.source_id for c in result.chunks}
                ).to_dict()

            record = trace_record(jid, expected, result, verdict)
            record["latencies_ms"]["total_ms"] = elapsed_ms
            safe = _scrub_record(record)
            fh.write(json.dumps(safe, ensure_ascii=False, default=str) + "\n")
            rows.append((jid, expected, result))
            print(
                f"{jid} {result.decision.zone.value:7s} {result.decision.action.value:7s} "
                f"{elapsed_ms:6.0f}ms chunks={len(result.chunks)} "
                f"ok={record['citation_verdict']['ok'] if record['citation_verdict'] else 'n/a'}"
            )

    ok_count = sum(
        1
        for _, exp, r in rows
        if (exp == "answerable" and r.decision.action.value == "ANSWER")
        or (exp == "refuse" and r.decision.action.value == "REFUSE")
    )
    print(f"\n{len(rows)} journeys, {ok_count} behave as expected")
    print(f"Saved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
