"""Groq LLM adapter (optional, lazy import of groq SDK)."""

from __future__ import annotations

import json

from app.llm.base import BaseLLM, LLMError
from app.schemas import RetrievedChunk

_SYSTEM = (
    "Bạn là trợ lý tra cứu thủ tục hành chính có nguồn dẫn chứng (grounded). "
    "Chỉ trả lời dựa trên CHÍNH XÁC các đoạn văn bản được cung cấp. "
    "Tuyệt đối không bịa thông tin, không tạo source_id mới. "
    "Trả về JSON duy nhất với schema: "
    '{"answer_text": string, "spoken_citation": string, "source_ids": [string], '
    '"limitations": [string], "next_step": string}.'
)


class GroqLLM(BaseLLM):
    name = "groq"

    def __init__(self, api_key: str = "", model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self):
        if self._client is None:
            try:
                from groq import Groq  # type: ignore

                self._client = Groq(api_key=self.api_key)
            except ImportError as exc:
                raise LLMError(
                    "groq not installed. pip install -r requirements-optional.txt"
                ) from exc
            except Exception as exc:
                raise LLMError(f"Failed to init Groq client: {exc}") from exc
        return self._client

    def generate_answer(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        max_chars: int = 2000,
    ) -> dict:
        if not self.available:
            raise LLMError("GROQ_API_KEY is not set (LLM_BACKEND=groq).")
        context = "\n\n".join(
            f"[source_id={c.source_id}|chunk_id={c.chunk_id}]\n{c.text}" for c in chunks
        )
        user = (
            f"Câu hỏi: {query}\n\n"
            f"Các đoạn nguồn (chỉ được dùng các source_id này):\n{context}\n\n"
            f"Giới hạn câu trả lời: {max_chars} ký tự."
        )
        client = self._get_client()
        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": user},
                ],
                temperature=0.2,
            )
            text = completion.choices[0].message.content.strip()
            text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMError(f"Groq returned non-JSON output: {exc}") from exc
        except Exception as exc:
            raise LLMError(f"Groq request failed: {exc}") from exc
        parsed.setdefault("source_ids", [])
        parsed.setdefault("limitations", [])
        parsed.setdefault("next_step", "")
        return self.enforce_source_ids(parsed, {c.source_id for c in chunks})
