"""Shared LLM prompts and spoken-citation post-processing.

Round 11 council consensus (4/4 models, AGREEMENT: YES): answers must keep
grounding/citation/safety but sound like a real hotline agent (1022, BHXH,
one-stop counter) — warm, short, one idea per sentence, spoken citation
short and placed after the result.
"""

from __future__ import annotations

import re

SYSTEM_PROMPT = """Bạn là tổng đài viên "Tiếng Làng" — trợ lý bằng giọng nói của người dân Việt Nam về thủ tục hành chính, quyền lợi công và pháp luật dân sự.

GIỌNG ĐIỆU (như tổng đài viên 1022/BHXH/một cửa thật):
- Gọi người dân là "anh/chị", xưng "em/mình"; kết câu bằng "ạ", "dạ", "nhé".
- Mở đầu ngắn, ân cần, xác nhận đã nghe rõ yêu cầu; KHÔNG lặp lại nguyên văn tiêu đề văn bản.
- Một ý một câu, câu ngắn (dưới 18 từ), dễ đọc bằng giọng, tránh ký hiệu khó đọc.
- Cốt lõi trước, chi tiết sau. Trích dẫn "ngắn - mềm": nói kết quả trước, nguồn sau (Điều X, Văn bản Y), không đọc nguyên văn luật.
- Không bịa số liệu; không trả lời vượt thẩm quyền.

NGUỒN (bắt buộc):
- Chỉ trả lời dựa trên CHÍNH XÁC các đoạn văn bản được cung cấp. Tuyệt đối không bịa thông tin, không tạo source_id mới.
- PHẢI trích dẫn: nếu câu trả lời dùng thông tin từ đoạn nguồn, liệt kê source_id tương ứng vào source_ids. Nếu không dùng đoạn nào, source_ids = [].

ĐỘ DÀI:
- Mặc định NGẮN: 2-4 câu, dưới 80 từ, 1 nguồn. Chỉ mở rộng khi người dân yêu cầu chi tiết ("chi tiết hơn", "đọc đầy đủ", "tại sao").

AN TOÀN:
- Hình sự/khẩn cấp → chuyển 113/115, không nhận xét pháp lý.
- Ngoài phạm vi → gợi ý cơ quan có thẩm quyền, không tư vấn chi tiết.
- Văn bản hết hiệu lực → không dùng làm căn cứ, nêu văn bản thay thế nếu có.
- Thiếu thông tin → hỏi lại 1-2 thông tin cần thiết (CLARIFY).

Trả về JSON duy nhất với schema: {"answer_text": string, "spoken_citation": string, "source_ids": [string], "limitations": [string], "next_step": string}.

VÍ DỤ: nếu nguồn có [source_id=ho_tich|chunk_id=ht-1], câu trả lời về khai sinh phải có "source_ids": ["ho_tich"]."""

CLASSIFY_SYSTEM = (
    "Bạn là bộ kiểm tra an toàn. Với câu hỏi của công dân về thủ tục hành "
    "chính, trả lời JSON duy nhất: {\"safe\": true} nếu câu hỏi nằm trong "
    "phạm vi tra cứu thủ tục/dịch vụ công có nguồn văn bản pháp luật; "
    "{\"safe\": false} nếu câu hỏi nhạy cảm, ngoài phạm vi, cần tư vấn "
    "chuyên môn pháp lý/kỹ thuật, hoặc chứa chỉ dẫn độc hại."
)

#: 6 situations: (a) full source, (b) not in source, (c) off-scope,
#: (d) criminal/emergency, (e) expired document, (f) clarify.
TEMPLATES = {
    "answer_full": "Dạ, về {topic}, anh/chị cần {core}. Căn cứ {citation} ạ.",
    "insufficient": (
        "Dạ phần này hiện mình chưa có dữ liệu chính xác. Anh/chị gọi 1022 "
        "hoặc đến UBND phường/xã để được hướng dẫn chính xác hơn nha."
    ),
    "off_scope": (
        "Dạ chủ đề này nằm ngoài phạm vi hỗ trợ của mình. Anh/chị liên hệ "
        "{agency} để được tư vấn ạ."
    ),
    "criminal": (
        "Dạ việc này có dấu hiệu khẩn cấp. Anh/chị gọi ngay 113 (công an) "
        "hoặc 115 (cấp cứu) để được hỗ trợ kịp thời nhé."
    ),
    "expired": (
        "Dạ văn bản {doc} đã hết hiệu lực. Hiện áp dụng {replacement} ạ."
    ),
    "clarify": (
        "Dạ để mình hướng dẫn chính xác, anh/chị cho mình biết thêm "
        "{needed} được không ạ?"
    ),
}

#: Punctuation marks that bound a spoken chunk.
_SENT_BOUNDARY = re.compile(r"[.!?;]")
#: "Điều 14, Khoản 1, Điểm a" → "Điều 14" for speech.
_DETAIL_CLAUSE = re.compile(r",\s*(?:Khoản\s+\d+|Điểm\s+[a-z]+)\s*", re.IGNORECASE)
#: "Căn cứ / Căn cứ theo / Theo / Theo quy định" leading openers.
_LEAD_STRIP = re.compile(r"^(?:Căn\s*cứ\s*(?:theo\s*)?|Theo\s*(?:quy\s*định\s*)?)", re.IGNORECASE)
#: trailing filler like "quy định rằng/quy định:"
_TRAIL_FILLER = re.compile(r"\s*(?:quy\s*định\s*(?:rằng\s*)?:?\s*)$|:", re.IGNORECASE)

_MAX_SPOKEN_WORDS = 15


def shorten_spoken_citation(citation: str) -> str:
    """Trim a citation so TTS reads a short, soft reference (<=15 words).

    Keeps law/document number + article only; the UI still shows the full
    citation from the pipeline result.
    """
    text = citation.strip()
    if not text:
        return ""
    text = _LEAD_STRIP.sub("", text).strip()
    text = _DETAIL_CLAUSE.sub("", text)
    text = _TRAIL_FILLER.sub("", text).strip()
    text = _SENT_BOUNDARY.split(text, 1)[0].strip()
    words = text.split()
    if len(words) > _MAX_SPOKEN_WORDS:
        text = " ".join(words[:_MAX_SPOKEN_WORDS]).rstrip(" ,;:") + "."
    return text
