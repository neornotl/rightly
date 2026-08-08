"""Groq LLM adapter (optional, lazy import of groq SDK)."""

from __future__ import annotations

import json

from app.llm.base import BaseLLM, LLMError
from app.schemas import RetrievedChunk

_SYSTEM = (
    "Bạn là trợ lý tra cứu thủ tục hành chính có nguồn dẫn chứng (grounded). "
    "Chỉ trả lời dựa trên CHÍNH XÁC các đoạn văn bản được cung cấp. "
    "Tuyệt đối không bịa thông tin, không tạo source_id mới. "
    "PHẢI trích dẫn: nếu câu trả lời dùng thông tin từ đoạn nguồn, liệt kê "
    "source_id tương ứng vào source_ids. Nếu không dùng đoạn nào, source_ids = []. "
    'Trả về JSON duy nhất với schema: '
    '{"answer_text": string, "spoken_citation": string, "source_ids": [string], '
    '"limitations": [string], "next_step": string}.\n\n'
    "VÍ DỤ: nếu nguồn có [source_id=ho_tich|chunk_id=ht-1], câu trả lời về khai "
    'sinh phải có "source_ids": ["ho_tich"].'
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
            f"Giới hạn câu trả lời: {max_chars} ký tự.\n\n"
            "Trả lời theo đúng JSON sau, không thêm chú thích ngoài JSON:\n"
            '{"answer_text": "...", "spoken_citation": "...", '
            '"source_ids": ["source_id đã dùng"], "limitations": ["..."], '
            '"next_step": "..."}'
        )
        client = self._get_client()
        last_error: Exception | None = None
        for attempt in range(3):  # up to 2 retries
            try:
                completion = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": _SYSTEM},
                        {"role": "user", "content": user},
                    ],
                    temperature=0.2,
                    response_format={"type": "json_object"},
                )
                text = completion.choices[0].message.content.strip()
                text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                parsed = json.loads(text)
                break
            except json.JSONDecodeError as exc:
                last_error = exc
                if attempt < 2:
                    continue
                raise LLMError(f"Groq returned non-JSON output: {exc}") from exc
            except Exception as exc:
                last_error = exc
                raise LLMError(f"Groq request failed: {exc}") from exc
        if last_error is not None:
            raise LLMError(f"Groq request failed after retries: {last_error}") from last_error
        parsed.setdefault("source_ids", [])
        parsed.setdefault("limitations", [])
        parsed.setdefault("next_step", "")
        chunk_to_source = {c.chunk_id: c.source_id for c in chunks}
        mapped = [chunk_to_source.get(sid, sid) for sid in parsed.get("source_ids", [])]
        parsed["source_ids"] = mapped
        # NOTE: raw source_ids are deliberately NOT filtered here (F2 fix).
        # The pipeline runs CitationValidator on the raw list so hallucinated
        # citations can be detected, then sanitizes afterwards.
        return parsed
