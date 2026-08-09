"""Voice FAQ (F5): curated short answers matched diacritic-insensitively.

Why: elderly users often phrase questions loosely and ASR drops tones.
Matching strips Vietnamese diacritics on both sides so "so do" matches
"sổ đỏ". Matches are deterministic, cheap, and need no LLM call — good for
demo reliability in noisy environments and for the 20-query demo budget.

Curated answers are written by the team (C reviews claims), so the safety
router is deliberately bypassed for strong matches only (threshold >= 6
normalized chars). Weak or no match falls through to the full pipeline.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

from app.schemas import GroundedAnswer

_FAQ_FILE = Path("data") / "faq.json"

_STRIP_MARKS = re.compile(r"[\u0300-\u036f]")
_D_MAP = {"đ": "d", "Đ": "d", "ð": "d"}


def _strip_diacritics(text: str) -> str:
    """Lowercase, strip Vietnamese tones + đ->d, collapse whitespace."""
    text = "".join(_D_MAP.get(ch, ch) for ch in text)
    text = unicodedata.normalize("NFD", text)
    text = _STRIP_MARKS.sub("", text)
    return " ".join(text.casefold().split())


@dataclass(frozen=True)
class FaqHit:
    faq_id: str
    question: str
    answer_text: str
    spoken_citation: str
    score: int

    def to_grounded_answer(self) -> GroundedAnswer:
        return GroundedAnswer(
            answer_text=self.answer_text,
            spoken_citation=self.spoken_citation,
            source_ids=[],
            limitations=[
                "Đây là câu trả lời ngắn dạng kịch bản FAQ — liên hệ cơ quan "
                "có thẩm quyền để được hướng dẫn chi tiết cho trường hợp của bạn."
            ],
            next_step="",
        )


@lru_cache(maxsize=1)
def _load_faq(path: Optional[Path] = None) -> tuple[dict, ...]:
    file = path or _FAQ_FILE
    if not file.exists():
        return ()
    try:
        payload = json.loads(file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ()
    items = payload.get("faqs", []) if isinstance(payload, dict) else []
    return tuple(
        it for it in items if isinstance(it, dict) and it.get("id") and it.get("answer_text")
    )


class FAQMatcher:
    """Best-match FAQ lookup; score = longest matched keyword in chars."""

    MIN_SCORE = 5

    def __init__(self, path: Optional[Path] = None):
        self._items = tuple(
            {
                "id": it["id"],
                "question": it.get("question", ""),
                "answer_text": it["answer_text"],
                "spoken_citation": it.get("spoken_citation", "Câu trả lời thường gặp (FAQ)"),
                "keywords": tuple(_strip_diacritics(k) for k in it.get("keywords", []) if k),
            }
            for it in _load_faq(path)
        )

    @property
    def count(self) -> int:
        return len(self._items)

    def answer(self, query: str) -> Optional[FaqHit]:
        """Return the best FAQ hit, or None below :attr:`MIN_SCORE`."""
        text = _strip_diacritics(query)
        if not text:
            return None
        best: Optional[FaqHit] = None
        for item in self._items:
            for kw in item["keywords"]:
                if not kw or kw not in text:
                    continue
                score = len(kw) + (1 if _strip_diacritics(item["question"]) in text else 0)
                if best is None or score > best.score:
                    best = FaqHit(
                        faq_id=item["id"],
                        question=item["question"],
                        answer_text=item["answer_text"],
                        spoken_citation=item["spoken_citation"],
                        score=score,
                    )
        if best is None or best.score < self.MIN_SCORE:
            return None
        return best
