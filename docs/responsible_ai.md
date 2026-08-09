# Responsible AI — Rightly

## Ethics

- Rightly **không phải cơ quan nhà nước**; mọi câu trả lời là tham khảo,
  có nguồn dẫn chứng, có cảnh báo giới hạn.
- Không thay cán bộ/chuyên gia; không phán quyết tranh chấp; không xử lý
  khẩn cấp (RED → chuyển con người/kênh chính thức).
- **Vụ việc hình sự**: không tự ý đưa ra kết luận hệ trọng; chuyển hướng tới
  hotline/công an nếu cần tư vấn thêm (`CRIMINAL_MATTER` → ORANGE/GUIDE).
- Ưu tiên **an toàn hơn đầy đủ**: thiếu nguồn thì từ chối, không đoán.
- Trung thực về giới hạn hệ thống với người dùng (message CLARIFY/REFUSE
  nói rõ "tôi không trả lời khi chưa chắc chắn").

## Privacy

- Default: không lưu transcript, xóa raw audio sau phiên, log ẩn danh.
- Chỉ transcript + chunks cần thiết được gửi tới LLM; không gửi audio.
- Không thu thập PII không cần thiết; delete session API có sẵn.
- Xem `privacy_deletion_policy.md` và `threat_model.md`.

## Bias

| Nguồn bias | Mitigation (phase này / roadmap) |
|---|---|
| Corpus chỉ 1 nguồn demo | Nhãn DEMO, không dùng kết luận |
| Giọng nói vùng miền (ASR) | `accent_group` trong fixture WER; phải thu thập audio thật cho pilot |
| Người cao tuổi / khó đọc | TTS chậm hơn, lặp lại, nguồn nói ra (spoken citation) |
| Từ vựng hành chính đa nghĩa | AMBIGUOUS_QUERY → CLARIFY |
| LLM bias nội dung | Chỉ bám chunks, source_ids bị chặn ngoài phạm vi |

## Environmental considerations

- Mock mode = không gọi API cloud → tiêu thụ năng lượng thấp.
- PhoWhisper chạy CPU int8; tránh model > medium trên laptop thường.
- TTS/LLM cloud (khi bật) phụ thuộc mạng và bên thứ ba; cân nhắc tần suất
  để giảm năng lượng.

## Human oversight

- RED/ORANGE routing yêu cầu con người (policy + `requires_human`).
- Pilot có người điều phối, không gợi ý đáp án, thu consent riêng.
- Trước pilot bắt buộc: review rule-set bởi chuyên gia tiếng Việt + an toàn;
  xác minh kênh chính thức (hotline, một cửa).
- Mọi thay đổi routing/rule phải có test hồi quy (R3).

## Transparency

- UI/CLI luôn hiển thị "DEMO - không phải kênh chính thức".
- Câu trả lời kèm spoken citation + limitations + next_step.
- Báo cáo eval không bao giờ giả vờ là kết quả pilot.
