# Data card — Rightly (preparation phase)

## 1. Data collected (in this phase)

| Item | Status | Retention |
|---|---|---|
| User query text (transcript) | In-memory during pipeline; logged ONLY if `SAVE_TRANSCRIPTS=true` | Session (default) / per config |
| Raw audio file | Temporary, only when user provides a file; deleted after session if inside `DATA_DIR` and `DELETE_RAW_AUDIO_AFTER_SESSION=true` | Session |
| Session ID (random) | Logged in JSONL | Log file; deletable per session |
| Latency / routing metadata | Logged in JSONL (anonymous) | Log file |
| Source corpus (`data/sources`) | DEMO/SYNTHETIC, fictional | Repository |

## 2. Data NOT collected

- Tên, số điện thoại, địa chỉ, email, căn cước công dân của người dùng.
- Audio lên cloud (thiết kế mặc định).
- Nội dung cuộc gọi, danh bạ, vị trí GPS.

## 3. Sources

`data/sources/DEMO_SOURCE.md` — dữ liệu **hư cấu** (xã Bình Minh không có
thật), nhãn `DEMO/SYNTHETIC` ở front matter và trong từng chunk
(`is_demo=true`). Không có nguồn chính thức nào trong repo.

### Front matter fields

`source_id`, `title`, `source_type`, `publisher`, `published_date`,
`language`, `license`, `url`, `notes` — schema tại
`data/schemas/source.schema.json`.

## 4. Chunking

- 900 ký tự / chunk, overlap 120.
- Mỗi chunk ghi `chunk_id = <source_id>::cNNN`, `is_demo` kế thừa từ nguồn.
- Output: `data/chunks/demo_chunks.jsonl` + `data/metadata.csv` (sinh bởi
  `scripts/ingest_documents.py`).

## 5. Provenance & updates (for real deployment)

- Mỗi nguồn thật phải có publisher + ngày kiểm tra + người duyệt.
- Thủ tục có thể thay đổi: cần pipeline refresh có đánh dấu ngày và giữ bản
  cũ với trạng thái "hết hiệu lực (demo cũ)" nếu vẫn hiển thị.

## 6. Bias considerations

- Demo corpus chỉ 1 nguồn, 1 chủ đề → không đại diện cho miền hành chính.
- Kết quả eval không phản ánh hiệu năng thật (watermark bắt buộc).
