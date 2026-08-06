# Evaluation dataset card (R1-R4 fixtures)

> Tất cả fixture trong `data/eval/` là **SYNTHETIC DEMO - NOT PILOT RESULTS**.

## R1 — WER (`data/eval/wer_dev.jsonl`)

Sinh tự động bởi `eval/run_all.py` nếu chưa có; cấu trúc:

```json
{"case_id": 1, "accent_group": "northern",
 "reference": "thủ tục cấp giấy xác nhận hộ khẩu",
 "hypothesis": "thủ tục cấp giấy xác nhận hộ khẩu"}
```

- `reference`: transcript chuẩn (chữ thường).
- `hypothesis`: transcript giả lập từ ASR (lỗi diacritics/âm tiết có chủ đích).
- `accent_group`: nhãn vùng giọng để báo cáo nhóm.

Giới hạn: không phải audio thật; chỉ kiểm tra logic metric, không phải chất
lượng ASR.

## R2 — Retrieval (`retrieval_dev.jsonl`, `retrieval_test.jsonl`)

```json
{"query": "Thủ tục cấp giấy xác nhận hộ khẩu tại xã Bình Minh?",
 "expected_source_id": "demo_binhminh_procedures", "accent_group": "standard"}
```

- Query viết theo giọng nói (diacritics đầy đủ) + biến thể nhóm giọng.
- `expected_source_id` phải tồn tại trong chunks (validate_data kiểm tra).

## R3 — Routing (`routing_dev.jsonl`, `routing_test.jsonl`)

```json
{"query": "...", "expected_zone": "YELLOW", "expected_action": "ANSWER",
 "notes": "safe grounded"}
```

- Bao phủ: safe grounded, emergency, violence/threat, legal dispute,
  out-of-scope, no-source.

## R4 — Latency (`latency_dev.jsonl`, sinh tự động)

```json
{"case_id": 0, "hold_message": true,
 "asr_ms": 2000, "retrieval_ms": 40, "llm_ms": 1500, "tts_ms": 800, "total_ms": 4800}
```

- Sinh ngẫu nhiên seed cố định (reproducible), chỉ kiểm tra bộ tổng hợp số
  liệu; **không** phải phép đo latency thật.

## Chia dev/test

- `retrieval_dev` (6), `retrieval_test` (6) — dev để tinh chỉnh, test để báo
  cáo.
- `routing_dev` (6), `routing_test` (6).
- `run_all.py` báo cáo trên `retrieval_dev` + `routing_test` + WER dev +
  latency dev.

## Schema validation

`scripts/validate_data.py` kiểm tra fixture khớp
`data/schemas/retrieval_case.schema.json` / `routing_case.schema.json`.
