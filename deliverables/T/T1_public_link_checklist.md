# T1 — Public deploy (Streamlit Cloud) không lộ secret — DONE (08/08/2026)

> **Checklist lịch sử.** Không coi nhãn DONE là xác nhận public deployment còn hoạt động hoặc an toàn ở hiện tại.

- **Owner**: T (công tác viên: OpenCode)
- **Quest**: T1 · Deadline 12/08 · **Status: DONE** (chờ bước cuối của T: nối repo trên dashboard Streamlit)

## Đã hoàn thành (code, đã push)

1. **Secrets an toàn**: `app/config.py::_merge_streamlit_secrets()` — secret từ
   Streamlit dashboard được merge vào env (setdefault, không đè .env); UI không
   hiển thị secret; `.streamlit/secrets.toml` đã gitignore + example file không
   chứa key thật.
2. **Retention log 30 ngày** (privacy #2/#3): `prune_old_logs()` chạy lúc khởi
   tạo pipeline, `LOG_RETENTION_DAYS=30`.
3. **Guard abuse nhẹ** (privacy #10): UI giới hạn 20 câu/phiên + 1000 ký tự/câu;
   ghi chú trung thực: đây KHÔNG phải chống DDoS thật trên Streamlit Cloud
   (multi-instance), chỉ giới hạn mỗi browser session.
4. **Deploy config**: `.streamlit/config.toml` (main file = `app/ui.py`),
   `requirements-streamlit.txt` (chỉ dotenv + streamlit + groq — không kéo
   faster-whisper/edge-tts).
5. **REAL-MODE SMOKE TEST (hành động #1 hội đồng): 12/12 passed** qua Groq thật:
   - 9/12 câu trong phạm vi → YELLOW/ANSWER có citation (validator chạy, không
     hallucination source)
   - 2/12 ngoài phạm vi → từ chối đúng (cổ phiếu → CLARIFY; hack → REFUSE)
   - 1/12 (thực phẩm) → ORANGE/REFUSE (retrieval thiếu — hành vi an toàn)
   - Latency LLM: 336-546ms (10/12), **2/12 chậm ~56s** = retry (nghi 429 rate
     limit free tier) — đã được retry_transient xử lý đúng, cần theo dõi
   - Báo cáo: `results/smoke_cloud_20260808_1123.json`

## Bước cuối (con người T làm, ~10 phút)

1. **Xoay key Groq**: key đã trao đổi trong chat → tạo key mới tại
   https://console.groq.com/keys → cập nhật cả `.env` và Streamlit dashboard.
2. Streamlit Cloud: **New app** → chọn repo `neornotl/tieng-lang-v4` (private
   OK, cần cấp quyền GitHub cho Streamlit) → Main file path = **`app/ui.py`**,
   Python version mặc định (3.12+).
3. **Settings → Secrets**: dán nội dung (đã thay key thật):
   ```toml
   APP_MODE = "cloud"
   LLM_BACKEND = "groq"
   ASR_BACKEND = "mock"
   RETRIEVAL_BACKEND = "bm25"
   TTS_BACKEND = "mock"
   GROQ_API_KEY = "gsk_...KEY MỚI..."
   PII_SCRUB_OUTBOUND = "true"
   LOG_RETENTION_DAYS = "30"
   SAVE_TRANSCRIPTS = "false"
   ```
4. Deploy → mở app → test 3 câu: câu hộ tịch (phải trả lời có nguồn), câu
   "mua cổ phiếu" (phải từ chối), câu chứa SĐT (đáp án không nhắc SĐT).
5. Dán link vào `QUESTS.md` (T1) + báo C/P.
6. Theo dõi tuần đầu: latency bất thường, tỷ lệ ORANGE/REFUSE sai.

## Đã kiểm chứng chống lộ secret

- `git check-ignore .streamlit/secrets.toml` → ignored
- `.env` → ignored (từ trước)
- `safe_settings_summary` chỉ in trạng thái "set/unset" của key
- UI không render prompt/secret nội bộ
