"""P6: Citation validator report on curated cases.

Runs the validator against sample answers (incl. the NĐ 62/2021 expiry
case), maps failures to policy decisions, and writes
results/citation_validator_report.json.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parent.parent

from app.safety.policy import Policy  # noqa: E402
from app.schemas import GroundedAnswer  # noqa: E402
from app.validation.citation_validator import CitationValidator  # noqa: E402

CASES = [
    ("C1_outdated_nd62", "nd62_2021", {"nd62_2021"}, "NĐ 62/2021 hết hiệu lực 10/01/2025"),
    ("C2_valid_nd154", "nd154_2024", {"nd154_2024"}, "Trích dẫn hợp lệ (hiệu lực)"),
    ("C3_unsupported", "luat60_2014", {"nd123_2015"}, "Trích dẫn không thuộc nguồn truy xuất"),
    ("C4_unknown", "luat99_9999", {"nd123_2015"}, "Source_id không tồn tại"),
    (
        "C5_valid_multi",
        "nd123_2015;luat60_2014",
        {"nd123_2015", "luat60_2014"},
        "Đa trích dẫn hợp lệ",
    ),
]


def main() -> int:
    validator = CitationValidator(
        status_path=ROOT / "data" / "law_status.json",
        today=date.today(),
    )
    policy = Policy()
    rows = []
    for name, cited, retrieved, note in CASES:
        ids = [s.strip() for s in cited.split(";")]
        verdict = validator.validate(GroundedAnswer(answer_text="x", source_ids=ids), retrieved)
        decision = None
        if not verdict.ok:
            outdated = any(i.kind == "outdated" for i in verdict.issues)
            decision = policy.citation_decision(outdated=outdated).to_dict()
        rows.append(
            {
                "case": name,
                "note": note,
                "cited": ids,
                "retrieved": sorted(retrieved),
                "verdict": verdict.to_dict(),
                "policy": decision,
            }
        )
        print(f"{name:<20} ok={verdict.ok} issues={[i.kind for i in verdict.issues]}")

    out = ROOT / "results" / "citation_validator_report.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        json.dumps(
            {"today": date.today().isoformat(), "cases": rows}, ensure_ascii=False, indent=2
        ),
        encoding="utf-8",
    )
    print(f"\nSaved: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
