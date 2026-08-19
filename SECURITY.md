# Security Policy

## Báo cáo lỗ hổng

Dự án đang ở giai đoạn PREPARATION/MVP (mock-first). Nếu bạn phát hiện lỗ hổng
bảo mật — bao gồm rò rỉ dữ liệu, lộ secret, prompt injection làm sai lệch nguồn
pháp luật, hoặc xử lý dữ liệu cá nhân không đúng cam kết trong
`docs/privacy_deletion_policy.md` — hãy dùng GitHub Security Advisory hoặc liên hệ maintainer hiện hành qua kênh riêng tư.

Vui lòng **không** công khai lỗ hổng trước khi đội xác nhận và xử lý.

## Cam kết của dự án

- **Không commit secret**: `.env`, `*.env` trong .gitignore; chỉ `!.env.example`
  (placeholder).
- **Dữ liệu riêng tư**: raw audio bị xóa sau phiên khi bật
  `DELETE_RAW_AUDIO_AFTER_SESSION`; transcript chỉ lưu khi `SAVE_TRANSCRIPTS=true`.
  Xem `docs/privacy_deletion_policy.md`.
- **Cá nhân trong repo**: `data/contacts.json` chỉ chứa đầu mối tư vấn được
  đồng ý đưa vào; không thêm SĐT/ảnh/audio người tham gia pilot vào repo.
- **Nguồn pháp luật**: chỉ trích dẫn văn bản trong `data/law_status.json`
  (registry có kiểm soát); nguồn hết hiệu lực bị chặn bởi CitationValidator.
- **Môi trường public (Streamlit Cloud)**: dùng cấu hình không lộ secret; nếu
  không thể đảm bảo, không deploy dữ liệu nhạy cảm.

## Phạm vi hỗ trợ

Bảo mật được ưu tiên cho: pipeline local (ASR→TTS), privacy logging, validator
nguồn, config không lộ key. Các tính năng ngoài scope (điện thoại/SIM,
FreeSWITCH, multi-tenant) chưa được audit.
