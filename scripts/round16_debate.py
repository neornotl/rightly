"""Round 16 — council ruling on the team lead's "product-first" proposal (09/08).

3 phases (resumable via --phase N):
  P1 analysis   : each member assesses product-first vs parallel; product gaps.
  P2 critique   : cross-critique, rank gaps by ROI, propose revised schedule.
  P3 ruling     : accept/reject product-first; tonight checklist with hours.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from council_models import MEMBERS  # noqa: E402

OUT_FILE = "debate_output/round16.json"

STATE = """TỔNG QUAN DỰ ÁN "TIẾNG LÀNG v4.0" — BÁO CÁO KÍN CHO HỘI ĐỒNG (sau Round 15, sáng 09/08/2026):
- Sản phẩm: voice-first AI tiếng Việt "tổng đài viên ảo" tư vấn thủ tục hành chính/
  quyền lợi công/pháp luật dân sự cho người cao tuổi nông thôn. ASR(PhoWhisper/Mock)
  →retrieval hybrid→SafetyRouter→LLM(Groq/Gemini)→CitationValidator(11 nguồn luật
  thật)→TTS. CLI+Streamlit. 111 tests xanh, preflight 9/9, smoke real Groq 12/12.
- HIỆN TRẠNG SẢN PHẨM 09/08: pipeline chạy nội bộ (dev máy), Streamlit chưa deploy
  public ổn định, chưa voice FAQ, corpus trọng điểm 15-30 văn bản luật đang làm,
  key Groq chưa xoay, chưa tích hợp SĐT/Zalo, chưa OpenVINO path, chưa script log
  WER/MOS. T là người duy nhất code (C: content/compliance, P: pilot/partnership).
- ĐỀ XUẤT CỦA ĐỘI TRƯỞNG (cần hội đồng phán quyết): "TRƯỚC HẾT, HOÀN THIỆN SẢN
  PHẨM CHO DÙNG ĐƯỢC ĐÃ — mấy vụ mượn máy/pilot/quay video nên ĐỢI SẢN PHẨM XONG
  rồi làm sẽ TỐT HƠN. Hôm nay (09/08) T + hội đồng hoàn thiện sản phẩm luôn."
- CUỘC THI: Intel(R) Vietnam AI Impact Festival 2026 (VAIIF26, nội bộ). BTC
  NIC+SHTP+SHTP-IC+Intel VN. ĐỘI THI BẢNG HỌC SINH 13-17, nhóm ≤3, consent phụ
  huynh. Hồ sơ = Google Form: tên ≤10 từ + 150 từ (EN) + video 2' (giọng VN + phụ
  đề EN) + consent. Hạn 25/08/2026. Top 3 = 3 vé RIÊNG bảng Học sinh; Top 1 bảng
  = 1 đội đi Intel AI Global Impact Festival 2026.
- RUBRIC 50Đ: M1 Impact&Inclusion 15đ, M2 AI Innovation 20đ, M3 Technical 15đ.
  Ethical AI Guidelines Intel 9 nguyên tắc.
- PHÁN QUYẾT R13-R15: SDG 16 (16.3/16.10); song ngữ thu hẹp (form EN, video phụ
  đề EN, UI VN); Top-12 hành động (pilot thật, video, 150 từ, consent, GTM mềm,
  Technical Rigor, ethical, sweep); TOP-6 BOOSTER R15: (1) pilot 20-30 NCT + KPI
  (18/08), (2) video Bà Năm không diễn (16/08), (3) SĐT thật + Zalo OA (13/08),
  (4) Intel AI PC/NUC loan + OpenVINO (email 09/08, trả lời 12/08), (5) LOI
  UBND/Hội NCT đóng dấu (14/08), (6) A/B demo 1022 vs Rightly (15/08).
  Xác suất chốt R15: Top 3 bảng 65-75% (mục tiêu 70-75%), Top 1 bảng 28-40%
  (mục tiêu 35-40%) sau booster — >80%/>50% KHÔNG thực tế.
- LỊCH HIỆN TẠI: 09/08 sáng: P email Intel loan + LOI UBND, C kịch bản; chiều:
  C quay video pilot lên xã, T SIM/Zalo + OpenVINO path. 12/08 deploy public.
  13/08 pilot 5-7 người + SĐT/Zalo live + freeze feature. 14/08 Technical Rigor
  + LOI đóng dấu. 16/08 video RENDER. 18/08 pilot 20-30 XONG. 25/08 nộp.
- NGUỒN LỰC: 17 ngày, T code 1 mình; P+C đang chờ sản phẩm để demo/pilot thật.
  Không máy AI PC; có thể liên hệ BTC (thi.theu.nguyen@intel.com).

CÂU HỎI HỘI ĐỒNG ROUND 16 (họp kín — PHÁN QUYẾT CHIẾN LƯỢC "PRODUCT-FIRST"):
1) ĐỀ XUẤT ĐỘI TRƯỞNG: "hoàn thiện sản phẩm dùng được ĐÃ rồi mới pilot/mượn máy/
   quay video — hôm nay T + hội đồng hoàn thiện sản phẩm luôn". Đánh giá thành
   thật: (a) đồng ý/không đồng ý + lý do định lượng; (b) so sánh 2 phương án:
   PRODUCT-FIRST (dồn T vào sản phẩm hôm nay, pilot/video/mượn máy dời sau) vs
   SONG SONG (T làm sản phẩm, P/C vẫn chạy pilot/LOI/video độc lập hôm nay) —
   phương án nào giữ được mốc 13/08 pilot, 16/08 video, 25/08 nộp? Rủi ro mỗi
   phương án (mất ngày, chậm tuyển pilot, video thiếu cảnh thật)?
2) "HOÀN THIỆN SẢN PHẨM" nghĩa là gì: liệt kê tối đa 8 gap CỤ THỂ còn thiếu để
   sản phẩm "dùng được đã" (ví dụ: deploy public + backup link, xoay key Groq,
   voice FAQ, corpus trọng điểm 15-30 văn bản, script log WER/MOS, tích hợp
   SĐT/Zalo, OpenVINO path, UX giọng cho NCT, chống fail khi nhiều người dùng,
   privacy khi deploy public) — với MỖI gap: ước lượng giờ, có CHẶN mốc nào
   không (pilot 13/08 / video 16/08 / nộp 25/08), gap nào làm TRƯỚC theo ROI.
3) LỊCH SỬA: nếu chốt product-first hôm nay, đề xuất LỊCH 09-13/08 mới (ai làm
   gì) KHÔNG phá mốc 13/08 pilot thật + 16/08 video + 18/08 pilot 20-30. Mượn
   máy Intel/LOI/video nên dời hay vẫn chạy song song?
4) PHÁN QUYẾT: chấp nhận đề xuất product-first (với điều kiện gì) hay bác bỏ?
   Ai làm gì TỐI NAY 09/08 (checklist 3-5 việc có giờ ước lượng).
Trả lời tối đa 1100 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_P2_HEADER = """BÁO CÁO KÍN — PHIÊN 2 (PHẢN BIỆN + HỘI TỤ):
Đã nhận 5 phân tích (dán bên dưới). YÊU CẦU:
1) Phản biện 2-3 luận điểm YẾU của các thành viên khác (chỉ rõ ai nói gì, định
   lượng: giờ, người-ngày, rủi ro phá mốc, xác suất ảo).
2) Công nhận 1 điểm "bất ngờ đúng" của MỖI thành viên.
3) Chốt BẢNG XẾP HẠNG tối đa 6 product-gap ưu tiên làm TRƯỚC hôm nay:
   [stt | gap | giờ | chặn mốc nào (13/08, 16/08, 25/08)? | ai | nên làm hôm nay?].
4) QUYẾT ĐỊNH PHƯƠNG ÁN: product-first tối nay (chỉ T code) vs song song
   (T code + P/C vẫn chạy pilot/LOI/video) — chọn cái nào, vì sao? P/C có thể
   làm gì TỐI NAY không phụ thuộc sản phẩm (tuyển pilot, xin LOI, kịch bản)?
Trả lời tối đa 900 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

_P3_HEADER = """BÁO CÁO KÍN PHIÊN 3 (PHÁN QUYẾT CUỐI — PRODUCT-FIRST):
Đã nhận 5 bảng xếp hạng (dán bên dưới). YÊU CẦU:
1) Với MỖI bảng xếp hạng của đồng nghiệp: HỢP LÝ / MỘT PHẦN / KHÔNG HỢP LÝ + 1 dòng.
2) PHÁN QUYẾT CHỐT: chấp nhận đề xuất "hoàn thiện sản phẩm trước" của đội trưởng
   — CÓ (điều kiện) / KHÔNG (lý do) — và PHƯƠNG ÁN chốt (product-first hay song
   song), kèm lý do giữ mốc.
3) CHECKLIST TỐI NAY 09/08 (ai làm gì, giờ ước lượng, ưu tiên theo ROI) — tối đa
   5 việc, phải trả lời: P/C làm gì nếu chưa có sản phẩm.
4) LỊCH 09-13/08 SỬA LẠI (ngày | việc | ai) KHÔNG phá mốc 13/08 + 16/08 + 25/08.
5) 1 dòng "dòng đỏ" + 1 câu thông điệp.
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
    return {"round": 16, "date": "2026-08-09", "state": STATE}


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
