"""Round 15 — council: what would ACTUALLY push Top 3 >80% and Top 1 >50%.

3 phases (resumable via --phase N):
  P1 boosters : each member proposes high-leverage boosters + adjusted odds.
  P2 critique : cross-critique, kill pipe dreams, rank boosters by ROI.
  P3 ruling   : final booster list (who/deadline/cost/points) + honest ceiling.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from council_models import MEMBERS  # noqa: E402

OUT_FILE = "debate_output/round15.json"

STATE = """TỔNG QUAN DỰ ÁN "TIẾNG LÀNG v4.0" — BÁO CÁO KÍN CHO HỘI ĐỒNG (sau Round 14, ngày 08/08/2026):
- Sản phẩm: voice-first AI tiếng Việt "tổng đài viên ảo" tư vấn thủ tục hành chính/
  quyền lợi công/pháp luật dân sự cho người cao tuổi nông thôn. ASR(PhoWhisper/Mock)
  →retrieval hybrid→SafetyRouter→LLM(Groq/Gemini)→CitationValidator(11 nguồn luật
  thật)→TTS. CLI+Streamlit. 111 tests xanh, preflight 9/9, smoke real Groq 12/12.
- CUỘC THI: Intel(R) Vietnam AI Impact Festival 2026 (VAIIF26, KHÔNG phải VAIFF).
  BTC NIC+SHTP+SHTP-IC+Intel VN. ĐỘI THI BẢNG HỌC SINH 13-17, nhóm ≤3, consent
  phụ huynh. Hồ sơ = Google Form: tên ≤10 từ + 150 từ (EN) + video 2' (giọng VN +
  phụ đề EN) + consent. Hạn 25/08/2026. Top 3 = 3 vé RIÊNG của bảng Học sinh;
  Top 1 bảng = 1 đội/bảng đi Intel AI Global Impact Festival 2026.
- RUBRIC 50Đ: M1 Impact&Inclusion 15đ, M2 AI Innovation 20đ, M3 Technical 15đ.
  Ethical AI Guidelines Intel 9 nguyên tắc (kiểm tra trước khi trao giải quốc tế).
- ĐỘI THẮNG NĂM NGOÁI: 2025 Global: Your Voice (SV, dịch ngôn ngữ ký hiệu, 2,5tr
  người, SDG 4). 2025 Country (13-17): Hap (kính thông minh + YOLOv8 + OpenVINO,
  offline, SDG 3) → Regional Award Global 2025. 2024: AERO ResQ (drone cứu nạn),
  S-REC. Pattern: accessibility + hardware/OpenVINO mạnh ở 13-17 + SDG rõ + số
  liệu tác động lớn.
- PHÁN QUYẾT R14: SDG 16 (Peace/Justice/Institutions, target 16.3/16.10); song
  ngữ thu hẹp (form EN, video phụ đề EN, UI VN); cắt OpenVINO thật (scope creep
  ROI âm); xác suất chốt: Top 3 bảng: 30-35% hôm nay → 45-55% sau Top-12; Top 1
  bảng: 8-15% → 18-25%.
- TOP-12 R13 đang chạy: pilot thật ≥5-7 NCT (13/08), video Bà Năm (16/08), public
  link Streamlit + 3 key Groq xoay (12/08), corpus luật trọng điểm 15-30 văn bản
  (13/08), 150 từ EN + SDG 16 (11/08), consent chuẩn (12/08), GTM mềm LOI/email
  (18/08), Technical Rigor WER/MOS trên VIVOS 760 wav (14/08), ethical 1 trang
  (15/08), sweep hồ sơ (22-24/08), nộp (25/08). Freeze feature 13/08.
- NGUỒN LỰC 17 NGÀY: T (code), C (content/compliance/video), P (pilot/partnership/
  video). Không có máy AI PC. Có thể liên hệ BTC (thi.theu.nguyen@intel.com).
- BỐI CẢNH CẠNH TRANH 13-17: ước 50-150 bài toàn quốc; các đội thường là trường
  chuyên, có thầy kèm, video chuyên nghiệp, vài đội có hardware; Hap-style
  OpenVINO mỗi năm có 1-2 đội. Giám khảo = người VN + Intel.

CÂU HỎI HỘI ĐỒNG ROUND 15 (họp kín — MỤC TIÊU THÁCH THỨC):
1) MỤC TIÊU: đẩy xác suất **Top 3 bảng Học sinh >80%** và **Top 1 bảng >50%**.
   Đánh giá thành thật: (a) hai mục tiêu này có THỰC TẾ đạt được trong 17 ngày
   không? (b) trần trung thực (honest ceiling) của từng mục tiêu là bao nhiêu %?
2) BOOSTER (đòn bẩy thực): đề xuất tối đa 6 BOOSTER khả thi VƯỢT mặt bằng Top-12
   hiện tại, mỗi ý: (a) tên, (b) mô tả 2-3 dòng, (c) tác động rubric cụ thể (+Xđ),
   (d) tác động lên xác suất Top 3/Top 1 (+X%?), (e) chi phí (người-ngày + tiền
   nếu có, ví dụ SĐT thật ~200k, thuê máy, phí), (f) rủi ro, (g) ai làm + deadline.
   GỢI Ý các hướng (không giới hạn, hãy chọn ít nhất 1 trong mỗi nhóm):
   - HARDWARE/EDGE: liên hệ BTC Intel xin mượn AI PC/NUC + OpenVINO path thật
     (ASR int8 + LLM nhỏ) để demo offline live; thuê/mượn laptop có NPU.
   - TRIỂN KHAI THẬT: SĐT tổng đài thật (SIM + Zalo OA) cho pilot; Streamlit
     paid tier bỏ sleep; tích hợp Zalo để người thật dùng theo giọng.
   - BẰNG CHỨNG QUY MÔ: pilot 15-30 phiên + đa vùng (Bắc/Trung/Nam) + 1 số liệu
     định lượng (task success %, thời gian tiết kiệm, satisfaction) có nguồn;
     WER/MOS trên 760 wav VIVOS + 20 phiên pilot.
   - GTM CHÍNH THỨC: thư xác nhận quan tâm từ UBND xã/Hội NCT/BHXH huyện (đóng
     dấu), email BTC; 1-2 user ngoài đội dùng public link thật.
   - VIDEO WOW: quay pilot thật tại xã (không diễn), chất lượng dựng chuyên
     nghiệp (thuê editor?), trailer 15s cho mạng xã hội, phụ đề EN.
   - NARRATIVE/DIFFERENTIATION: "tổng đài 1022 không làm được gì mà Tiếng Làng
     làm" — demo so sánh trực tiếp; câu chuyện Bà Năm xúc động thật.
3) XÁC SUẤT CẬP NHẬT SAU BOOSTER: sau khi chọn top-3 booster, Top 3 và Top 1 là
   bao nhiêu %? Mục tiêu >80% và >50% có chạm được không, hay phải đặt lại kỳ vọng?
4) 2 VIỆC ĐẦU TIÊN ngay sáng 09/08 để kích hoạt booster (ai làm gì).
Trả lời tối đa 1100 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_P2_HEADER = """BÁO CÁO KÍN — PHIÊN 2 (PHẢN BIỆN + HỘI TỤ BOOSTER):
Đã nhận 5 danh sách booster (dán bên dưới). YÊU CẦU:
1) Phản biện 2-3 booster YẾU/KHÔNG KHẢ THI/ĐÁNH GIÁ QUÁ CAO của các thành viên khác
   (chỉ rõ ai nói gì, định lượng lý do — người-ngày, rủi ro, xác suất ảo).
2) Công nhận 1 booster "bất ngờ tốt" của MỖI thành viên.
3) Chốt BẢNG XẾP HẠNG TOP-6 booster (thứ tự tuyệt đối theo ROI): [stt | booster |
   +điểm rubric | +% Top 3 | +% Top 1 | người-ngày+tiền | ai | deadline].
4) TRẦN TRUNG THỰC của bạn: Top 3 max bao nhiêu %? Top 1 max bao nhiêu %? Có nên
   đặt mục tiêu >80% / >50% hay điều chỉnh kỳ vọng (bao nhiêu)?
Trả lời tối đa 900 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

_P3_HEADER = """BÁO CÁO KÍN PHIÊN 3 (PHÁN QUYẾT CUỐI — BOOSTER PLAN):
Đã nhận 5 bảng xếp hạng (dán bên dưới). YÊU CẦU:
1) Với MỖI bảng xếp hạng của đồng nghiệp: HỢP LÝ / MỘT PHẦN / KHÔNG HỢP LÝ + 1 dòng.
2) TOP-6 BOOSTER HỢP NHẤT (tuyệt đối): người làm, người-ngày+tiền, deadline, +điểm.
3) XÁC SUẤT CHỐT: Top 3 bảng và Top 1 bảng — (a) sau Top-12 R13 (b) sau booster.
   Trần trung thực của từng mục tiêu. Mục tiêu >80% / >50%: giữ, hạ, hay thay bằng
   mục tiêu thực tế (nêu con số).
4) 2 hành động 09/08 sáng + 2 hành động 09/08 chiều (ai làm).
5) 1 dòng "dòng đỏ" + 1 slogan.
Trả lời tối đa 900 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

SYSTEM = (
    "Bạn là thành viên hội đồng chiến lược của dự án 'Rightly' (voice-first "
    "AI tiếng Việt cho người cao tuổi; thi Intel Vietnam AI Impact Festival 2026 — "
    "KHÔNG phải VAIFF — bảng Học sinh 13-17, hạn 25/08). Bạn THIỆN THỰC, định lượng, "
    "không nể nang, bác bỏ luận điểm ảo; ưu tiên ROI thực (người-ngày, tiền, rủi ro). "
    "Tiếng Việt."
)


def _build(phase: int, data: dict) -> str:
    if phase == 1:
        return STATE
    if phase == 2:
        blocks = [_P2_HEADER]
        for m in MEMBERS:
            t = data.get("phase1", {}).get(m["display"], "[chưa có]")
            blocks.append(f"\n=== {m['display']} ===\n{t[:2800]}")
        return "\n".join(blocks)
    blocks = [_P3_HEADER]
    for m in MEMBERS:
        t = data.get("phase2", {}).get(m["display"], "[chưa có]")
        blocks.append(f"\n=== {m['display']} ===\n{t[:2400]}")
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
    return {"round": 15, "date": "2026-08-08", "state": STATE}


def save(d):
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)


def main():
    phase = int(sys.argv[sys.argv.index("--phase") + 1]) if "--phase" in sys.argv else 1
    key = f"phase{phase}"
    d = load()
    d.setdefault(key, {})
    prompt = _build(phase, d)
    max_tokens = {1: 7000, 2: 5800, 3: 5800}[phase]
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
