# Hardware benchmark plan

> **Kế hoạch đo, không phải kết quả đo.** Chỉ công bố số liệu từ output benchmark có thể truy vết; thông số máy và giả định trong file này có thể đã cũ.

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
| NPU | KHÔNG có — máy này chỉ chạy OpenVINO-CPU; NPU chỉ có trên máy AI PC mượn |
| faster-whisper | 1.2.1 (ctranslate2) |

## Trạng thái 09/08 (F4-prep)

- Script đo đã sẵn: `scripts/benchmark_openvino.py` — detect CPU/NPU, ASR
  latency + WER + ghi `results/hardware_benchmark.csv` (append, không chứa audio).
- Chưa có audio thật local (VIVOS chưa tải) → chạy lần đầu khi có máy mượn
  hoặc khi P/C đưa audio pilot (13/08).
- Claim trung thực: CHƯA có số liệu OpenVINO; không claim NPU trên máy này.

## Quy trình đo

1. Cài `faster-whisper` + tải model có chủ đích (chưa làm trong phase này):
   - `phowhisper-small` (khuyến nghị thử đầu tiên, ~500MB)
   - `phowhisper-base` nếu RAM/latency không đạt.
2. Chạy `python scripts/benchmark_openvino.py --audio <dir> --refs <jsonl>`
   hoặc để mặc định dùng VIVOS test nếu có. Ghi asr_ms, audio_seconds, wer,
   latency; tính P50/P90 bằng `eval/latency.py`.
3. Đo bộ nhớ: peak RSS bằng `psutil` hoặc Task Manager trong khi chạy.
4. Nhiệt/nguồn: máy laptop dùng pin — ghi chú.

## Intel AI PC (tùy chọn, chờ trả lời loan 12/08)

- Nếu có máy Intel AI PC (Core Ultra): chạy lại cùng script — device NPU sẽ
  được detect tự động, so sánh CPU vs NPU.
- **Không claim OpenVINO**: chưa benchmark; chỉ ghi số liệu thực đo.

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
