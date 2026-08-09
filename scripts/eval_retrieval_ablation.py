"""P5: Retrieval ablation on the real corpus (no LLM calls).

Compares BM25-only vs Dense-only vs Hybrid(RRF) vs Hybrid+rerank on
the 8 demo queries with manual source-level relevance labels.

Output: results/retrieval_ablation.json + printed table.
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parent.parent

from app.retrieval.bm25_retriever import BM25Retriever  # noqa: E402
from app.retrieval.document_loader import DocumentLoader  # noqa: E402
from app.retrieval.hybrid_retriever import DenseIndex, HybridRetriever  # noqa: E402

CHUNKS = ROOT / "data" / "chunks" / "real_chunks.jsonl"
CACHE = ROOT / "data" / "chunks" / "real_embeddings.npz"

QUERIES = [
    (
        "Q1",
        "Tôi cần đăng ký khai sinh cho con, thủ tục như thế nào?",
        {"nd123_2015", "luat60_2014", "nd07_2025"},
    ),
    (
        "Q2",
        "Hồ sơ đăng ký kết hôn cần những giấy tờ gì?",
        {"nd123_2015", "nd126_2014", "luat60_2014", "luat52_2014"},
    ),
    ("Q3", "Đăng ký tạm trú cần bao nhiêu ngày xử lý?", {"luat68_2020", "nd154_2024", "nd62_2021"}),
    (
        "Q4",
        "Tôi muốn xin cấp lại giấy khai sinh vì bị mất, phí là bao nhiêu?",
        {"nd123_2015", "luat60_2014", "nd07_2025"},
    ),
    (
        "Q5",
        "Thủ tục xin giấy xác nhận tình trạng hôn nhân mất bao lâu?",
        {"nd123_2015", "nd126_2014"},
    ),
    ("Q6", "Đăng ký khai sinh quá hạn có bị phạt không?", set()),
    ("Q7", "Hồ sơ xin cấp hộ chiếu gồm những gì?", set()),
    (
        "Q8",
        "Tôi cần thay đổi họ tên trong giấy khai sinh, làm ở đâu?",
        {"nd123_2015", "luat60_2014"},
    ),
]


def ndcg_at5(hits: list, relevant: set[str]) -> float:
    seen: set[str] = set()
    dcg = 0.0
    for rank, h in enumerate(hits[:5]):
        if h.source_id in relevant and h.source_id not in seen:
            seen.add(h.source_id)
            dcg += 1.0 / math.log2(rank + 2)
    ideal = sum(1.0 / math.log2(i + 2) for i in range(min(5, len(relevant))))
    return dcg / ideal if ideal else 0.0


def recall_at5(hits: list, relevant: set[str]) -> float:
    if not relevant:
        return 0.0
    return len({h.source_id for h in hits[:5]} & relevant) / len(relevant)


def noise_at5(hits: list, relevant: set[str]) -> float:
    if not hits:
        return 0.0
    if not relevant:
        return 1.0
    return sum(1 for h in hits[:5] if h.source_id not in relevant) / len(hits[:5])


def run_variant(name: str, search_fn) -> dict:
    rows = []
    for qid, q, rel in QUERIES:
        t0 = time.perf_counter()
        hits = search_fn(q)
        ms = (time.perf_counter() - t0) * 1000.0
        rows.append(
            {
                "query_id": qid,
                "latency_ms": round(ms, 1),
                "retrieved": [h.source_id for h in hits[:5]],
                "recall@5": round(recall_at5(hits, rel), 4),
                "ndcg@5": round(ndcg_at5(hits, rel), 4),
                "noise@5": round(noise_at5(hits, rel), 4),
                "expected_sources": sorted(rel),
            }
        )
    n = len(rows)
    return {
        "variant": name,
        "rows": rows,
        "mean_recall@5": round(sum(r["recall@5"] for r in rows) / n, 4),
        "mean_ndcg@5": round(sum(r["ndcg@5"] for r in rows) / n, 4),
        "mean_latency_ms": round(sum(r["latency_ms"] for r in rows) / n, 1),
        "empty_retrievals": sum(1 for r in rows if not r["retrieved"]),
    }


def main() -> int:
    chunks = DocumentLoader.load_chunks(CHUNKS)
    print(f"chunks: {len(chunks)}")

    bm25 = BM25Retriever.from_chunks(chunks)
    dense = DenseIndex.from_chunks(chunks, cache_path=CACHE)
    hybrid = HybridRetriever.from_chunks(chunks, cache_path=CACHE, rerank=False)
    hybrid_rr = HybridRetriever.from_chunks(chunks, cache_path=CACHE, rerank=True)

    results = [
        run_variant("bm25", lambda q: bm25.search(q, top_k=5)),
        run_variant("dense", lambda q: dense.search(q, top_k=5)),
        run_variant("hybrid_rrf", lambda q: hybrid.search(q, top_k=5)),
        run_variant("hybrid_rerank", lambda q: hybrid_rr.search(q, top_k=5)),
    ]

    print(f"\n{'variant':<14} {'r@5':>6} {'nDCG@5':>8} {'noise@5':>8} {'empty':>6} {'lat(ms)':>8}")
    for r in results:
        mean_noise = round(sum(row["noise@5"] for row in r["rows"]) / len(r["rows"]), 4)
        print(
            f"{r['variant']:<14} {r['mean_recall@5']:>6} {r['mean_ndcg@5']:>8} "
            f"{mean_noise:>8} {r['empty_retrievals']:>6} {r['mean_latency_ms']:>8}"
        )

    out = ROOT / "results" / "retrieval_ablation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        json.dumps({"queries": len(QUERIES), "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nSaved: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
