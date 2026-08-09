"""Round 17 — council ruling on T's full 09/08 work plan + live critique mode.

User (team lead) directive 09/08: T finishes ALL remaining tasks TODAY so the
product is usable tonight; only P's verified phone + Zalo OA + C's corpus links
are needed afterwards to go public. Council runs IN PARALLEL with coding:
critique each delivered piece as it lands.

3 phases (resumable via --phase N):
  P1 analysis   : rate each remaining gap (hours, blocks which milestone).
  P2 critique   : critique the shipped demo pieces (connect+slip) + risks.
  P3 ruling     : accept plan; acceptance criteria for "demo-ready public".
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from council_models import MEMBERS  # noqa: E402

OUT_FILE = "debate_output/round17.json"

STATE = """TỔNG QUAN DỰ ÁN "TIẾNG LÀNG v4.0" — BÁO CÁO KÍN CHO HỘI ĐỒNG (Round 17, tối 09/08/2026):
- Sản phẩm: voice-first AI tiếng Việt "tổng đài viên ảo" tư vấn thủ tục hành chính/
  quyền lợi công/pháp luật dân sự cho người cao tuổi nông thôn. ASR→retrieval hybrid→
  SafetyRouter→LLM(Groq/Gemini)→CitationValidator(11 nguồn luật thật)→TTS.
  CLI+Streamlit. 125 tests xanh, ruff sạch, preflight 9/9, smoke real Groq 12/12.
- SAU ROUND 16 (song song có kiểm soát, 5/5): T dồn 100% vào 3 gap: (F3) deploy
  public Streamlit Cloud + HF Spaces backup, (F4) xoay 3 key Groq + fallback Gemini
  + rate-limit, (F5) voice FAQ 5-10 kịch bản trước 17h. P: email BTC Intel loan +
  LOI UBND/Hội NCT + nguồn pilot. C: danh sách NCT + consent + kịch bản phỏng vấn.
- ĐÃ LÀM XONG TỐI NAY (09/08): feature demo "NỐI MÁY + PHIẾU HỒ SƠ" — (1)
  Command.CONNECT + triggers ("nối máy","đồng ý kết nối","oke"...), (2)
  State.CONNECTING với edges LISTENING/SPEAKING→CONNECTING→{LISTENING,SPEAKING,
  DONE,ERROR}, (3) module app/contacts.py: danh bạ JSON, CHỈ mở tel: khi
  verified=true, (4) app/forms.py: phiếu markdown điền sẵn quy trình, trường cá
  nhân ĐỂ TRỐNG + privacy note "không thu thập/lưu/gửi", (5) Streamlit UI: nút
  "Gọi ngay (mở quay số)" + tải phiếu, (6) CLI xử lý lệnh nối máy, (7) 14 test
  mới xanh. contacts.json còn 2 số placeholder 1900XXXX verified=false — P phải
  xác minh số thật trước demo public.
- CÒN LẠI CỦA T (09/08): (F3) deploy public sẵn sàng — requirements.txt, template
  .streamlit/secrets.toml.example, script verify, hướng dẫn 2 nút bấm; (F4) cơ chế
  xoay key Groq (nhiều GROQ_API_KEY_2/3) + fallback Gemini + rate-limit theo IP/
  session; (F5) voice FAQ 5-10 kịch bản (file FAQ, giọng trầm, chống lỗi ASR); +
  script log WER/MOS cho pilot (13/08); + OpenVINO path CPU-first (máy không NPU).
- CUỘC THI: Intel(R) Vietnam AI Impact Festival 2026 (VAIIF26, nội bộ). BTC
  NIC+SHTP+SHTP-IC+Intel VN. ĐỘI BẢNG HỌC SINH 13-17, nhóm ≤3, consent phụ huynh.
  Hồ sơ = Google Form: tên ≤10 từ + 150 từ (EN) + video 2' + consent. Hạn
  25/08/2026. Top 3 = 3 vé riêng bảng Học sinh; Top 1 bảng = Intel AI Global
  Impact Festival 2026. Rubric 50đ: M1 Impact&Inclusion 15, M2 AI Innovation 20,
  M3 Technical 15. Xác suất chốt R15: Top 3 65-75%, Top 1 28-40%.
- YÊU CẦU ĐỘI TRƯỞNG (09/08): "Làm full phần việc của T HÔM NAY — tối nay sản
  phẩm dùng được luôn; chỉ cần add SĐT + Zalo OA + link corpus của C là đem
  public được. Hội đồng vừa code vừa thảo luận vừa phản biện nếu thấy vấn đề."
- LỊCH: 10-11/08 Zalo OA đăng ký; 12/08 deploy public + trả lời Intel loan;
  13/08 pilot 5-7 người + SĐT/Zalo live + FREEZE feature; 14/08 Technical Rigor;
  16/08 video RENDER; 18/08 pilot 20-30 XONG; 25/08 nộp.

CÂU HỎI HỘI ĐỒNG ROUND 17 (họp kín — DUYỆT KẾ HOẠCH "T LÀM FULL HÔM NAY"):
1) ĐÁNH GIÁ TỪNG GAP còn lại của T: [F3 deploy public | F4 xoay key+fallback+
   rate-limit | F5 voice FAQ | script WER/MOS | OpenVINO path | corpus 15-30] —
   với mỗi gap: giờ ước lượng, có chặn mốc nào (12/08 public / 13/08 pilot /
   14/08 rigor / 16/08 video), phải xong TỐI NAY hay có thể dời?
2) PHẢN BIỆN 2-3 feature demo đã ship tối nay (nối máy + phiếu): thiếu gì về
   privacy/legal (PDPL NĐ 13/2023), UX người cao tuổi, rủi ro lộ số, rủi ro
   phiếu bị hiểu nhầm là giấy tờ chính thức? Sửa ngay bây giờ hay đủ dùng?
3) RỦI RO khi đem public tối nay: lộ secret, DDoS, spam, chi phí API, Groq
   rate-limit hằng ngày, dữ liệu người dùng → cơ chế nào BẮT BUỘC phải có trong
   bản public đầu tiên (phân loại theo BẮT BUỘC / NÊN / CÓ THỂ TRÌ HOÃN)?
4) PHÁN QUYẾT: chấp nhận kế hoạch "T làm full hôm nay, sản phẩm dùng được tối
   nay" (điều kiện gì)? TIÊU CHÍ "DEMO-READY PUBLIC" (checklist tối thiểu)?
   LỆNH code theo thứ tự nào tối nay (thứ tự ưu tiên từng task + giờ)?
Trả lời tối đa 1100 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_P2_HEADER = """BÁO CÁO KÍN — PHIÊN 2 (PHẢN BIỆN CHI TIẾT + HỘI TỤ):
Đã nhận 5 phân tích (dán bên dưới). YÊU CẦU:
1) Phản biện 2-3 luận điểm YẾU của thành viên khác (ai nói gì, định lượng).
2) Công nhận 1 điểm "bất ngờ đúng" của MỖI thành viên.
3) PHẢN BIỆN KỸ THUẬT 2 feature demo đã ship tối nay:
   a) Command.CONNECT trigger "oke"/"đồng ý" — rủi ro false-positive với lời nói
      thường của NCT (ASR lỗi) dẫn tới mở kết nối nhầm? Cần cấp độ xác nhận thứ 2?
   b) Phiếu hồ sơ markdown tự điền summary của LLM — rủi ro LLM viết bừa thủ tục
      làm NCT tin tưởng giấy? Cần watermark "không chính thức" mạnh hơn?
   c) contacts.json verified=false — nếu public link mà P chưa xác minh số, hiện
      nút Gọi ngay ảo hay ẩn hẳn? (đã chọn ẩn + cảnh báo — đủ hay nên khác?)
4) BẢNG XẾP HẠNG task tối nay: [stt | task | giờ | chặn mốc | làm tối nay?].
5) TIÊU CHÍ "DEMO-READY PUBLIC" tối thiểu (5-8 dòng checklist BẮT BUỘC).
Trả lời tối đa 900 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

_P3_HEADER = """BÁO CÁO KÍN PHIÊN 3 (PHÁN QUYẾT CUỐI — DUYỆT KẾ HOẠCH T 09/08):
Đã nhận 5 phản biện (dán bên dưới). YÊU CẦU:
1) Với MỖI bảng xếp hạng của đồng nghiệp: HỢP LÝ / MỘT PHẦN / KHÔNG HỢP LÝ + 1 dòng.
2) PHÁN QUYẾT CHỐT: chấp nhận "T làm full hôm nay — sản phẩm dùng được tối nay"
   — CÓ (điều kiện) / KHÔNG (lý do) — kèm lệnh thứ tự code tối nay (tối đa 6 task,
   giờ, thứ tự).
3) CHECKLIST "DEMO-READY PUBLIC" chốt (tối đa 8 mục, phân BẮT BUỘC/NÊN/HOÃN).
4) 3 CẢNH BÁO ĐỎ (rủi ro sẽ nổ nếu không xử lý trước 12/08).
5) 1 dòng "dòng đỏ" + 1 câu thông điệp cho đội.
Trả lời tối đa 900 từ tiếng Việt, kết thúc: AGREEMENT: [YES/PARTIAL/NO] — ≤15 từ."""

SYSTEM = (
    "Bạn là thành viên hội đồng chiến lược của dự án 'Rightly' (voice-first "
    "AI tiếng Việt cho người cao tuổi; thi Intel Vietnam AI Impact Festival 2026 — "
    "KHÔNG phải VAIFF — bảng Học sinh 13-17, hạn 25/08). Bạn THẬN TRỌNG, định lượng, "
    "không nể nang, bác bỏ luận điểm ảo; ưu tiên ROI thực (người-ngày, tiền, rủi ro "
    "phá mốc). Tiếng Việt."
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
    return {"round": 17, "date": "2026-08-09", "state": STATE}


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
