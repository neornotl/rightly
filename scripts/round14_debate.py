"""Round 14 — council: fit + top-3/top-1 per bracket, SDG primary vote (from form
screenshot read by vision members), and C's bilingual proposal.

3 phases (resumable via --phase N):
  P1 positions : each member gives position on 4 questions + votes ONE SDG.
  P2 critique  : cross-critique + refine consensus (SDG, bilingual, chances).
  P3 ruling    : final ruling + updated probabilities + AGREEMENT.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from council_models import MEMBERS  # noqa: E402

OUT_FILE = "debate_output/round14.json"

VISION = """DỮ LIỆU MỚI TỪ ẢNH (3 thành viên vision: gemini-2.5-flash, nemotron-nano-omni,
minimax-m3 — 3/3 đồng thuận, xem debate_output/vision_round14.json):
- Ảnh là MỘT CÂU HỎI trong Google Form nộp bài của cuộc thi (ảnh chụp phần "Primary SDG").
- Nội dung câu hỏi: "Which of the UN's Sustainable Development Goals (SDGs) aligns best
  with your project/solution? *" — "Primary SDGs (Choose one)" — BẮT BUỘC, chỉ chọn 1.
- 17 lựa chọn: SDG 1 No poverty, 2 Zero hunger, 3 Good health and well-being,
  4 Quality education, 5 Gender equality, 6 Clean water, 7 Affordable clean energy,
  8 Decent work, 9 Industry innovation infrastructure, 10 Reduced inequalities,
  11 Sustainable cities and communities, 12 Responsible consumption, 13 Climate action,
  14 Life below water, 15 Life on land, 16 Peace justice strong institutions,
  17 Partnerships for the goals.
- KHÔNG có trọng số/điểm số/rubric nào trong ảnh — chỉ là 1 câu hỏi chọn 1 SDG.
- Khuyến nghị ban đầu của cả 3 vision member: SDG 3 (Good health and well-being)."""

STATE = f"""TỔNG QUAN DỰ ÁN "TIẾNG LÀNG v4.0" — BÁO CÁO KÍN CHO HỘI ĐỒNG (sau Round 13, ngày 08/08/2026):
- Sản phẩm: voice-first AI tiếng Việt "tổng đài viên ảo" tư vấn thủ tục hành chính/quyền
  lợi công/pháp luật dân sự cho người cao tuổi nông thôn. ASR(PhoWhisper/Mock)→retrieval
  hybrid→SafetyRouter→LLM(Groq/Gemini)→CitationValidator(11 nguồn luật thật)→TTS.
  111 tests xanh, preflight 9/9, smoke real Groq 12/12.
- CUỘC THI CHÍNH THỨC: Intel(R) Vietnam AI Impact Festival 2026 (KHÔNG phải VAIFF!).
  BTC: NIC + SHTP + SHTP-IC + Intel VN. Chủ đề "Enriching Lives with AI Innovation".
  ĐỘI THI BẢNG HỌC SINH 13-17 (xác nhận 08/08) — nhóm ≤3 học sinh THCS/THPT/CĐ nghề.
  Hồ sơ = Google Form: tên ≤10 từ + mô tả ≤150 từ + video ≤2 phút + consent có chữ ký
  người có thẩm quyền (thí sinh <18 → phụ huynh/giám hộ). Hạn nộp 25/08/2026.
- GIẢI (xác nhận chính thức): Top 3 xét THEO TỪNG BẢNG (3 giải/bảng; bảng Học sinh có
  3 vé riêng, không cạnh tranh với bảng Sinh viên). Top 1 THEO TỪNG BẢNG → 1 đội/bảng
  đại diện VN dự Intel AI Global Impact Festival 2026 (2 đội VN đi global).
  Mỗi thành viên đội thắng: GCN + 13.000.000 đ.
- RUBRIC 50Đ (PDF "Evaluation Rubrics for VAIIF26"): M1 Impact&Inclusion 15đ, M2 AI
  Innovation 20đ, M3 Technical 15đ. Ethical AI Guidelines Intel 9 nguyên tắc.
- ĐỘI THẮNG NĂM NGOÁI (PDF chính thức SHTP-IC "Vietnam AI Impact Festival 2025"):
  2025 Global: Your Voice (ĐH Lạc Hồng, dịch ngôn ngữ ký hiệu, 2,5 triệu người, SDG 4).
  2025 Country (bảng 13-17): Hap (kính thông minh + YOLOv8 + OpenVINO, màn hình-free,
  offline, SDG 3) → sau đó thắng Regional Award Global 2025.
  2024 Country: AERO ResQ (drone cứu nạn, SDG 11), S-REC (tuyển dụng AI, SDG 8).
  Pattern: accessibility/cộng đồng 2 năm liền + hardware/OpenVINO mạnh ở bảng 13-17
  + SDG ghi rõ + số liệu tác động lớn.
- Ước lượng cơ hội (fit_assessment_aiif26.md §7): Top 3 bảng Học sinh 25-40% hôm nay
  → 45-60% nếu Top-12 đúng hạn; Top 1 bảng 8-15% → 20-30%.
- Round 13 đã chốt Top-12 hành động (video 2' storyboard Bà Năm, pilot thật, public
  link 12/08, corpus luật thật, 150 từ lock 11/08, SDG map, consent, sweep 22-24/08).
- ĐỀ XUẤT MỚI CỦA C: làm HỒ SƠ SONG NGỮ (150 từ tiếng Việt + tiếng Anh? video phụ đề
  2 ngôn ngữ? UI tiếng Việt là chính) — chưa được hội đồng bàn.

{VISION}

CÂU HỎI HỘI ĐỒNG ROUND 14 (họp kín):
1) TOP 3 / TOP 1 THEO BẢNG: với việc đã xác nhận Top 3 và Top 1 đều xét THEO TỪNG BẢNG
   (bảng Học sinh 13-17 có 3 vé riêng, đội mình KHÔNG cạnh tranh với Sinh viên), đánh
   giá lại: (a) xác suất vào Top 3 bảng Học sinh hôm nay và sau khi xong Top-12; (b) xác
   suất Top 1 bảng (vé đi Global) hôm nay và sau Top-12; (c) 3 yếu tố quyết định nhất
   để thắng bảng này dựa trên pattern đội thắng năm ngoái (đặc biệt Hap 13-17).
2) VOTE SDG PRIMARY (bắt buộc chọn DUY NHẤT 1 trong 17): bạn chọn SDG nào cho dự án và
   tại sao (xét cả rubric M1 "SDG map 1đ", narrative đội thắng năm ngoái, và đối tượng
   người cao tuổi nông thôn). Chỉ được chọn 1. Kết thúc phần này bằng dòng: VOTE SDG: <số>.
3) ĐỀ XUẤT SONG NGỮ CỦA C: nên làm gì trong 17 ngày — (a) 150 từ song ngữ Việt-Anh khi
   nộp form (form hỏi bằng tiếng Anh, video 2' cần phụ đề tiếng Việt hay tiếng Anh?),
   (b) tác động lên điểm rubric (video tiếng Việt hay tiếng Anh lợi hơn cho hội đồng
   chấm là người VN + Intel?), (c) chi phí người-ngày, (d) rủi ro claim/consent khi
   dịch. Kết luận: song ngữ ở mức nào (form tiếng Anh + video phụ đề song ngữ? UI giữ
   tiếng Việt?) và ai làm gì.
4) RÀ SOÁT TÊN CUỘC THI: nhắc lại 1 lần nữa — cuộc thi là Intel Vietnam AI Impact
   Festival 2026, KHÔNG phải VAIFF. Mọi hồ sơ/narrative/trả lời của bạn từ giờ phải
   dùng đúng tên. Nếu bạn từng viết "VAIFF" trong các round trước, ghi nhận và cam kết
   dùng đúng tên.
Trả lời tối đa 1000 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_P2_HEADER = """BÁO CÁO KÍN — PHIÊN 2 (PHẢN BIỆN + HỘI TỤ):
Đã nhận 5 ý kiến vòng 1 (dán bên dưới, gồm cả VOTE SDG của từng người). YÊU CẦU:
1) Phản biện 2 luận điểm YẾU/QUÁ LẠC QUAN/THIẾU CĂN CỨ của các thành viên khác
   (top3/top1, SDG, song ngữ) — chỉ rõ ai nói gì.
2) Công nhận 1 luận điểm HỢP LÝ của MỖI thành viên.
3) VOTE SDG CẬP NHẬT: sau khi xem các lựa chọn khác, giữ hay đổi? Kết thúc bằng dòng
   VOTE SDG: <số>.
4) Chốt khuyến nghị SONG NGỮ của bạn sau khi nghe phản biện (giữ/thu hẹp/bỏ — mức độ nào).
Trả lời tối đa 800 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

_P3_HEADER = """BÁO CÁO KÍN PHIÊN 3 (PHÁN QUYẾT CUỐI):
Đã nhận 5 ý kiến phiên 2 (dán bên dưới). YÊU CẦU:
1) Với MỖI ý kiến phiên 2: HỢP LÝ / MỘT PHẦN / KHÔNG HỢP LÝ + 1 dòng lý do.
2) PHÁN QUYẾT SDG: chốt DUY NHẤT 1 SDG cho form + lý do cuối. Dòng: VOTE SDG: <số>.
3) PHÁN QUYẾT SONG NGỮ: chốt mức song ngữ (form/video/UI), người làm, deadline,
   ngày-người chi phí.
4) XÁC SUẤT CHỐT: Top 3 bảng Học sinh và Top 1 bảng — hôm nay và sau Top-12 (%). 3 yếu
   tố quyết định thắng bảng này.
5) 1 dòng "dòng đỏ" (điều tệ nhất nếu làm sai) + 1 câu slogan.
Trả lời tối đa 800 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

SYSTEM = (
    "Bạn là thành viên hội đồng chiến lược của dự án 'Rightly' (voice-first "
    "AI tiếng Việt cho người cao tuổi; thi Intel Vietnam AI Impact Festival 2026 — "
    "KHÔNG phải VAIFF — bảng Học sinh 13-17, hạn 25/08). Bạn THIỆN THỰC, định lượng, "
    "không nể nang; đề xuất KHẢ THI (người-day, rủi ro), ưu tiên ROI. Tiếng Việt."
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
        blocks.append(f"\n=== {m['display']} ===\n{t[:2200]}")
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
    return {"round": 14, "date": "2026-08-08", "state": STATE}


def save(d):
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)


def main():
    phase = int(sys.argv[sys.argv.index("--phase") + 1]) if "--phase" in sys.argv else 1
    key = f"phase{phase}"
    d = load()
    d.setdefault(key, {})
    prompt = _build(phase, d)
    max_tokens = {1: 6500, 2: 5200, 3: 5200}[phase]
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
