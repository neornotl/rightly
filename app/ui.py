"""Streamlit UI for Tieng Lang (optional dependency).

Run with:
    pip install -r requirements-optional.txt
    streamlit run app/ui.py

In mock mode everything works without keys or models. The UI never displays
secrets or raw internal prompts.
"""

from __future__ import annotations

try:
    import streamlit as st  # type: ignore
except ImportError:  # pragma: no cover - reported to user
    st = None

from app.config import load_settings, safe_settings_summary
from app.pipeline import Pipeline

if st is None:
    raise SystemExit(
        "streamlit is not installed. Run: pip install -r requirements-optional.txt\n"
        "Fallback: use the CLI instead -> python -m app.cli"
    )

st.set_page_config(page_title="Tiếng Làng (DEMO)", layout="wide")

settings = load_settings()


@st.cache_resource
def get_pipeline() -> Pipeline:
    return Pipeline(settings=load_settings())


pipeline = get_pipeline()

st.title("Tiếng Làng - DEMO")
st.caption(
    "DEMO - không phải kênh chính thức. Dữ liệu mẫu SYNTHETIC, không phải hướng dẫn hành chính thật."
)
st.warning(
    "Cảnh báo: bản này là môi trường thử nghiệm. Tiếng Làng không phải cơ "
    "quan nhà nước và không thay thế cán bộ hoặc chuyên gia."
)

if "session_id" not in st.session_state:
    st.session_state.session_id = pipeline.create_session()
session_id = st.session_state.session_id

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
        if query.strip():
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
        f"**Zone:** {decision['zone']} | **Action:** {decision['action']} "
        f"| **Cần người:** {decision['requires_human']}"
    )
    st.markdown(f"**Reason codes:** `{', '.join(decision['reason_codes'])}`")

    if data.get("answer"):
        st.markdown("#### Câu trả lời")
        st.write(data["answer"]["answer_text"])
        st.markdown("#### Spoken citation")
        st.write(data["answer"]["spoken_citation"])
        if data["answer"]["limitations"]:
            st.markdown("#### Giới hạn")
            for lim in data["answer"]["limitations"]:
                st.markdown(f"- {lim}")
    else:
        st.markdown("#### Hướng dẫn")
        st.write(decision["user_message"])

    st.markdown("#### Nguồn (retrieved chunks)")
    for chunk in data["chunks"][:3]:
        st.markdown(f"- `{chunk['source_id']}::{chunk['chunk_id']}` score={chunk['score']}")

    st.markdown("#### Latency")
    st.write(data["latencies_ms"])

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔁 Nói lại"):
            if data.get("answer"):
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
