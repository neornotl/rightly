# Demo script (mock)

Kịch bản demo 5 phút, chạy hoàn toàn mock — không key, không model, không
mạng.

## Setup

```powershell
.\.venv\Scripts\python.exe scripts/ingest_documents.py
.\.venv\Scripts\python.exe scripts/run_mock_demo.py
```

## Kịch bản

### 1. Giới thiệu (30s)

> "Tiếng Làng là trợ lý tra cứu thủ tục hành chính bằng tiếng Việt, mọi câu
> trả lời đều kèm nguồn. Đây là bản DEMO — dữ liệu xã Bình Minh là hư cấu."

### 2. Demo chuẩn (1 phút)

Câu hỏi: `Thủ tục cấp giấy xác nhận hộ khẩu tại xã Bình Minh?`

Kỳ vọng: zone=YELLOW/ANSWER, câu trả lời lấy từ chunk nguồn, spoken citation
hiển thị `demo_binhminh_procedures`.

### 3. Demo an toàn (1 phút)

Câu hỏi: `Tôi bị đau tim dữ dội, làm sao bây giờ?`

Kỳ vọng: zone=RED/ESCALATE, requires_human=true, **không có** câu trả lời nội
dung, message chuyển hướng khẩn cấp (số điện thoại chưa xác minh — nói rõ
"placeholder").

### 4. Demo từ chối (1 phút)

Câu hỏi: `Tổng thống Mỹ tên là gì?`

Kỳ vọng: ORANGE/REFUSE — "không tìm thấy nguồn đủ tin cậy".

### 5. CLI tương tác (tùy chọn, 1 phút)

```powershell
.\.venv\Scripts\python.exe -m app.cli --transcript "Đăng ký khai sinh cần giấy gì?" --once
```

Nói rõ: lệnh "nói lại", "nguồn ở đâu", "kết thúc" hoạt động trong CLI.

## Lưu ý trình bày

- Nhấn mạnh: kết quả là **SYNTHETIC DEMO - NOT PILOT RESULTS**.
- Không hứa hẹn tính năng điện thoại/SIM (ngoài phạm vi).
- Nếu demo UI: `python -m streamlit run app/ui.py`.
