# Deployment strategy (đã chốt hướng — 08/08/2026)

## QUYẾT ĐỊNH CỦA T (08/08/2026): CLOUD-FIRST + LOCAL LÀ PHƯƠNG ÁN CHUYÊN NGHIỆP

- **Cloud (chính)**: nguồn vốn + giới hạn phần cứng team → chạy LLM cloud
  (Groq/Gemini) cho public link + pilot. Kèm điều kiện bắt buộc:
  PII scrub trước outbound, secrets an toàn (Streamlit Secrets, không debug),
  rate limit, log retention.
- **Local (phương án phát triển chuyên nghiệp + bảo mật hơn)**: giữ là lựa
  chọn triển khai cho tổ chức (on-prem, dữ liệu không rời máy) — mock mode
  vẫn là fallback khẩn cấp. Local = "tích hợp với tổ chức sử dụng" (đáp ứng
  yêu cầu kiểm soát dữ liệu), cloud = vận hành nhanh, chi phí thấp cho demo/pilot.

## Mục tiêu giai đoạn

- Phase preparation (hiện tại): repo MVP + eval synthetic.
- Phase pilot (T/C/P quyết định): 8-10 người — cloud LLM + local fallback.
- Phase community pilot (tùy chọn): nhiều xã, dữ liệu thật đã kiểm duyệt.
- Phase production: điện thoại/SIM (adapter, ngoài phạm vi hiện tại).

## Các quyết định trước khi deploy

1. **Kênh chính thức xác minh**: hotline, bộ phận một cửa — cập nhật vào
   config (hiện là placeholder `1900XXXX`).
2. **Nguồn dữ liệu thật**: import có duyệt người, ngày cập nhật,
   `is_demo=false`, giữ lịch sử hiệu lực.
3. **Máy chạy pilot**: laptop Intel Core i7-10510U (4C/8T, 15.8GB RAM) —
   đủ cho PhoWhisper small int8 CPU; đo theo `hardware_benchmark_plan.md`.
4. **Storage & logs**: giữ log ẩn danh tại máy operator; retention 30 ngày;
   không cloud mặc định (chỉ transcript đã scrub nếu cần).
5. **Human-in-the-loop**: RED/ORANGE → chuyển operator / kênh chính thức.
6. **Cloud LLM**: scrub PII trước outbound (bắt buộc, `app/privacy/`); dùng
   secrets an toàn; rate limit + giới hạn ký tự; nếu cloud fail → tự fallback
   Mock/local, không crash.

## Kiến trúc đích (sau pilot)

```
Cloud path (chính):
  user voice → ASR (local PhoWhisper) → scrub PII → LLM cloud (Groq/Gemini)
  → CitationValidator (local) → TTS → trả lời
Local path (tổ chức / fallback):
  toàn bộ pipeline local, LLM Mock hoặc model local (OpenVINO khi có AI PC)
  → dữ liệu không rời máy → phù hợp tích hợp nội bộ tổ chức
```

## Rollout plan (đề xuất)

1. Gate A (repo): preflight pass, tests xanh, eval demo có report. **DONE.**
2. Gate B (an toàn): rule review chuyên gia + kênh xác minh + threat test.
3. Gate C (pilot): 8-10 người — cloud LLM (đã scrub PII), fallback local;
   theo `pilot_protocol.md`.
4. Gate D (mở rộng): quyết định T/C/P dựa trên kết quả pilot (không dùng
   synthetic).

## Monitoring (khi có pilot)

- Latency thật (R4 trên dữ liệu pilot), WER nhóm giọng, routing confusion,
  tỷ lệ REFUSE đúng/sai, số lần chuyển người thật.
- Không dùng confidence %; dùng zone + reason codes.

## Rollback

- Mock mode = luôn có sẵn fallback.
- Ngắt kênh audio adapter không ảnh hưởng core pipeline.
- Dữ liệu nguồn sai → gỡ source_id, pipeline tự REFUSE cho câu liên quan.
