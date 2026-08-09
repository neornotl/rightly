"""Log pilot metrics (WER/MOS/CSAT) — P uses during real pilots (13/08, 18/08).

Usage:
    python scripts/log_pilot_metrics.py --audio <wav> --ref "câu đúng cần nói" \
        --task-id ho-khau --accent bac
Then answer interactive prompts: task success (co/khong) + CSAT 1-5.

Appends one record per run to data/eval/pilot_metrics.jsonl. Records are
anonymous (no names); raw audio stays on the pilot device (not uploaded).
Aggregation for Technical Rigor (14/08): median WER, task success rate, CSAT.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parent.parent.as_posix())

from eval.wer import evaluate_wer  # noqa: E402

METRICS_FILE = Path("data") / "eval" / "pilot_metrics.jsonl"


def _ask(prompt: str, choices: dict[str, str], default: str = "") -> str:
    label = "/".join(f"{k}={v}" for k, v in choices.items())
    while True:
        raw = (
            input(f"{prompt} [{label}]{' [default: ' + default + ']' if default else ''}: ")
            .strip()
            .lower()
        )
        if not raw and default:
            return default
        if raw in choices:
            return raw
        print(f"  -> chấp nhận: {', '.join(choices)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Pilot WER/CSAT logging (anonymous)")
    ap.add_argument("--audio", required=True, help="Path to pilot audio (wav)")
    ap.add_argument("--ref", required=True, help="Reference transcript the user should say")
    ap.add_argument("--task-id", required=True, help="Pilot task id (e.g. ho-khau)")
    ap.add_argument("--accent", default="", help="accent_group: bac/trung/nam (optional)")
    args = ap.parse_args()

    audio = Path(args.audio)
    if not audio.exists():
        print(f"ERROR: audio not found: {audio}")
        return 2

    from app.asr.phowhisper_asr import PhoWhisperASR

    print("Transcribing...")
    t0 = time.perf_counter()
    result = PhoWhisperASR().transcribe(audio)
    latency_ms = round((time.perf_counter() - t0) * 1000.0, 1)

    transcript = result.transcript.strip()
    print(f"ASR: {transcript!r}")
    print(f"REF: {args.ref!r}")

    (wer, subs, ins, dels), stats = evaluate_wer(
        [{"reference": args.ref, "hypothesis": transcript}]
    )
    print(f"WER = {wer * 100:.1f}%  (sub={subs} ins={ins} del={dels}, latency={latency_ms}ms)")

    success = _ask("Task hoàn thành đúng?", {"co": "yes", "khong": "no"})
    csat = _ask(
        "Độ hài lòng người dùng 1-5?",
        {"1": "rất tệ", "2": "tệ", "3": "tạm", "4": "tốt", "5": "rất tốt"},
    )
    comment = input("Ghi chú (tùy chọn, không ghi tên người): ").strip()

    record = {
        "task_id": args.task_id,
        "accent_group": args.accent,
        "transcript": transcript,
        "reference": args.ref,
        "wer": round(wer, 4),
        "latency_ms": latency_ms,
        "task_success": success == "co",
        "csat": int(csat),
        "mos_subjective": int(csat),
        "comment": comment[:500],
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with METRICS_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Saved -> {METRICS_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
