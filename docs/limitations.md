# Limitations — Tiếng Làng v4.0

Trung thực về giới hạn: không claim tính năng chưa chạy.

## Functional

1. **Corpus demo duy nhất**: 1 nguồn hư cấu (xã Bình Minh). Không đại diện
   cho miền thủ tục hành chính thật.
2. **BM25 thuần từ vựng**: không hiểu ngữ nghĩa, không embedding/rerank.
   Câu hỏi đổi từ ("giấy xác nhận" ↔ "xác nhận") vẫn ổn, nhưng hỏi kiểu
   khác hoàn toàn có thể trượt.
3. **Rule an toàn heuristic**: danh sách pattern tiếng Việt thủ công; có thể
   miss (không phát hiện tình huống nguy hiểm viết kiểu khác) hoặc false
   positive. Cần review chuyên gia trước pilot.
4. **Không có confidence score**: không calibration nên không dùng % — mọi
   quyết định dùng threshold score BM25 + overlap token + zone.
5. **ASR mock**: MockASR đọc transcript từ file — không phải nhận dạng
   giọng thật. PhoWhisper là adapter, model chưa tải/benchmark.
6. **TTS mock**: ghi text, không tạo âm thanh. Edge-TTS cần mạng và là
   endpoint bên thứ ba.
7. **LLM cloud**: adapter có sẵn nhưng chưa được kiểm thử trên dữ liệu thật;
   chất lượng phụ thuộc key/model và có rủi ro output ngoài schema.
8. **State machine**: lệnh thoại bằng từ khóa (prefix), chưa có NLU.
9. **Latency R4**: số liệu hiện tại là fixture giả lập, không phải phép đo.

## Operational

10. **Windows 10 + Python 3.14**: môi trường dev; CI Linux cần xác nhận
    tương thích.
11. **Số liên hệ khẩn cấp**: placeholder `1900XXXX` — **PHẢI XÁC MINH** trước
    khi triển khai; chưa nên đưa vào trả lời thật.
12. **Scrub logs là heuristic**: không đảm bảo xóa mọi PII; không phải
    pipeline xóa dữ liệu pháp lý.
13. **Chưa có server đa người dùng**: không có auth, rate-limit, giám sát
    vận hành — chưa sẵn sàng production.
14. **Đa ngôn ngữ / điện thoại / OpenVINO**: ngoài phạm vi phase này.

## Measurement honesty

- Mọi số trong `results/` là SYNTHETIC DEMO.
- Không dùng kết quả demo để quyết định ngưỡng pilot mà không có dữ liệu
  thật.
