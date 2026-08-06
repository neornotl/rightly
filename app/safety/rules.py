"""Rule-based checks (pure keyword/regex heuristics, no LLM).

Order of application matters: RED first, then ORANGE, then scope checks.

IMPORTANT: these rules are conservative heuristics for Vietnamese text. They
are NOT a replacement for trained classifiers and must be reviewed with a
Vietnamese-speaking safety expert before pilot (docs/responsible_ai.md).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_EMERGENCY_PATTERNS = [
    r"cấp cứu",
    r"đau tim",
    r"đột quỵ",
    r"ngộ độc",
    r"tự tử",
    r"tự sát",
    r"muốn chết",
    r"sốc phản vệ",
    r"cháy",
    r"hỏa hoạn",
    r"nguy hiểm đến tính mạng",
    r"đang bị tấn công",
    r"bị đánh gấp",
    r"khủng hoảng",
]

_VIOLENCE_THREAT_PATTERNS = [
    r"đe dọa",
    r"bạo lực",
    r"hành hung",
    r"bắt cóc",
    r"cướp",
    r"xâm hại",
    r"hiếp dâm",
]

_LEGAL_PATTERNS = [
    r"tòa án",
    r"tòa ",
    r"tranh chấp",
    r"kiện (tụng|ra tòa|tòa)",
    r"khởi kiện",
    r"phán quyết",
    r"án tòa",
    r"chia tài sản (ly hôn|thừa kế)",
    r"quyết định của tòa",
    r"luật sư",
    r"đòi nợ",
    r"đất (đai )?tranh chấp",
]

_OUT_OF_SCOPE_PATTERNS = [
    r"dự đoán (giá|xổ số|kết quả)",
    r"xổ số",
    r"chơi (chứng khoán|bạc)",
    r"cá cược",
    r"thầy bói",
    r"bói toán",
    r"tử vi",
    r"tin tức nóng",
    r"bình luận chính trị",
    r"hướng dẫn (làm|nấu|cày) (game|game)",
    r"phim ",
    r"bài tập về nhà",
]

_DOUBT_WORDS = [
    r"hay là",
    r"hay\?",
    r"không biết",
    r"không rõ",
    r"có phải",
    r"là gì nhỉ",
    r"thế nào nhỉ",
    r"hả",
]

_COMPILED = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in _EMERGENCY_PATTERNS
    + _VIOLENCE_THREAT_PATTERNS
    + _LEGAL_PATTERNS
    + _OUT_OF_SCOPE_PATTERNS
    + _DOUBT_WORDS
]
_N_EMERGENCY = len(_EMERGENCY_PATTERNS)
_N_VIOLENCE = len(_VIOLENCE_THREAT_PATTERNS)
_N_LEGAL = len(_LEGAL_PATTERNS)
_N_OOS = len(_OUT_OF_SCOPE_PATTERNS)


@dataclass(frozen=True)
class RuleHits:
    emergency: list[str] = field(default_factory=list)
    violence: list[str] = field(default_factory=list)
    legal: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    ambiguous: list[str] = field(default_factory=list)


def _match(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE) is not None


def check_rules(normalized_text: str) -> RuleHits:
    """Run all rule groups on normalized (lowercased) Vietnamese text."""
    hits = RuleHits()
    text = normalized_text.casefold()
    for i, pat in enumerate(_EMERGENCY_PATTERNS):
        if _match(pat, text):
            hits.emergency.append(pat)
    for i, pat in enumerate(_VIOLENCE_THREAT_PATTERNS):
        if _match(pat, text):
            hits.violence.append(pat)
    for i, pat in enumerate(_LEGAL_PATTERNS):
        if _match(pat, text):
            hits.legal.append(pat)
    for i, pat in enumerate(_OUT_OF_SCOPE_PATTERNS):
        if _match(pat, text):
            hits.out_of_scope.append(pat)
    for i, pat in enumerate(_DOUBT_WORDS):
        if _match(pat, text):
            hits.ambiguous.append(pat)
    return hits


def normalize_query(text: str) -> str:
    """Lowercase + collapse whitespace (diacritics preserved)."""
    return " ".join(text.casefold().split())
