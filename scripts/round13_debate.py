"""Round 13 — council: breakaway transformations to maximize VAIIF26 score.

3 phases (resumable via --phase N):
  P1 ideas    : each member proposes up to 8 concrete changes (score ROI).
  P2 critique : each member reviews others' ideas, flags weak ones, ranks top.
  P3 plan     : final consolidated action plan + point target + AGREEMENT.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from council_models import MEMBERS  # noqa: E402

OUT_FILE = "debate_output/round13.json"

STATE = """TỔNG QUAN DỰ ÁN "TIẾNG LÀNG v4.0" — BÁO CÁO KÍN CHO HỘI ĐỒNG (sau Round 12, ngày 08/08/2026):
- Sản phẩm: voice-first AI tiếng Việt, "tổng đài viên ảo" tư vấn thủ tục hành chính/quyền lợi công/pháp luật dân sự cho người cao tuổi, nông thôn, ít kỹ năng số. Hình sự/khẩn cấp chuyển 113/115. ASR(PhoWhisper/Mock)→retrieval hybrid BM25+dense→SafetyRouter→LLM(Groq/Gemini, cloud-first)→CitationValidator(11 nguồn luật thật, chặn văn bản hết hiệu lực)→TTS. CLI+Streamlit. 111 tests xanh, ruff sạch, preflight 9/9, smoke real Groq 12/12, Round 11 đã chuẩn hóa giọng tổng đài viên (trích dẫn đọc ≤15 từ).

CUỘC THI CHÍNH THỨC (đã xác minh web 08/08/2026, xem docs/competition_aiif26.md):
- Tên: Intel(R) Vietnam AI Impact Festival 2026 — bảng "AI Changemakers" (Học sinh 13-17 / Sinh viên 18+, nhóm ≤3). BTC: NIC + SHTP + SHTP-IC + Intel VN. Chủ đề: "Enriching Lives with AI Innovation".
- HỒ SƠ NỘP QUA GOOGLE FORM DUY NHẤT (không có PDF thuyết minh): tên dự án ≤10 từ; mô tả ≤150 từ; VIDEO/VLOG ≤2 PHÚT; mẫu consent có chữ ký người có thẩm quyền. Hạn: 25/08/2026.
- Giải: 3 đội xuất sắc nhất mỗi bảng, mỗi thành viên 13 triệu + GCN; đội hạng cao nhất mỗi bảng đại diện VN dự Intel AI Global Impact Festival 2026.
- RUBRIC CHÍNH THỨC 50 ĐIỂM (PDF "Evaluation Rubrics for VAIIF26" — đã đọc đầy đủ):
  M1 "Enriching Lives: Impact & Inclusion" 15đ: problem statement rõ (2) + bằng chứng vấn đề/citation (1) + target audience rõ (2) + UX equivalent cho mọi người (1) + gỡ rào cản cho người khuyết tật (1) + khả thi tài chính (1) + offline/low-bandwidth (1) + đa ngôn ngữ/đa phương thức (1) + tác động xã hội rõ (1) + AI tạo tác động vượt software truyền thống (1) + SDG map (1) + môi trường (1) + đường bền vững (1).
  M2 "AI Innovation: Application & Implementation" 20đ: không force-fit AI (1) + AI là công nghệ chính (2) + ý tưởng mới/original (3) + thể hiện tri thức kỹ năng AI (2) + dữ liệu thu thập & phân tích rõ (1) + giải trình chọn dữ liệu (1) + đạo đức AI (1) + quyền riêng tư (1) + giảm bias (1) + môi trường (1) + prototype chạy (1) + triển khai: chưa test/test/public link (2) + GTM/deployment strategy (1).
  M3 "Technical Knowledge and Skills" 15đ: tech stack rõ (2) + hardware: không đề/desktop/AI PC hoặc tương đương/components chuyên biệt (0-3) + software: no-code/1 chương trình/nhiều chương trình+API (0-3) + UI: code only/low-code/template/custom (0-3) + emerged AI: không/truncated/advanced package/Gen AI+Agents+RAG+multimodal (0-4).
- Ethical AI Guidelines chính thức (9 nguyên tắc Intel): môi trường, công bằng-giảm bias, privacy, minh bạch-giải thích được, an toàn, human oversight, nhân quyền, data integrity, không đạo văn + ghi credit. Intel kiểm tra AI ethics trước khi trao giải quốc tế (năm 2025: VN thắng 6 giải Global/Regional; "Your Voice" ĐH Lạc Hồng - AI vì cộng đồng).

TỰ CHẤM HIỆN TẠI (hội đồng Round 6: ~36-42/50; MỤC TIÊU ≥45/50, tối đa khả thi 48):
- M1 mục tiêu 13/15: đủ về kỹ thuật; thiếu problem statement 150 từ + SDG map + số liệu thật + testimony người dùng.
- M2 mục tiêu 18/20: thiếu public link có người dùng (+2), GTM evidence (thư quan tâm) (+1-2).
- M3 mục tiêu 14/15: có tech stack/software/UI custom/emerged AI; thiếu AI PC/OpenVINO (không có máy → ghi limitation, giữ desktop 1-2đ).
- Đã có: threat model, privacy (PII scrubber outbound, retention 30 ngày, không lưu transcript), demo deterministic + watermark, R1-R4 eval, naturalness prompt, 11 nguồn luật thật, docs đầy đủ.
- Đang thiếu: (1) pilot người thật + testimony + 1-2 user ngoài đội qua public link; (2) WER/MOS trên ≥30-50 mẫu giọng thật; (3) public link ổn định (chờ xoay key Groq + deploy); (4) corpus luật trọng điểm 25-30+ văn bản thay corpus demo "xã Bình Minh"; (5) GTM thư quan tâm UBND xã/Hội NCT; (6) VIDEO 2 PHÚT (đây là bài dự thi chính!); (7) consent mẫu đúng yêu cầu form.
- Kim cảnh: 17 ngày (08/08→25/08). Nguồn lực: T (code ngày đêm), C (content/compliance/video), P (pilot/partnership/video).

CÂU HỎI HỘI ĐỒNG ROUND 13 (họp kín — đề xuất "biến đổi" để ăn giải, không bó tay vì kiến trúc cũ):
1) Đề xuất TỐI ĐA 8 "BIẾN ĐỔI" khả thi (chức năng/thardware/quy trình/narrative/hồ sơ/video) từ trạng thái hiện tại để đạt điểm CAO NHẤT có thể (hướng 45-48/50). Mỗi ý: (a) tên, (b) mô tả 2-3 dòng, (c) tham số rubric cụ thể bị tác động (+X/50, khu M1/M2/M3 + tên tham số), (d) chi phí (người-day), (e) rủi ro chính, (f) thứ tự ưu tiên. Ưu tiên các ý "phi-code" (giấy tờ, kể chuyện, video 2 phút, hồ sơ nộp, tổ chức pilot, số điện thoại thật xác minh) — không chỉ feature code. NHỚ: bài dự thi = 150 từ + video 2 phút, mọi điểm rubric phải "lộ" trong đó.
2) Chỉ rõ ý nào là "vàng" (ROI cao, rủi ro thấp) làm TRƯỚC trong 7 ngày đầu (08-15/08), ý nào cắt.
3) Dự đoán điểm sau khi hoàn thành top-5 ý: X/50? Lỗ trống gì không kịp?
Trả lời tối đa 950 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_P2_HEADER = """BÁO CÁO KÍN — PHIÊN 2 (PHẢN BIỆN + ƯU TIÊN HÓA):
Đã nhận 5 danh sách đề xuất "biến đổi" (dán bên dưới). YÊU CẦU:
1) Chỉ ra 2-3 đề xuất của các thành viên khác mà bạn cho là YẾU/PHI THỰC TẾ/KHÔNG ĐỔI ĐIỂM — phản biện lý thuyết logic + đề xuất thay thế.
2) Ghi nhận 1 đề xuất "bất ngờ" tốt nhất của MỖI thành viên.
3) Chốt BẢNG XẾP HẠNG chung TOP-10 (ưu tiên tuyệt đối, real ranking) dựa trên tổng hợp 5 danh sách: [thứ tự | ý biến đổi | +điểm ước | ngày-người | ai làm (T/C/P)] — có giải trình ngắn vị trí.
Trả lời tối đa 800 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_P3_HEADER = """BÁO CÁO KÍN PHIÊN 3 (PHÁN QUYẾT CUỐI):
Đã nhận 5 bảng xếp hạng (dán bên dưới). YÊU CẦU:
1) Với MỖI bảng xếp hạng của đồng nghiệp: đánh giá HỢP LÝ / MỘT PHẦN / KHÔNG HỢP LÝ + 1 dòng lý do.
2) Hợp nhất thành TOP (max 12 dòng): thứ tự TUYỆT ĐỐI, người làm, điểm tăng, deadline từng nhóm.
3) Tổng điểm dự kiến SAU khi xong top-12 (X/50) + "dòng đỏ" (điều tệ nhất có thể xảy ra nếu không làm).
4) 1 câu slogan chốt chiến lược tổng.
Trả lời tối đa 700 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

SYSTEM = (
    "Bạn là thành viên hội đồng chiến lược của dự án 'Rightly' (voice-first "
    "AI tiếng Việt, thi Intel Vietnam AI Impact Festival 2026 (VAIIF26), hạn 25/08). Bạn THIỆN THỰC, định lượng, không nể nang; "
    "đề xuất phải KHẢ THI trên thực tế (người-day, rủi ro), ưu tiên ROI. Tiếng Việt."
)


def _build(phase: int, data: dict) -> str:
    if phase == 1:
        return STATE
    if phase == 2:
        blocks = [_P2_HEADER]
        for m in MEMBERS:
            t = data.get("phase1", {}).get(m["display"], "[chưa có]")
            blocks.append(f"\n=== {m['display']} ===\n{t[:2600]}")
        return "\n".join(blocks)
    blocks = [_P3_HEADER]
    for m in MEMBERS:
        t = data.get("phase2", {}).get(m["display"], "[chưa có]")
        blocks.append(f"\n=== {m['display']} (TOP-10) ===\n{t[:2000]}")
    return "\n".join(blocks)


def call_model(member, user_text, max_tokens):
    key = os.environ.get(member["key_env"]) if member["key_env"] else None
    body = {
        "model": member["model"],
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user_text}],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    headers.update(member.get("headers_extra") or {})
    data = json.dumps(body).encode("utf-8")
    last = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(member["url"], data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            return payload["choices"][0]["message"]["content"].strip()
        except Exception as exc:  # noqa: BLE001
            last = exc
            print(f"  [{member['display']}] att {attempt}: {exc}")
    raise RuntimeError(f"{member['display']} failed: {last}")


def load():
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"round": 13, "date": "2026-08-08", "state": STATE}


def save(d):
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)


def main():
    phase = int(sys.argv[sys.argv.index("--phase") + 1]) if "--phase" in sys.argv else 1
    key = f"phase{phase}"
    d = load()
    d.setdefault(key, {})
    prompt = _build(phase, d)
    max_tokens = {1: 6000, 2: 5000, 3: 5000}[phase]
    for m in MEMBERS:
        if d[key].get(m["display"]):
            print(f"skip {m['display']}")
            continue
        print(f"== [{phase}] {m['display']} ...")
        sys.stdout.flush()
        try:
            d[key][m["display"]] = call_model(m, prompt, max_tokens)
        except Exception as exc:  # noqa: BLE001
            d[key][m["display"]] = f"[ERROR] {exc}"
        save(d)
    print("Saved ->", OUT_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
