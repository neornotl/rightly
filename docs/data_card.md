# Data card — Rightly

> **Phạm vi:** mô tả dữ liệu trong repository và hành vi mặc định của ứng dụng. Không phải đánh giá pháp lý về nguồn hay chính sách xử lý dữ liệu của một deployment cụ thể.

## 1. Data collected (in this phase)

| Item | Status | Retention |
|---|---|---|
| User query text (transcript) | In-memory during pipeline; logged ONLY if `SAVE_TRANSCRIPTS=true` | Session (default) / per config |
| Raw audio file | Temporary, only when user provides a file; deleted after session if inside `DATA_DIR` and `DELETE_RAW_AUDIO_AFTER_SESSION=true` | Session |
| Session ID (random) | Logged in JSONL | Log file; deletable per session |
| Latency / routing metadata | Logged in JSONL (anonymous) | Log file |
| Runtime corpus (`data/chunks/real_chunks.jsonl`) | Chunk đã chuẩn bị, dùng ưu tiên khi khởi tạo pipeline | Repository |
| Demo source (`data/sources/`) | DEMO/SYNTHETIC, chỉ cho phát triển/fallback mock | Repository |
| Law-status registry (`data/law_status.json`) | Trạng thái/expiry/replacement của source ID | Repository |

## 2. Data NOT collected

- Tên, số điện thoại, địa chỉ, email, căn cước công dân của người dùng.
- Audio lên cloud (thiết kế mặc định).
- Nội dung cuộc gọi, danh bạ, vị trí GPS.

## 3. Sources

`data/sources/DEMO_SOURCE.md` là dữ liệu **hư cấu** (xã Bình Minh không có thật), được gắn `DEMO/SYNTHETIC` và `is_demo=true`.

Corpus đang được pipeline ưu tiên nằm trong `data/chunks/real_chunks.jsonl`. Văn bản nguồn thô được lưu riêng trong `legal-sources/`; pipeline không đọc trực tiếp các file này trong request path.

### Front matter fields

`source_id`, `title`, `source_type`, `publisher`, `published_date`,
`language`, `license`, `url`, `notes` — schema tại
`data/schemas/source.schema.json`.

## 4. Chunking

- Demo ingest dùng 900 ký tự/chunk, overlap 120.
- Chunk mang `chunk_id`, `source_id`, text, score metadata; `is_demo` kế thừa từ nguồn demo.
- `scripts/ingest_documents.py` tạo demo output, không phải quy trình tái tạo toàn bộ corpus runtime.

## 5. Provenance & updates (for real deployment)

- Mỗi nguồn thật phải có publisher + ngày kiểm tra + người duyệt.
- Thủ tục có thể thay đổi: cần pipeline refresh có đánh dấu ngày và giữ bản
  cũ với trạng thái "hết hiệu lực (demo cũ)" nếu vẫn hiển thị.

## 6. Bias considerations

- Demo corpus chỉ một nguồn/chủ đề nên không đại diện cho miền hành chính.
- Corpus runtime và registry vẫn cần review liên tục về chất lượng, provenance và hiệu lực.
- Kết quả eval fixture không tự động phản ánh hiệu năng người dùng thật.
