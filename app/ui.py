"""Streamlit UI for Rightly (optional dependency).

Run with:
    pip install -r requirements-optional.txt
    streamlit run app/ui.py

In mock mode everything works without keys or models. The UI never displays
secrets or raw internal prompts.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Streamlit Cloud runs `streamlit run app/ui.py`: only the *script dir*
# (app/) is prepended to sys.path, so `import app...` breaks. Put the repo
# root (parent of app/) on sys.path explicitly.
_APP_ROOT = Path(__file__).resolve().parent.parent
if str(_APP_ROOT) not in sys.path:
    sys.path.insert(0, str(_APP_ROOT))

try:
    import streamlit as st  # type: ignore
except ImportError:  # pragma: no cover - reported to user
    st = None

from app.config import load_settings, safe_settings_summary  # noqa: E402 - needs sys.path fix above
from app.pipeline import Pipeline  # noqa: E402

if st is None:
    raise SystemExit(
        "streamlit is not installed. Run: pip install -r requirements-optional.txt\n"
        "Fallback: use the CLI instead -> python -m app.cli"
    )

st.set_page_config(page_title="Rightly (DEMO)", layout="wide")

# Council R20 (nemotron-nano): elderly-friendly CSS — bigger fonts, larger
# click targets, darker captions (Streamlit defaults are too small for 65-80).
st.markdown(
    """
    <style>
      html, body, [class*="st-"], .stMarkdown p, .stButton button {
        font-size: 18px !important;
      }
      .stButton button, [data-testid="stLinkButton"] a, .stPopover button {
        min-height: 48px;
      }
      .stCaption, [data-testid="stCaptionContainer"] {
        color: #444 !important;
      }
      h1 { font-size: 1.9rem !important; }
      h2, h3 { font-size: 1.4rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

settings = load_settings()


@st.cache_resource
def get_pipeline() -> Pipeline:
    return Pipeline(settings=load_settings())


pipeline = get_pipeline()

st.title("Rightly - DEMO")
st.caption(
    "DEMO - không phải kênh chính thức. Dữ liệu mẫu SYNTHETIC, không phải hướng dẫn hành chính thật."
)
st.warning(
    "Cảnh báo: bản này là môi trường thử nghiệm. Rightly không phải cơ "
    "quan nhà nước và không thay thế cán bộ hoặc chuyên gia."
)

if "session_id" not in st.session_state:
    st.session_state.session_id = pipeline.create_session()
session_id = st.session_state.session_id


def _render_connect_and_slip(data: dict, session_id: str) -> None:
    """Offer 'nối máy tới cơ quan' + phiếu chuẩn bị hồ sơ (demo-grade).

    Privacy: phone numbers are shown only when verified; the slip never
    collects personal data. Nothing here leaves the browser.
    """
    from app.contacts import default_contact, find_contact
    from app.forms import build_registration_slip

    contact = find_contact("bo-phan-mot-cua-xa-binh-minh") or default_contact()
    answer = data.get("answer") or {}

    st.divider()
    st.markdown("#### 📞 Bạn có muốn kết nối với cơ quan không?")
    if contact is None:
        st.info("Chưa có đầu mối liên hệ trong danh bạ (P cần xác minh).")
        return
    st.markdown(f"**{contact.label}**")
    if contact.callable:
        # Council R17: consent dialog before dialing (no silent tel: action).
        with st.popover("📞 Gọi ngay", use_container_width=True):
            st.warning(
                f"Cuộc gọi sẽ mở từ thiết bị của BẠN tới: **{contact.label}** "
                f"({contact.phone}). Rightly không tự gọi và không nghe cuộc gọi."
            )
            st.link_button("📞 Xác nhận gọi ngay", contact.tel_link, type="primary")
            st.caption("Không muốn gọi? Đóng hộp này — không có cuộc gọi nào được mở.")
    else:
        st.warning(
            "Số điện thoại chưa được xác minh thực tế (đang là chỗ trống tạm) — "
            "bản demo không mở quay số với số chưa kiểm chứng."
        )
    if contact.note:
        st.caption(contact.note)

    slip = build_registration_slip(
        query=str(data.get("query", "")),
        summary=str(answer.get("answer_text", "")),
        next_step=str(answer.get("next_step", "")),
        contact=contact,
    )
    st.download_button(
        "📄 Tải phiếu chuẩn bị hồ sơ (điền sẵn quy trình, bạn tự điền thông tin cá nhân)",
        data=slip.to_markdown(),
        file_name="phieu_chuan_bi_ho_so.md",
        mime="text/markdown",
    )
    st.caption(
        "Phiếu chỉ hỗ trợ khai sẵn quy trình — không thu thập, lưu trữ hay gửi "
        "thông tin cá nhân của bạn. Rightly không phải cơ quan nhà nước."
    )


# Lightweight abuse guard (demo-grade): per-session caps. Honest note: this
# is NOT real DDoS protection on Streamlit Cloud (multiple instances) - it
# only limits what one browser session can do.
MAX_QUERIES_PER_SESSION = 20
MAX_QUERY_CHARS = 1000
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# F4: per-client hourly cap (in-memory, per instance). Key = hashed client IP
# (when available) + session id so a full session never gets locked out.
from app.ratelimit import RateLimiter  # noqa: E402

_limiter = RateLimiter(
    limit=settings.rate_limit_per_ip, window_seconds=settings.rate_limit_window_seconds
)


def _client_key() -> str:
    ip = ""
    try:
        headers = st.context.headers
        ip = headers.get("X-Forwarded-For", "").split(",")[0].strip()
    except Exception:  # noqa: BLE001 - Streamlit API varies across versions
        pass
    return f"{hash(ip or 'local') % 10**9}|{session_id}"


col_status, col_query = st.columns([1, 2])

with col_status:
    st.subheader("Trạng thái hệ thống")
    st.json(safe_settings_summary(settings))
    if st.button("Xóa phiên (delete session)"):
        pipeline.delete_session(session_id)
        del st.session_state.session_id
        st.rerun()

with col_query:
    st.subheader("Nhập câu hỏi (mock transcript)")
    query = st.text_input("Câu hỏi:", key="query_input")
    if st.button("Hỏi", type="primary"):
        if st.session_state.query_count >= MAX_QUERIES_PER_SESSION:
            st.error(
                f"Đã đạt giới hạn {MAX_QUERIES_PER_SESSION} câu hỏi cho phiên này. "
                "Xóa phiên để tiếp tục."
            )
        elif len(query.strip()) > MAX_QUERY_CHARS:
            st.error(f"Câu hỏi quá dài (tối đa {MAX_QUERY_CHARS} ký tự).")
        elif not _limiter.allow(_client_key()):
            st.error(
                f"Đã đạt giới hạn {settings.rate_limit_per_ip} câu hỏi trong "
                f"{settings.rate_limit_window_seconds // 3600} giờ cho máy này. "
                "Vui lòng quay lại sau."
            )
        elif query.strip():
            st.session_state.query_count += 1
            with st.spinner("Đang xử lý..."):
                result = pipeline.process_text(session_id, query)
            st.session_state.last_result = result.to_dict()
        else:
            st.info("Nhập câu hỏi trước.")

if "last_result" in st.session_state:
    data = st.session_state.last_result
    decision = data["decision"]
    zone_color = {
        "YELLOW": "🟡",
        "ORANGE": "🟠",
        "RED": "🔴",
    }.get(decision["zone"], "")
    st.subheader(f"Kết quả {zone_color}")
    st.markdown(
        f"**Mức độ xử lý:** {decision['zone']} | "
        f"**Hướng xử lý:** {decision['action']} | "
        f"**Cần cán bộ hỗ trợ:** {'Có' if decision['requires_human'] else 'Không'}"
    )
    st.markdown(f"**Lý do:** `{', '.join(decision['reason_codes'])}`")

    if data.get("answer"):
        st.markdown("#### Câu trả lời")
        st.write(data["answer"]["answer_text"])
        st.markdown("#### Phần nhắc (kèm câu trả lời)")
        st.write(data["answer"]["spoken_citation"])
        if data["answer"]["limitations"]:
            st.markdown("#### Lưu ý")
            for lim in data["answer"]["limitations"]:
                st.markdown(f"- {lim}")
        _render_connect_and_slip(data, session_id)
    else:
        st.markdown("#### Hướng dẫn")
        st.write(decision["user_message"])

    with st.expander("Chi tiết kỹ thuật"):
        st.markdown("#### Nguồn (retrieved chunks)")
        for chunk in data["chunks"][:3]:
            st.markdown(f"- `{chunk['source_id']}::{chunk['chunk_id']}` score={chunk['score']}")
        st.markdown("#### Latency")
        st.write(data["latencies_ms"])

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔁 Nghe lại"):
            audio_path = pipeline.settings.resolved_results_dir() / f"{session_id}.wav"
            if audio_path.exists() and audio_path.stat().st_size > 0:
                st.audio(str(audio_path))
            elif data.get("answer"):
                st.warning(
                    "Chế độ thử nghiệm hiện không tạo giọng đọc (TTS chưa kích hoạt "
                    "trên máy chủ này). Xem nội dung bên dưới:"
                )
                st.info(data["answer"]["answer_text"])
    with c2:
        if st.button("🐢 Nói chậm hơn"):
            st.info("(mock: chưa kích hoạt tốc độ chậm trong bản demo)")
    with c3:
        if st.button("❌ Xóa phiên"):
            pipeline.delete_session(session_id)
            del st.session_state.session_id
            st.rerun()


st.divider()
st.caption(
    "Không hiển thị secret hoặc prompt nội bộ. Audio không được gửi ra ngoài trong chế độ mặc định."
)
