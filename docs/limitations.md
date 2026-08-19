# Giới hạn hiện tại của Rightly

> Tài liệu này nói về giới hạn có thể suy ra từ code và artifact hiện có, không kết luận ứng dụng đã sẵn sàng production/pilot.

Trung thực về giới hạn: không claim tính năng chưa chạy.

## Functional

1. **Chất lượng corpus phụ thuộc pipeline dữ liệu**: corpus runtime có nhiều chunk và registry, nhưng freshness, quyền sử dụng, provenance và đầy đủ nội dung vẫn phải được xác minh độc lập.
2. **Retrieval không bảo đảm hiểu đúng ý định**: BM25 là đường chắc chắn có sẵn; hybrid/rerank là tùy chọn dependency và có thể hạ về BM25.
   Câu hỏi đổi từ ("giấy xác nhận" ↔ "xác nhận") vẫn ổn, nhưng hỏi kiểu
   khác hoàn toàn có thể trượt.
3. **Rule an toàn heuristic**: danh sách pattern tiếng Việt thủ công; có thể
   miss (không phát hiện tình huống nguy hiểm viết kiểu khác) hoặc false
   positive. Cần review chuyên gia trước pilot.
4. **Không có confidence score**: không calibration nên không dùng % — mọi
   quyết định dùng threshold score BM25 + overlap token + zone.
5. **ASR mock không đại diện nhận dạng giọng thật**: PhoWhisper là adapter tùy chọn, cần benchmark trên thiết bị/giọng mục tiêu.
6. **TTS phụ thuộc backend ngoài**: mock chỉ ghi spoken text; các backend thật có thể cần mạng, key, quota hoặc `ffmpeg`.
7. **LLM không phải nguồn luật**: backend cloud/local có thể lỗi, thay đổi model hoặc trả format không mong muốn; system sẽ từ chối khi lỗi nhưng không thể bảo đảm trả lời đầy đủ.
8. **State machine**: lệnh thoại bằng từ khóa (prefix), chưa có NLU.
9. **Latency R4**: số liệu hiện tại là fixture giả lập, không phải phép đo.

## Operational

10. **Môi trường triển khai cần được xác minh riêng**: dependency, model, tài nguyên và network thay đổi theo máy/host.
11. **Contact phải được xác minh tại deployment**: chỉ contact có `verified=true` và số hợp lệ mới callable; không suy ra correctness chỉ từ dữ liệu repo.
12. **Scrub logs là heuristic**: không đảm bảo xóa mọi PII; không phải
    pipeline xóa dữ liệu pháp lý.
13. **Không có nền tảng production hoàn chỉnh**: rate limit là in-memory per process; authentication, distributed rate limiting, monitoring, backup và access control cần thiết kế riêng.
14. **Đa ngôn ngữ / điện thoại / OpenVINO**: ngoài phạm vi phase này.

## Measurement honesty

- Mọi số trong `results/` là SYNTHETIC DEMO.
- Không dùng kết quả demo để quyết định ngưỡng pilot mà không có dữ liệu
  thật.
