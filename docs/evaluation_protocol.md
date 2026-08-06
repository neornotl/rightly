# Evaluation protocol (R1-R4)

## Nguyên tắc

1. Mọi kết quả demo ghi watermark **SYNTHETIC DEMO - NOT PILOT RESULTS**.
2. Kết quả tái tạo được bằng lệnh rõ ràng (dưới đây).
3. Không dùng confidence score (chưa calibration).
4. Không chỉnh fixture để "đẹp" kết quả; thay đổi fixture phải là thay đổi
   chủ ý, có commit message rõ.

## R1 — WER

- Metric: WER (token-level, Levenshtein), substitutions/insertions/deletions.
- Normalize: NFC, lowercase, collapse whitespace, bỏ punctuation.
- Báo cáo tổng + theo `accent_group`.
- Lệnh: `python -m eval.wer --input data/eval/wer_dev.jsonl`
  (output `results/wer_results.csv`, `results/wer_summary.json`).
- Ngưỡng mục tiêu (pilot, chưa đặt cho demo): thảo luận với team ASR.

## R2 — Retrieval

- Metrics: top-1 accuracy, hit@3, hit@5, MRR.
- Lệnh: `python -m eval.retrieval --input data/eval/retrieval_test.jsonl`
- Tiêu chí qua cổng: top-1 ≥ 0.8 trên test (synthetic, tham chiếu thôi).

## R3 — Routing

- Metrics: zone accuracy, action accuracy, confusion matrix,
  false-safe rate (RED → không YELLOW), false-refusal rate (YELLOW → không
  REFUSE/CLARIFY/ESCALATE).
- Lệnh: `python -m eval.routing --input data/eval/routing_test.jsonl`
- Bắt buộc: false-safe rate RED = 0 trên mọi fixture; nếu > 0 → blocker.

## R4 — Latency

- Metrics: P50, P90, max, mean theo stage (asr/retrieval/llm/tts/total).
- Hỗ trợ so sánh `hold_message=true/false`.
- Lệnh: `python -m eval.latency --input data/eval/latency_dev.jsonl`
- Lưu ý: fixture latency là số liệu giả lập; phép đo thật ở
  `docs/hardware_benchmark_plan.md`.

## Chạy toàn bộ

```bash
python -m eval.run_all
```

Sinh `results/wer_results.csv`, `wer_summary.json`, `retrieval_results.csv`,
`retrieval_summary.json`, `routing_results.csv`, `routing_summary.json`,
`latency_results.csv`, `latency_summary.json`, `evaluation_report.md`.

## Watermark policy

- Mọi summary JSON chứa `"note": "SYNTHETIC DEMO - NOT PILOT RESULTS"`.
- `evaluation_report.md` ghi chú rõ ở đầu.
- Bất kỳ báo cáo ngoài repo nào trích số liệu đều phải kèm watermark.
