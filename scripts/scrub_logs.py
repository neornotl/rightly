"""Scrub sensitive patterns from log files (heuristic).

Usage:
    python scripts/scrub_logs.py [--logs logs/session.log.jsonl] [--in-place]

Default: rewrites a scrubbed copy to <file>.scrubbed.jsonl.
NOTE: heuristic only; see app/logging_utils.scrub_text limitations.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.logging_utils import scrub_value


def main() -> int:
    parser = argparse.ArgumentParser(description="Heuristic log scrubber")
    parser.add_argument("--logs", type=Path, nargs="*", default=[Path("logs/session.log.jsonl")])
    parser.add_argument(
        "--in-place", action="store_true", help="Overwrite the source file (backup .bak first)"
    )
    args = parser.parse_args()

    total_lines = 0
    changed_lines = 0
    for log_path in args.logs:
        if not log_path.exists():
            print(f"[SKIP] {log_path} not found", file=sys.stderr)
            continue
        out_lines: list[str] = []
        with log_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    record = json.loads(stripped)
                except json.JSONDecodeError:
                    out_lines.append(line)
                    continue
                scrubbed = scrub_value(record)
                out_lines.append(json.dumps(scrubbed, ensure_ascii=False))
                if scrubbed != record:
                    changed_lines += 1
                total_lines += 1
        target = log_path
        if not args.in_place:
            target = log_path.with_suffix(log_path.suffix + ".scrubbed.jsonl")
        elif log_path.exists():
            backup = log_path.with_suffix(log_path.suffix + ".bak")
            backup.write_bytes(log_path.read_bytes())
        target.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"[OK] {log_path} -> {target} ({total_lines} lines, {changed_lines} changed)")

    if changed_lines:
        print(f"\nHeuristic scrub found {changed_lines}/{total_lines} records needing changes.")
        print("IMPORTANT: review results; this is not legal-grade redaction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
