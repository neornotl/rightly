"""Run a 1,000-question, non-FAQ answerability benchmark.

The benchmark reports objective checks and preserves every answer for human
review. It does not claim legal correctness from an LLM self-score alone.

Usage:
    python -m eval.benchmark_1000 --limit 1000 --output results/benchmark_1000
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from pathlib import Path

from app.config import load_settings
from app.faq import FAQMatcher
from app.pipeline import Pipeline
from app.retrieval.document_loader import DocumentLoader


def _sentences(text: str) -> list[str]:
    candidates = []
    for part in re.split(r"(?<=[.!?;])\s+|\n+", text):
        part = re.sub(r"\s+", " ", part).strip(" .;:")
        lowered = part.casefold()
        if len(part) < 55 or len(part) > 180:
            continue
        if any(marker in lowered for marker in ("source_id:", "title:", "source_type:", "publisher:", "published_date:", "url:", "notes:", "http://", "https://")):
            continue
        letters = [char for char in part if char.isalpha()]
        if letters and sum(char.isupper() for char in letters) / len(letters) > 0.55:
            continue
        if lowered.startswith(("ngh định", "chính phủ", "cộng hòa", "chương ", "mục ", "phần ")):
            continue
        if re.search(r"\b(?:chương|mục|phần)\s+[ivxlcdm0-9]+\b", lowered):
            continue
        if lowered.startswith(("căn cứ", "xét đề nghị", "nơi nhận", "nơi nhận:")):
            continue
        if re.search(r"\b(?:sau đây gọi là|quy định tại|theo quy định tại)\s*$", lowered):
            continue
        if not re.search(r"(?:điều|khoản|điểm|phạt|hồ sơ|giấy|thủ tục|người|cơ quan|thời hạn|quyền|nghĩa vụ)", lowered):
            continue
        candidates.append(part)
    return candidates


def _make_queries(limit: int, faq: FAQMatcher) -> list[dict]:
    settings = load_settings()
    records = DocumentLoader.load_chunks(settings.chunks_dir / "real_chunks.jsonl")
    variants = (
        "Bác giải thích giúp quy định này: {topic}.",
        "Nếu tôi gặp trường hợp này thì cần hiểu thế nào: {topic}.",
        "Quy định trên áp dụng ra sao trong thực tế: {topic}.",
        "Tôi là người dân, cần biết mình phải làm gì theo quy định này: {topic}.",
    )
    output: list[dict] = []
    seen: set[str] = set()
    for record in records:
        if record.chunk_id.endswith("::c000"):
            continue
        title = record.title or record.source_id
        for sentence in _sentences(record.text):
            topic = re.sub(r"\s+", " ", sentence).strip(" .;:")
            if len(topic) > 150:
                topic = topic[:150].rsplit(" ", 1)[0]
            for variant in variants:
                query = variant.format(topic=topic)
                if query in seen or faq.answer(query) is not None:
                    continue
                seen.add(query)
                output.append(
                    {
                        "case_id": len(output) + 1,
                        "query": query,
                        "expected_source_id": record.source_id,
                        "expected_title": title,
                        "chunk_id": record.chunk_id,
                    }
                )
                if len(output) >= limit:
                    return output
    return output


def _number_tokens(text: str) -> set[str]:
    return set(re.findall(r"\b\d+(?:[.,]\d+)*\b", text))


_VI_STOP = {
    "theo", "quy", "dinh", "nay", "duoc", "la", "gi", "nhu", "nao", "cho",
    "toi", "bác", "bac", "muon", "hoi", "ro", "thi", "can", "biet", "ve",
    "voi", "neu", "gap", "truong", "hop", "phai", "lam", "sao", "cho", "toi",
}


def _terms(text: str) -> set[str]:
    words = re.findall(r"[a-zA-ZÀ-ỹđĐ0-9]{3,}", text.casefold())
    return {word for word in words if word not in _VI_STOP}


def _score(case: dict, result, source_text: str) -> tuple[int, list[str]]:
    reasons: list[str] = []
    answer = result.answer
    if not answer or not answer.answer_text.strip():
        reasons.append("empty_answer")
        return 0, reasons
    score = 1
    if result.faq_answered:
        reasons.append("faq_answered")
    else:
        score += 1
    source_ids = set(answer.source_ids) | {chunk.source_id for chunk in result.chunks}
    if case["expected_source_id"] in source_ids:
        score += 1
    else:
        reasons.append("expected_source_missing")
    if answer.spoken_citation.strip():
        score += 1
    else:
        reasons.append("missing_citation")
    text = answer.answer_text.strip()
    words = text.split()
    sentence_lengths = [len(s.split()) for s in _sentences(text)]
    if 12 <= len(words) <= 180 and (not sentence_lengths or max(sentence_lengths) <= 42):
        score += 1
    else:
        reasons.append("hard_to_read_length")
    evidence = " ".join(chunk.text for chunk in result.chunks) + " " + source_text
    unsupported_numbers = _number_tokens(text) - _number_tokens(evidence)
    if unsupported_numbers:
        reasons.append("unsupported_numbers:" + ",".join(sorted(unsupported_numbers)))
    query_terms = _terms(case["query"])
    answer_terms = _terms(text)
    focus_ratio = len(query_terms & answer_terms) / max(len(query_terms), 1)
    if focus_ratio < 0.18:
        reasons.append("off_topic_or_too_generic")
    evidence_terms = _terms(evidence)
    answer_factual_terms = _terms(text) - {"anh", "chi", "da", "thua", "xin", "cam", "on"}
    evidence_ratio = len(answer_factual_terms & evidence_terms) / max(len(answer_factual_terms), 1)
    if evidence_ratio < 0.30:
        reasons.append("weak_evidence_support")
    if len(words) > 120:
        reasons.append("possibly_excessive")
    if re.search(r"source_id|chunk_id|```|\{.*answer_text", text, re.I):
        reasons.append("internal_format_leak")
    return score, reasons


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=Path("results/benchmark_1000"))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--checkpoint-every", type=int, default=10)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    faq = FAQMatcher()
    cases = _make_queries(args.limit, faq)
    settings = load_settings()
    source_texts: dict[str, str] = {}
    for record in DocumentLoader.load_chunks(settings.chunks_dir / "real_chunks.jsonl"):
        source_texts[record.source_id] = source_texts.get(record.source_id, "") + " " + record.text
    pipeline = Pipeline(settings=settings)
    session_id = pipeline.create_session()
    rows: list[dict] = []
    cases_path = args.output / "cases.jsonl"
    if args.resume and cases_path.exists():
        for line in cases_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        rows = rows[: len(cases)]
    completed = {row["case_id"] for row in rows}
    for case in cases:
        if case["case_id"] in completed:
            continue
        try:
            result = pipeline.process_text(session_id, case["query"])
            score, reasons = _score(case, result, source_texts.get(case["expected_source_id"], ""))
            row = {
                **case,
                "score": score,
                "max_score": 5,
                "flags": reasons,
                "result": result.to_dict(),
            }
        except Exception as exc:  # keep every case auditable
            row = {**case, "score": 0, "max_score": 5, "flags": [f"exception:{exc}"]}
        rows.append(row)
        if len(rows) % args.checkpoint_every == 0:
            cases_path.write_text(
                "\n".join(json.dumps(item, ensure_ascii=False) for item in rows) + "\n",
                encoding="utf-8",
            )
            print(f"[BENCHMARK] {len(rows)}/{len(cases)}")

    cases_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )
    scores = [row["score"] for row in rows]
    flagged = [row for row in rows if row["flags"]]
    summary = {
        "cases": len(rows),
        "mean_score": round(statistics.mean(scores), 3) if scores else 0,
        "score_5_rate": round(sum(s == 5 for s in scores) / max(len(scores), 1), 3),
        "flagged_cases": len(flagged),
        "faq_leaks": sum("faq_answered" in row["flags"] for row in rows),
        "empty_answers": sum("empty_answer" in row["flags"] for row in rows),
        "accuracy_status": "needs_human_review_against_official_answers",
        "human_review_file": "cases.jsonl; sort by score ascending and inspect every flagged answer",
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (args.output / "review.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case_id", "score", "flags", "query", "answer"])
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (item["score"], item["case_id"])):
            answer = ((row.get("result") or {}).get("answer") or {}).get("answer_text", "")
            writer.writerow({
                "case_id": row["case_id"],
                "score": row["score"],
                "flags": ";".join(row["flags"]),
                "query": row["query"],
                "answer": answer,
            })
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
