"""Hybrid safety router.

Order of checks (rule-based FIRST, LLM classification OPTIONAL last):

1. Emergency / violence signals (RED) — run BEFORE any LLM call.
2. Legal-judgment requests (ORANGE/GUIDE).
3. Out-of-scope topics (ORANGE/GUIDE).
4. Retrieval sufficiency (no answer if below MIN_RETRIEVAL_SCORE or empty).
5. Ambiguity check.
6. Optional structured LLM classification (cloud mode only).
7. Conservative fallback: anything unresolved becomes CLARIFY/REFUSE, never a
   confident answer without evidence.

The LLM never decides routing alone: rule hits always take precedence.
"""

from __future__ import annotations

from typing import Callable, Optional

from app.config import Settings
from app.safety.policy import Policy
from app.safety.rules import RuleHits, check_rules, normalize_query
from app.schemas import RetrievedChunk, SafetyDecision, Zone


class SafetyRouter:
    def __init__(
        self,
        settings: Optional[Settings] = None,
        policy: Optional[Policy] = None,
        min_score: Optional[float] = None,
    ):
        self.settings = settings or Settings()
        self.policy = policy or Policy()
        self.min_score = min_score if min_score is not None else self.settings.min_retrieval_score

    def route(
        self,
        raw_query: str,
        chunks: list[RetrievedChunk],
        llm_classifier: Optional[Callable[[str, list[RetrievedChunk]], bool]] = None,
    ) -> tuple[SafetyDecision, str]:
        """Return (decision, normalized_query)."""
        query = normalize_query(raw_query)
        if not query:
            return self.policy.ambiguous_decision(), query

        hits: RuleHits = check_rules(query)

        # 1. RED rules have highest priority, before any LLM.
        if hits.emergency:
            return self.policy.emergency_decision(), query
        if hits.violence:
            return self.policy.violence_decision(), query

        # 2. Criminal-matter requests (careful, refer out before any conclusion).
        if hits.criminal:
            return self.policy.criminal_decision(), query

        # 3. Legal judgment requests.
        if hits.legal:
            return self.policy.legal_decision(), query

        # 4. Out-of-scope.
        if hits.out_of_scope:
            return self.policy.out_of_scope_decision(), query

        # 5. Retrieval sufficiency.
        sufficient = [c for c in chunks if c.score >= self.min_score]
        if not sufficient:
            return self.policy.insufficient_decision(), query

        # 6. Ambiguity heuristics.
        if hits.ambiguous and not chunks:
            return self.policy.ambiguous_decision(), query
        if len(hits.ambiguous) >= 2:
            return self.policy.ambiguous_decision(), query

        # 7. Optional structured LLM classification (only when provided).
        if llm_classifier is not None:
            try:
                safe = llm_classifier(query, sufficient)
            except Exception:
                safe = False  # conservative: on failure, do not auto-answer
            if not safe:
                return self.policy.ambiguous_decision(), query
            return self.policy.safe_decision(llm_reasoned=True), query

        # 8. Conservative fallback: grounded safe answer.
        return self.policy.safe_decision(llm_reasoned=False), query

    def would_answer(self, decision: SafetyDecision) -> bool:
        """True when the pipeline may produce a grounded spoken answer."""
        return decision.zone == Zone.YELLOW and decision.action.value == "ANSWER"
