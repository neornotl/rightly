# Deployment strategy (draft — ngoài phase preparation)

## Mục tiêu giai đoạn

- Phase preparation (hiện tại): repo MVP + eval synthetic.
- Phase pilot (T/C/P quyết định): 8-10 người, local laptop.
- Phase community pilot (tùy chọn): nhiều xã, dữ liệu thật đã kiểm duyệt.
- Phase production: điện thoại/SIM (adapter, ngoài phạm vi hiện tại).

## Các quyết định trước khi deploy

1. **Kênh chính thức xác minh**: hotline, bộ phận một cửa — cập nhật vào
   config (hiện là placeholder `1900XXXX`).
2. **Nguồn dữ liệu thật**: import có duyệt người, ngày cập nhật,
   `is_demo=false`, giữ lịch sử hiệu lực.
3. **Máy chạy pilot**: laptop Intel Core i7-10510U (4C/8T, 15.8GB RAM) —
   đủ cho PhoWhisper small int8 CPU; đo theo `hardware_benchmark_plan.md`.
4. **Storage & logs**: giữ log ẩn danh tại máy operator; không cloud mặc định.
5. **Human-in-the-loop**: RED/ORANGE → chuyển operator / kênh chính thức.

## Kiến trúc đích (sau pilot)

```
Laptop operator (core pipeline) ← microphone
    └─ adapter điện thoại (TBD): Asterisk/FreeSWITCH — NGOÀI PHẠM VI phase này
```

## Rollout plan (đề xuất)

1. Gate A (repo): preflight pass, tests xanh, eval demo có report. **DONE.**
2. Gate B (an toàn): rule review chuyên gia + kênh xác minh + threat test.
3. Gate C (pilot): 8-10 người theo `pilot_protocol.md`.
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
