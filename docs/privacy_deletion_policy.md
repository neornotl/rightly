# Privacy & deletion policy

## What we collect / not collect

**Collect (tối thiểu):**

| Data | Default | Lý do |
|---|---|---|
| Transcript (text query) | Không lưu (`SAVE_TRANSCRIPTS=false`) | Cần xử lý câu hỏi |
| Raw audio file | Xóa sau phiên nếu trong `DATA_DIR` | ASR; phiên ngắn hạn |
| Session ID (random) | Log JSONL | Phân biệt phiên, cho phép xóa |
| Metadata latency/routing | Log JSONL | Đánh giá |

**NOT collect:**

- Tên, địa chỉ, email, SĐT, CCCD, vị trí GPS của người dùng.
- Audio gửi lên cloud.
- Nội dung ngoài câu hỏi hiện tại.

## Retention

- Log JSONL: giữ trong `logs/` tới khi bị xóa; có `SessionStore.delete_session`.
- Chunks nguồn: theo vòng đời dữ liệu (mỗi nguồn có `published_date`).
- Không có lưu trữ dài hạn dữ liệu phiên mặc định.

## Deletion

1. `Pipeline.delete_session(session_id)` — xóa mọi dòng log của phiên.
2. `DELETE_RAW_AUDIO_AFTER_SESSION=true` — xóa raw audio trong `DATA_DIR`
   ngay sau phiên.
3. `scripts/scrub_logs.py` — scrub heuristic (email/SĐT/chuỗi ID dài);
   **không phải** đảm bảo pháp lý — với dữ liệu pilot thật, dùng xóa vật lý
   + xác nhận bằng chứng kiểm toán.

## Access control

- Phase này: repo local, không có server nhiều người dùng.
- Trước pilot: log chỉ operator có quyền đọc; không truy cập từ UI.
- API key chỉ trong `.env` (git-ignored), không vào code/source/log.

## Pilot consent assumptions

- Consent bằng giọng nói/chữ viết **tách biệt** cho: (a) ghi âm giọng nói,
  (b) video, (c) sử dụng transcript cho cải thiện hệ thống.
- Người dân có thể từ chối bất kỳ phần nào và vẫn tham gia các phần khác.
- ID người tham gia ẩn danh (không lưu tên thật).
- Chi tiết: `pilot_protocol.md`.

## Bounds & acknowledgment

- Scrub heuristic không thể phát hiện mọi PII (vd số ngắn như "113", địa
  chỉ trong văn xuôi) — với dữ liệu thật cần pipeline xóa + xác minh thủ công
  mẫu.
