"""End-to-end mock demo: text query through the full pipeline.

Usage:
    python scripts/run_mock_demo.py [--query "..."]

SYNTHETIC DEMO - NOT PILOT RESULTS
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows cp1252 console workaround
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import load_settings
from app.pipeline import Pipeline

DEFAULT_QUERY = "Thủ tục cấp giấy xác nhận hộ khẩu tại xã Bình Minh?"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run mock end-to-end demo")
    parser.add_argument("--query", type=str, default=DEFAULT_QUERY)
    args = parser.parse_args()

    settings = load_settings()
    if settings.app_mode != "mock":
        print(
            f"[WARN] running with APP_MODE={settings.app_mode}; demo is designed for mock",
            file=sys.stderr,
        )
    pipeline = Pipeline(settings=settings)
    session_id = pipeline.create_session()
    try:
        result = pipeline.process_text(session_id, args.query)
    finally:
        pipeline.delete_session(session_id)

    print("=" * 60)
    print("SYNTHETIC DEMO - NOT PILOT RESULTS")
    print("=" * 60)
    print(f"Query : {result.query}")
    print(f"Zone  : {result.decision.zone.value} ({result.decision.action.value})")
    print(f"Reasons: {', '.join(result.decision.reason_codes)}")
    if result.answer:
        print(f"\nAnswer:\n{result.answer.answer_text}")
        print(f"\nCitation: {result.answer.spoken_citation}")
    else:
        print(f"\nGuidance: {result.decision.user_message}")
    print(f"\nLatency: {result.latencies_ms}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
