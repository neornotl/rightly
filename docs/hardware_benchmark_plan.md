# Hardware benchmark plan

Mục tiêu: đo latency + bộ nhớ thật của pipeline trên laptop chuẩn (general)
và máy Intel AI PC (nếu có) — **trước khi** chọn model PhoWhisper và trước
khi pilot.

## Máy baseline (đã biết)

| Item | Giá trị |
|---|---|
| OS | Windows 10 (19045) |
| CPU | Intel Core i7-10510U (Comet Lake, 4C/8T, 1.8GHz base) |
| RAM | 15.8 GB |
| Python | 3.14.5 |
| GPU | Không (CPU-only) |
| faster-whisper | 1.2.1 (ctranslate2) |

## Quy trình đo

1. Cài `faster-whisper` + tải model có chủ đích (chưa làm trong phase này):
   - `phowhisper-small` (khuyến nghị thử đầu tiên, ~500MB)
   - `phowhisper-base` nếu RAM/latency không đạt.
2. Script đo (roadmap — TODO): dùng 10 file audio thật 5-15s, ghi
   asr_ms, retrieval_ms, llm_ms, tts_ms, total_ms; tính P50/P90/max bằng
   `eval/latency.py`.
3. Đo bộ nhớ: peak RSS bằng `psutil` hoặc Task Manager trong khi chạy.
4. Nhiệt/nguồn: máy laptop dùng pin — ghi chú.

## Intel AI PC (tùy chọn, chưa có)

- Nếu có máy Intel AI PC (Core Ultra): chạy lại cùng script, so sánh.
- **Không claim OpenVINO**: chưa benchmark; OpenVINO ngoài phạm vi phase này;
  chỉ ghi số liệu thực đo.

## Các biến cần ghi

- CPU model, RAM, OS, Python, model ASR (size, device, compute_type),
  num threads, audio sample rate/độ dài, thời gian đo, nhiệt độ phòng nếu ghi.

## Ngưỡng đề xuất (tham chiếu, chưa phải cam kết)

- ASR small int8 trên CPU i7-10510U: kỳ vọng < 5x thời gian audio (cần đo).
- Total pipeline mục tiêu: P90 < 15s cho câu hỏi ngắn (mock đã ~0.01s;
  latency fixture không tính).

## Output

- `results/hardware_benchmark.csv` + mục trong `evaluation_report.md`
  (watermark: synthetic trừ khi đo thật).
