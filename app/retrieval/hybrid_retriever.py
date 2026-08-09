"""Hybrid retrieval: BM25 + dense embeddings, fused with RRF, optional
cross-encoder rerank. Dense index uses a multilingual SentenceTransformer
with a disk cache of precomputed embeddings."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from app.retrieval.base import Retriever
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.document_loader import ChunkRecord, DocumentLoader
from app.schemas import RetrievedChunk

_QUERY_PREFIX = "query: "
_PASSAGE_PREFIX = "passage: "
_EMB_MODEL = "intfloat/multilingual-e5-small"
_RERANK_MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"

# Answerability gate thresholds, calibrated on the real corpus (8 demo
# queries). In-corpus queries score >= one threshold; out-of-corpus queries
# (e.g. "hộ chiếu", "phạt khai sinh quá hạn") fall below both.
_BM25_GATE = 12.2
_DENSE_GATE = 0.88


def _to_chunk(rec, score: float) -> RetrievedChunk:
    metadata = rec.metadata if hasattr(rec, "metadata") else DocumentLoader.to_metadata(rec)
    return RetrievedChunk(
        chunk_id=rec.chunk_id,
        source_id=rec.source_id,
        text=rec.text,
        score=round(float(score), 4),
        metadata=metadata,
    )


@dataclass
class DenseIndex:
    """Cosine-similarity dense retriever over chunk embeddings."""

    name: str = "dense"
    model_name: str = _EMB_MODEL
    cache_path: Path = field(default=Path("data/chunks/embeddings.npz"))
    chunks: list[ChunkRecord] = field(default_factory=list)
    _model: object = field(default=None, repr=False)
    _embeddings: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.cache_path = Path(self.cache_path)

    def _load_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _build(self) -> None:
        model = self._load_model()
        cache = Path(self.cache_path)
        texts = [f"{_PASSAGE_PREFIX}{c.text}" for c in self.chunks]
        if cache.exists():
            data = np.load(cache)
            if data["ids"].tolist() == [c.chunk_id for c in self.chunks]:
                self._embeddings = data["embeddings"]
                return
        self._embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez(
            cache,
            ids=[c.chunk_id for c in self.chunks],
            embeddings=self._embeddings.astype("float32"),
        )

    @classmethod
    def from_chunks(cls, chunks: list[ChunkRecord], cache_path=None) -> "DenseIndex":
        idx = cls(chunks=chunks)
        if cache_path:
            idx.cache_path = Path(cache_path)
        idx._build()
        return idx

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        if not self.chunks:
            return []
        model = self._load_model()
        q = model.encode([f"{_QUERY_PREFIX}{query}"], normalize_embeddings=True)[0]
        sims = self._embeddings @ q
        order = np.argsort(-sims)[:top_k]
        return [_to_chunk(self.chunks[i], float(sims[i])) for i in order if sims[i] > 0]


def _rrf_fuse(lists: list[list[RetrievedChunk]], k: int = 60) -> list[RetrievedChunk]:
    scores: dict[str, float] = {}
    order: dict[str, int] = {}
    for hits in lists:
        for rank, hit in enumerate(hits):
            scores[hit.chunk_id] = scores.get(hit.chunk_id, 0.0) + 1.0 / (k + rank + 1)
            if hit.chunk_id not in order:
                order[hit.chunk_id] = len(order)
    by_chunk = {h.chunk_id: h for hits in lists for h in hits}
    ranked = sorted(by_chunk, key=lambda cid: (-scores[cid], order[cid], cid))
    return [_to_chunk(by_chunk[cid], scores[cid]) for cid in ranked]


@dataclass
class HybridRetriever(Retriever):
    """BM25 + dense fused with RRF; optional cross-encoder rerank."""

    name: str = "hybrid"
    bm25: BM25Retriever = None  # type: ignore[assignment]
    dense: DenseIndex = None  # type: ignore[assignment]
    exclude_demo: bool = False
    rerank: bool = False
    gate: str = "bm25_dense"  # none | bm25_dense
    bm25_gate: float = _BM25_GATE
    dense_gate: float = _DENSE_GATE
    rerank_threshold: float = 0.0  # only applied when gate == "none"
    _reranker: object = field(default=None, repr=False)

    @classmethod
    def from_chunks(
        cls,
        chunks: list[ChunkRecord],
        cache_path=None,
        exclude_demo: bool = False,
        rerank: bool = False,
        gate: str = "bm25_dense",
        bm25_gate: float = _BM25_GATE,
        dense_gate: float = _DENSE_GATE,
    ) -> "HybridRetriever":
        bm25 = BM25Retriever.from_chunks(chunks)
        dense = DenseIndex.from_chunks(chunks, cache_path=cache_path)
        return cls(
            bm25=bm25,
            dense=dense,
            exclude_demo=exclude_demo,
            rerank=rerank,
            gate=gate,
            bm25_gate=bm25_gate,
            dense_gate=dense_gate,
        )

    def _filter(self, hits: list[RetrievedChunk]) -> list[RetrievedChunk]:
        if not self.exclude_demo:
            return hits
        return [h for h in hits if not (h.metadata and h.metadata.is_demo)]

    def _load_reranker(self):
        if self._reranker is None:
            from sentence_transformers import CrossEncoder

            self._reranker = CrossEncoder(_RERANK_MODEL)
        return self._reranker

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        pool = max(top_k * 4, 20)
        bm25_hits = self._filter(self.bm25.search(query, top_k=pool))
        dense_hits = self._filter(self.dense.search(query, top_k=pool))
        if self.gate == "bm25_dense":
            max_bm25 = bm25_hits[0].score if bm25_hits else 0.0
            max_dense = dense_hits[0].score if dense_hits else 0.0
            if max_bm25 < self.bm25_gate and max_dense < self.dense_gate:
                return []
        fused = _rrf_fuse([bm25_hits, dense_hits])
        if self.rerank and len(fused) > 1:
            reranker = self._load_reranker()
            pairs = [(query, h.text) for h in fused[:12]]
            scores = reranker.predict(pairs, show_progress_bar=False)
            # The gate already decides answerability; rerank only re-orders.
            threshold = self.rerank_threshold if self.gate == "none" else -1e9
            scored = [
                _to_chunk(h, float(s)) for h, s in zip(fused[:12], scores) if float(s) >= threshold
            ]
            scored.sort(key=lambda h: h.score, reverse=True)
            fused = scored
        return fused[:top_k]
