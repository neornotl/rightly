"""Round 12 — closed council session: can Tieng Lang v4.0 reach top 3 nationally?

3 phases, incremental save (resumable via --phase N):
  P1 opinions  : each member: probability of top-3 / top-1 category + blockers.
  P2 rebuttals : each member: >=2 logical rebuttals against others + 1 fair point
                 from each member.
  P3 verdicts  : each member: judge EVERY phase-2 rebuttal (HOP LY / KHONG /
                 MOT PHAN) + final strategic position + AGREEMENT.

Usage: python scripts/round12_debate.py --phase 1
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from council_models import MEMBERS  # noqa: E402

OUT_FILE = "debate_output/round12.json"

STATE = """TỔNG QUAN DỰ ÁN "TIẾNG LÀNG v4.0" — BÁO CÁO KÍN CHO HỘI ĐỒNG (sau Round 11, ngày 08/08/2026):
- Sản phẩm: voice-first AI tiếng Việt hoạt động như "tổng đài viên ảo" tư vấn thủ tục hành chính, quyền lợi công (BHXH, hộ tịch...), pháp luật dân sự; hướng tới người cao tuổi, người ít kỹ năng số, nông thôn. Hình sự/khẩn cấp chuyển kênh (113/115), không trả lời.
- Kiến trúc: ASR (Mock/PhoWhisper) → normalize → retrieval hybrid BM25+dense+RRF (npz cache) → SafetyRouter (RED/ORANGE/YELLOW; routes EMERGENCY/INSUFFICIENT/OFF-SCOPE/CRIMINAL) → LLM (Mock | Groq | Gemini, cloud-first đã chốt) → CitationValidator (chặn văn bản hết hiệu lực, 11 nguồn luật thật) → TTS (Mock/Edge). CLI + Streamlit UI sẵn sàng public link.
- Chất lượng hiện tại: 111 tests xanh, ruff sạch, preflight 9/9, eval R1-R4 có baseline (WER/Retrieval/Routing/Latency), demo transcript deterministic (docs/demo/), smoke real-mode Groq 12/12 PASSED (ngày 08/08), Round 11 đã làm câu trả lời tự nhiên theo chuẩn tổng đài viên (prompt dùng chung, trích dẫn đọc giọng ≤15 từ), PII scrubber outbound, retry+classify an toàn cho LLM cloud, log retention 30 ngày, UI guard 20 câu/phiên.
- Các khoản nợ kỹ thuật: corpus hiện là demo tổng hợp ("xã Bình Minh") chưa phải kho luật thật đầy đủ (quest C1 đang giao C); ASR/TTS chưa validate trên audio thật; chưa có AI PC/OpenVINO; Groq key chưa xoay; m365-copilot mới nối lại proxy hôm nay.
- Nợ con người: C (content) chưa có deliverable cuối tuần; P (pilot) chưa tuyển ai; pilot 8-10 người dự kiến 20/08; video demo 22/08; public link dự kiến 12/08.
- Deadline: hồ sơ dự thi VAIIF26 nộp 25/08/2026; mục tiêu ≥45/50 điểm rubric. Rubric ghi nhận từ các round trước: M1 pilot evidence & user testimony, M2 innovation & GTM, M3 technical stability; các tiêu chí Credibility, Trustworthiness, Compliance, Citation quality, Responsible AI, Impact & SDG alignment, Evaluation rigor.

CÂU HỎI HỘI ĐỒNG ROUND 12 (phiên họp KÍN — ý kiến chỉ nội bộ đội dự thi):
1) Với trạng thái hiện tại (chấm ngay hôm nay), xác suất dự án vào được TOP 3 TOÀN QUỐC VAIIF26 là bao nhiêu %? Lý do trung thực.
2) Nếu khó top 3 chung cuộc: hạng mục nào dự án có cơ hội TOP 1 nhất để (a) được công nhận/cấp chứng nhận cấp quốc gia, hoặc (b) giành vé đi vòng quốc tế? (các hạng mục điển hình: Dịch vụ công số / AI vì cộng đồng & tiếp cận / Responsible AI & Ethics / Innovation / Startup trẻ...). Chọn 1 hạng mục + luận cứ.
3) 3 rào cản LỚN NHẤT chặn đường top (kỹ thuật, con người, bằng chứng) + cách vượt cụ thể trước 25/08.
4) Phương án dự phòng: nếu pilot/evidence chưa kịp, chiến lược tối đa hóa điểm nào, cắt điểm nào?
Trả lời tối đa 900 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_REBUT_HEADER = """BÁO CÁO KÍN CHO HỘI ĐỒNG — PHIÊN 2 (PHẢN BIỆN CHÉO):
Đã nhận ý kiến mở đầu của 5 thành viên (dán bên dưới). Bạn là thành viên hội đồng phản biện. YÊU CẦU:
1) Chọn ÍT NHẤT 2 luận điểm của các thành viên khác mà bạn cho là SAI/QUÁ LẠC QUAN/THIẾU CĂN CỨ, phản biện bằng lý lẽ logic, có thể nêu dữ kiện đối chứng.
2) Với MỖI thành viên còn lại, công nhận ít nhất 1 luận điểm HỢP LÝ của họ (một dòng/người).
3) Giữ hay điều chỉnh lập trường mở đầu của bạn về top 3 / top 1 hạng mục (nêu rõ).
Trả lời tối đa 900 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

_VERDICT_HEADER = """BÁO CÁO KÍN CHO HỘI ĐỒNG — PHIÊN 3 (PHÁN QUYẾT CUỐI):
Đã nhận toàn bộ PHẢN BIỆN của 5 thành viên (dán bên dưới, kèm tên người phản biện và người bị phản biện). YÊU CẦU:
1) Xét TỪNG phản biện trong phiên 2: kết luận HỢP LÝ / KHÔNG HỢP LÝ / MỘT PHẦN, kèm 1-2 dòng lý do vì sao (đúng logic hay sai logic, thiếu/đủ bằng chứng). Phản biện nhắm vào ý kiến của chính bạn cũng phải xét công bằng.
2) Tổng kết: trong các phản biện được đa số thành viên công nhận, rút ra 3 hành động quyết định nhất trước 25/08.
3) ĐÍCH CHIẾN LƯỢC CUỐI của bạn: (a) mục tiêu thực tế nhất: top 3 chung cuộc / top 1 hạng mục nào / cấp chứng nhận quốc gia / vé quốc tế; (b) điểm số kỳ vọng /45 hoặc /50; (c) 1 câu chốt chiến lược.
Trả lời tối đa 700 từ tiếng Việt, kết thúc dòng: AGREEMENT: [YES/PARTIAL/NO] — [≤15 từ]."""

SYSTEM = (
    "Bạn là thành viên hội đồng phản biện của dự án 'Rightly' (voice-first "
    "AI tiếng Việt cho người dân, thi VAIIF26). Bạn KHÔNG nói xuôi, không nể nang: "
    "đánh giá trung thực, định lượng, có logic; ý kiến phản biện phải sắc và có căn cứ; "
    "ý kiến đồng thuận phải nêu lý do. Trả lời tiếng Việt."
)


def _build_prompt(phase: int, data: dict) -> str:
    if phase == 1:
        return STATE
    opinions = data.get("phase1", {})
    if phase == 2:
        blocks = [_REBUT_HEADER]
        for name in MEMBERS:
            text = opinions.get(name["display"], "[chưa có]")
            blocks.append(f"\n=== {name['display']} (ý kiến mở đầu) ===\n{text[:2800]}")
        return "\n".join(blocks)
    rebuttals = data.get("phase2", {})
    blocks = [_VERDICT_HEADER]
    for name in MEMBERS:
        text = rebuttals.get(name["display"], "[chưa có]")
        blocks.append(f"\n=== {name['display']} (phản biện phiên 2) ===\n{text[:2200]}")
    return "\n".join(blocks)


def call_model(member: dict, user_text: str, max_tokens: int) -> str:
    key = os.environ.get(member["key_env"]) if member["key_env"] else None
    body = {
        "model": member["model"],
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    headers.update(member.get("headers_extra") or {})
    data = json.dumps(body).encode("utf-8")
    last_err = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(member["url"], data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            return payload["choices"][0]["message"]["content"].strip()
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            if isinstance(exc, urllib.error.HTTPError):
                detail = exc.read().decode("utf-8", errors="replace")[:200]
                print(f"  [{member['display']}] HTTP {exc.code}: {detail}")
            else:
                print(f"  [{member['display']}] attempt {attempt}: {exc}")
    raise RuntimeError(f"{member['display']} failed: {last_err}")


def load() -> dict:
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"round": 12, "date": "2026-08-08", "state": STATE}


def save(data: dict) -> None:
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def main() -> int:
    phase = int(sys.argv[sys.argv.index("--phase") + 1]) if "--phase" in sys.argv else 1
    key = f"phase{phase}"
    data = load()
    data.setdefault(key, {})
    prompt = _build_prompt(phase, data)
    max_tokens = {1: 5000, 2: 5000, 3: 4000}[phase]
    for member in MEMBERS:
        if data[key].get(member["display"]):
            print(f"skip {member['display']} (already done)")
            continue
        print(f"== [{phase}] {member['display']} ...")
        sys.stdout.flush()
        try:
            data[key][member["display"]] = call_model(member, prompt, max_tokens)
            print(f"== done ({len(data[key][member['display']])} chars)")
        except Exception as exc:  # noqa: BLE001
            data[key][member["display"]] = f"[ERROR] {exc}"
            print(f"== FAILED: {exc}")
        save(data)
        sys.stdout.flush()
    print(f"Saved -> {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
