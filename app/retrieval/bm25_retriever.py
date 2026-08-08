"""Pure-Python Okapi BM25 retriever (no numpy/scikit-learn needed)."""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field

from app.retrieval.base import Retriever
from app.retrieval.document_loader import ChunkRecord, DocumentLoader
from app.schemas import RetrievedChunk

_TOKEN_RE = re.compile(
    r"[a-zA-Z0-9_]+|[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+",
    re.IGNORECASE,
)

# Common Vietnamese function words excluded from matching so that generic
# queries ("là gì", "tôi muốn") cannot push scores above the threshold.
# NOTE: tokens are diacritic-stripped, so entries must be plain ASCII.
_VIETNAMESE_STOPWORDS = {
    "toi",
    "ban",
    "ong",
    "ba",
    "chu",
    "co",
    "chau",
    "em",
    "anh",
    "chi",
    "cua",
    "va",
    "voi",
    "la",
    "thi",
    "ma",
    "de",
    "cho",
    "tai",
    "o",
    "co",
    "khong",
    "phai",
    "nen",
    "se",
    "da",
    "dang",
    "duoc",
    "bi",
    "nay",
    "kia",
    "do",
    "day",
    "gi",
    "nao",
    "sao",
    "vi",
    "do",
    "nhung",
    "hay",
    "hoac",
    "neu",
    "cung",
    "rat",
    "nhung",
    "cac",
    "mot",
    "can",
    "muon",
    "hoi",
    "giup",
    "khi",
    "vao",
    "ra",
    "len",
    "xuong",
    "di",
    "lai",
    "xem",
    "toi",
    "den",
    "con",
    "deu",
    "moi",
    "moi",
    "nguoi",
    "the",
    "lam",
}


def normalize_vietnamese(text: str) -> str:
    """Lowercase + strip diacritics (for matching robustness)."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.casefold()


@dataclass
class BM25Retriever(Retriever):
    """Okapi BM25 with default k1=1.5, b=0.75.

    ``min_token_overlap``: a document must share at least this many distinct
    query tokens (2 by default) to be returned. This is the primary guard
    against noise matches — a single generic word ("thế", "gì") must never
    look like a confident retrieval.
    """

    name: str = "bm25"
    k1: float = 1.5
    b: float = 0.75
    min_token_overlap: int = 2
    chunks: list[ChunkRecord] = field(default_factory=list)
    _doc_freqs: Counter = field(default_factory=Counter, repr=False)
    _doc_lens: list[int] = field(default_factory=list, repr=False)
    _avg_len: float = 0.0
    _doc_token_sets: list[set[str]] = field(default_factory=list, repr=False)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        tokens = [t.casefold() for t in _TOKEN_RE.findall(normalize_vietnamese(text))]
        return [t for t in tokens if t not in _VIETNAMESE_STOPWORDS]

    def _build(self) -> None:
        self._doc_lens = []
        self._doc_token_sets = []
        all_freqs: Counter = Counter()
        for chunk in self.chunks:
            toks = self._tokenize(chunk.text)
            self._doc_lens.append(len(toks))
            uniq = set(toks)
            self._doc_token_sets.append(uniq)
            for t in uniq:
                all_freqs[t] += 1
        self._doc_freqs = all_freqs
        n = len(self.chunks)
        self._avg_len = (sum(self._doc_lens) / n) if n else 0.0

    @classmethod
    def from_jsonl(cls, chunks_path) -> "BM25Retriever":
        records = DocumentLoader.load_chunks(chunks_path)
        retriever = cls(chunks=records)
        retriever._build()
        return retriever

    @classmethod
    def from_chunks(cls, chunks: list[ChunkRecord]) -> "BM25Retriever":
        retriever = cls(chunks=chunks)
        retriever._build()
        return retriever

    def _score_doc(self, query_tokens: list[str], idx: int) -> float:
        if not query_tokens or not self.chunks:
            return 0.0
        n = len(self.chunks)
        uniq_q = set(query_tokens)
        doc_tokens = self._doc_token_sets[idx]
        doc_len = self._doc_lens[idx]
        score = 0.0
        for term in sorted(uniq_q):
            df = self._doc_freqs.get(term, 0)
            if df == 0 or term not in doc_tokens:
                continue
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            tf = self._tokenize(self.chunks[idx].text).count(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self._avg_len)
            score += idf * (tf * (self.k1 + 1)) / denom
        return score

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        if not self.chunks:
            return []
        query_tokens = self._tokenize(query)
        uniq_query = set(query_tokens)
        if not query_tokens:
            return []
        if len(uniq_query) == 1:
            # Council T3: single-token queries keep the overlap guard lifted,
            # but tokens that appear in >50% of the corpus are too generic to
            # match anything ("phường", "hồ sơ") — treat them as empty.
            token = next(iter(uniq_query))
            if self._doc_freqs.get(token, 0) > len(self.chunks) / 2:
                return []
        scored = sorted(
            ((self._score_doc(query_tokens, i), i) for i in range(len(self.chunks))),
            key=lambda pair: pair[0],
            reverse=True,
        )
        results: list[RetrievedChunk] = []
        for score, idx in scored:
            if score <= 0.0:
                break
            overlap = len(uniq_query & self._doc_token_sets[idx])
            if overlap < self.min_token_overlap and len(uniq_query) > 1:
                continue
            rec = self.chunks[idx]
            results.append(
                RetrievedChunk(
                    chunk_id=rec.chunk_id,
                    source_id=rec.source_id,
                    text=rec.text,
                    score=round(score, 4),
                    metadata=DocumentLoader.to_metadata(rec),
                )
            )
            if len(results) >= top_k:
                break
        return results
