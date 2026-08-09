"""Mock LLM: deterministic, template-based answer generation from chunks.

No model, no API. Used as the default backend and as the safe fallback when a
real backend fails. Never invents source IDs (only uses provided chunk
source_ids).
"""

from __future__ import annotations

import json

from app.llm.base import BaseLLM
from app.schemas import RetrievedChunk


class MockLLM(BaseLLM):
    name = "mock"

    def generate_answer(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        max_chars: int = 2000,
    ) -> dict:
        if not chunks:
            raise ValueError("MockLLM requires at least one retrieved chunk.")
        top = self._pick_content_chunk(chunks)
        source_ids = list(dict.fromkeys(c.source_id for c in chunks))
        # Take a concise extract from the top chunk (first ~2 sentences).
        body = top.text.strip()
        answer = self._summarize(body)
        answer = answer[:max_chars]
        spoken = (
            f"Thông tin lấy từ {top.metadata.title if top.metadata else top.source_id} "
            f"({', '.join(source_ids)})."
        )
        return {
            "answer_text": answer,
            "spoken_citation": spoken,
            "source_ids": source_ids,
            "limitations": [
                "Đây là dữ liệu DEMO, không phải hướng dẫn chính thức.",
            ],
            "next_step": "Bạn có muốn tôi nói lại hoặc hỏi nguồn ở đâu không?",
        }

    @staticmethod
    def _pick_content_chunk(chunks: list[RetrievedChunk]) -> RetrievedChunk:
        """Prefer the top chunk that is actual content (not a title/warning).

        Markdown title blocks ("# ...") and "LƯU Ý QUAN TRỌNG" intro blocks are
        skipped so the stub answer reads like a real answer. Falls back to the
        top-ranked chunk.
        """
        for chunk in chunks:
            first_line = chunk.text.strip().splitlines()[0] if chunk.text.strip() else ""
            if first_line.startswith("#"):
                continue
            if "LƯU Ý QUAN TRỌNG" in chunk.text[:200].upper():
                continue
            return chunk
        return chunks[0]

    @staticmethod
    def _summarize(text: str, max_sentences: int = 3) -> str:
        import re

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        clean = [s for s in sentences if not s.startswith(("#", "*", "-", ">", "="))]
        if not clean:
            clean = sentences
        return " ".join(clean[:max_sentences])

    @staticmethod
    def to_json(doc: dict) -> str:
        return json.dumps(doc, ensure_ascii=False)
