# Pilot protocol (draft — cần review bởi hội đồng trước khi triển khai)

## Mục tiêu

Đo khả năng hoàn thành task, thời gian, mức hài lòng và độ chính xác khi
người dùng thật (8-10 người) dùng Tiếng Làng mock/local trên laptop.

## Người tham gia

- 8-10 người, ưu tiên: 2-3 người ≥ 60 tuổi, 1-2 người khiếm thị/khó đọc,
  còn lại đa dạng độ tuổi/kỹ năng số.
- ID ẩn danh (P01..P10); không ghi tên thật vào dữ liệu.

## Consent

- Tách biệt 3 mục: (a) ghi âm giọng nói, (b) ghi video, (c) dùng transcript
  cải thiện hệ thống. Từ chối một mục không ảnh hưởng các mục khác.
- Đọc to nội dung consent (người khiếm thị) hoặc bản chữ to.

## Môi trường

- Laptop operator; Microphone USB; headset tùy chọn.
- App mode: mock (transcript do operator nhập sau khi người dùng nói) và
  local (PhoWhisper nếu máy đủ tài nguyên — xem hardware plan).
- Chỉ 1 người quan sát trong phòng; không gợi ý đáp án.

## Tasks (3 chuẩn + 1 tự do)

1. **T1**: "Hỏi thủ tục cấp giấy xác nhận hộ khẩu cần những gì."
2. **T2**: "Hỏi đăng ký khai sinh cần giấy tờ gì."
3. **T3**: "Hỏi xác nhận tình trạng hôn nhân mất bao lâu."
4. **T4 (tự do)**: người tham gia tự đặt câu hỏi bất kỳ.

Mỗi task tối đa 5 phút; người dùng có thể hỏi lại, yêu cầu nói lại/chậm.

## Thu thập

- Task completion (hoàn thành / không hoàn thành).
- Thời gian (giây, từ lúc bắt đầu nói tới lúc nghe xong trả lời).
- Satisfaction 1-5 (thang hình tròn cho người khó đọc).
- Accuracy: so transcript tham chiếu của task với transcript hệ thống (WER);
  so answer với nguồn (đúng/thiếu/sai — do 2 người đánh giá độc lập).
- Ghi chú hành vi: người dùng có hiểu spoken citation? có hỏi "người thật"?

## Chống thiên kiến

- Không gợi ý câu hỏi (ngoài đọc task).
- Thứ tự task luân phiên giữa người tham gia.
- Operator không giải thích cách dùng trước khi task.

## Xử lý dữ liệu

- Audio: xóa sau phiên pilot hoặc giữ chỉ khi có consent (a).
- Log: phiên ẩn danh, xóa theo `privacy_deletion_policy.md`.
- Báo cáo: tổng hợp, không gắn nhận dạng; watermark rõ nếu là kết quả pilot.

## Gate

- Không triển khai pilot tới khi: preflight pass, rule-set review xong,
  kênh chính thức xác minh, consent form được duyệt.
