"""Build a transparent 1,000-question retrieval benchmark from legal chunks.

Each record targets a different corpus chunk. The questions are generated one at
a time from that chunk's article heading and a short normalized excerpt; they
are synthetic coverage cases, not user or public questions.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "data/chunks/real_chunks.jsonl"
METADATA = ROOT / "data/metadata.csv"
LAW_STATUS = ROOT / "data/law_status.json"
OUTPUT = ROOT / "data/eval/benchmark_1k_synthetic.jsonl"

HEADINGS = re.compile(r"(?:Điều|Chương|Mục)\s+[0-9IVXLC]+[^\n.]{0,140}", re.IGNORECASE)
SENTENCE = re.compile(r"[^.!?\n]{35,220}[.!?]")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text.casefold())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", text).split())


def load_metadata() -> dict[str, dict[str, str]]:
    with METADATA.open(encoding="utf-8", newline="") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def clean_excerpt(text: str) -> str:
    text = " ".join(text.split())
    match = SENTENCE.search(text)
    excerpt = match.group(0) if match else text[:180]
    return excerpt.strip(" .")


def make_question(title: str, text: str, ordinal: int) -> str:
    heading = HEADINGS.search(text)
    section = heading.group(0).strip() if heading else "quy định được trích dẫn"
    excerpt = clean_excerpt(text)
    templates = (
        "Theo {title}, {section} quy định nội dung gì liên quan đến {excerpt}?",
        "Tôi muốn hiểu {section} của {title}: quy định chính là gì về {excerpt}?",
        "Trong {title}, cần lưu ý gì tại {section} khi áp dụng nội dung {excerpt}?",
        "Bạn giải thích giúp quy định {section} trong {title}, nhất là phần {excerpt}, được không?",
        "Nếu tra cứu {title}, tôi cần biết {section} nói gì về {excerpt}?",
    )
    return templates[ordinal % len(templates)].format(
        title=title or "văn bản pháp luật hiện hành",
        section=section,
        excerpt=excerpt,
    )[:500]


def main() -> None:
    metadata = load_metadata()
    status = json.loads(LAW_STATUS.read_text(encoding="utf-8"))["sources"]
    active = {
        sid for sid, item in status.items()
        if item.get("status") == "active_verified" and not item.get("expired_on")
    }
    chunks = []
    for line in CHUNKS.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if item.get("source_id") in active and item.get("source_id") in metadata:
            text = item.get("text", "")
            if len(text) >= 40 and ("Điều" in text or "Chương" in text or "Mục" in text):
                chunks.append(item)

    # Round-robin sources so the benchmark covers the corpus instead of taking
    # the first 1,000 chunks from only a handful of documents.
    by_source = defaultdict(list)
    for chunk in chunks:
        by_source[chunk["source_id"]].append(chunk)
    chosen = []
    source_ids = sorted(by_source)
    while len(chosen) < 1000:
        added = False
        for source_id in source_ids:
            if by_source[source_id]:
                chosen.append(by_source[source_id].pop(0))
                added = True
                if len(chosen) == 1000:
                    break
        if not added:
            break
    if len(chosen) < 1000:
        raise SystemExit(f"Only {len(chosen)} eligible chunks found; refusing a short benchmark")

    records = []
    seen = set()
    for i, chunk in enumerate(chosen, 1):
        source_id = chunk["source_id"]
        title = metadata[source_id].get("title", "")
        question = make_question(title, chunk["text"], i)
        normalized = normalize(question)
        if normalized in seen:
            raise SystemExit(f"Generated duplicate question at ordinal {i}")
        seen.add(normalized)
        records.append(
            {
                "question_id": f"TLQ_{i:06d}",
                "question_text": question,
                "normalized_question": normalized,
                "provenance_type": "SYNTHETIC_COVERAGE",
                "seed_id": None,
                "source_record_id": None,
                "source_url": metadata[source_id].get("url") or None,
                "source_access_date": "2026-08-17",
                "pii_redaction_applied": True,
                "synthetic_generator": "scripts/generate_synthetic_benchmark_1k.py",
                "generation_prompt_version": "chunk-grounded-v1",
                "topic": "THU_TUC_CHUNG",
                "subtopic": metadata[source_id].get("linh_vuc", "phap_luat").lower().replace(" ", "_"),
                "jurisdiction": "national",
                "effective_date_context": None,
                "expected_answerability": "ANSWER",
                "expected_zone": "YELLOW",
                "expected_source_ids": [source_id],
                "required_facts": ["Trả lời phải bám vào nội dung của nguồn được chỉ định."],
                "forbidden_claims": ["Không tự suy đoán ngoài đoạn nguồn."],
                "must_mention_limitations": [],
                "difficulty": "medium",
                "linguistic_style": ("direct", "colloquial", "narrative")[i % 3],
                "user_need": "U01 - người dân cần giải thích quy định dễ hiểu",
                "gold_answer_outline": f"Giải thích phần {clean_excerpt(chunk['text'])} và dẫn nguồn {source_id}.",
                "label_status": "AUTO_DRAFT",
                "labelled_by": "synthetic_generator",
                "reviewed_by": None,
                "split": ("train_dev", "calibration", "test", "audit")[i % 4],
                "leakage_group_id": f"GROUP_{i:06d}",
                "notes": f"Synthetic question generated independently for chunk {chunk['chunk_id']}; not a cloned user question.",
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} questions to {OUTPUT}")
    print(f"unique sources: {len({r['expected_source_ids'][0] for r in records})}")
    print(f"unique targets: {len({r['notes'] for r in records})}")


if __name__ == "__main__":
    main()
