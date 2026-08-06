# Rubric evidence matrix (VAIIF26)

Ánh xạ từng tiêu chí đánh giá dự án tới: Claim / Evidence / Status /
Owner (T=Team, C=Community, P=Project lead) / Risk.

| # | Tiêu chí (VAIIF26) | Claim | Evidence file | Status | Owner | Risk |
|---|---|---|---|---|---|---|
| 1 | Kiến trúc module hóa | Adapter cho ASR/LLM/TTS/Retrieval, interface tách implementation | `app/asr/base.py`, `app/llm/base.py`, `app/tts/base.py`, `app/retrieval/base.py`, `docs/architecture.md` | DONE | T | Thấp |
| 2 | Mock-first, chạy không key | Mock slice chạy đầu-cuối không key/model | `scripts/run_mock_demo.py`, `tests/test_pipeline_mock.py` | DONE | T | Thấp |
| 3 | Không gửi audio cloud | Default không có upload audio | `app/pipeline.py`, `docs/threat_model.md` (T3) | DONE | T | Thấp |
| 4 | Safety routing hybrid | Rule RED trước LLM, LLM advisory | `app/safety/router.py`, `tests/test_safety_router.py` | DONE | T | Thấp |
| 5 | Không source = không trả lời | REFUSE khi thiếu nguồn | `tests/test_safety_router.py::test_insufficient_source_refuses` | DONE | T | Thấp |
| 6 | LLM không bịa citation | source_ids bị chặn | `app/llm/base.py::enforce_source_ids`, `tests/test_eval_and_machine.py` | DONE | T | Thấp |
| 7 | WER có thể tái tạo | R1 metric + fixture | `eval/wer.py`, `data/eval/wer_dev.jsonl`, `results/wer_summary.json` | DONE | T | Thấp |
| 8 | Retrieval metric | R2 top-1/hit@k/MRR | `eval/retrieval.py`, `results/retrieval_summary.json` | DONE | T | Thấp |
| 9 | Routing metric + false-safe | R3 confusion + false-safe RED = 0 | `eval/routing.py`, `results/routing_summary.json` | DONE | T | Thấp |
| 10 | Latency metric | R4 P50/P90/max, hold so sánh | `eval/latency.py`, `results/latency_summary.json` | DONE | T | Vừa (fixture chưa phải đo thật) |
| 11 | Eval demo không giả pilot | Watermark bắt buộc | `eval/common.py::WATERMARK`, `results/evaluation_report.md` | DONE | T | Thấp |
| 12 | Privacy mặc định | Không lưu transcript, xóa audio, log ẩn danh | `app/config.py`, `app/logging_utils.py`, `tests/test_pipeline_mock.py`, `tests/test_privacy_logging.py` | DONE | T | Thấp |
| 13 | Scrub logs heuristic | Scrubbing + giới hạn rõ | `scripts/scrub_logs.py`, `docs/privacy_deletion_policy.md` | DONE | T | Vừa |
| 14 | Không hard-code số khẩn cấp chưa xác minh | Placeholder config | `.env.example`, `app/config.py` | DONE | P | Vừa — PHẢI XÁC MINH |
| 15 | Demo data ghi nhãn | is_demo + watermark | `data/sources/DEMO_SOURCE.md`, `scripts/validate_data.py` | DONE | T | Thấp |
| 16 | Rule-set review chuyên gia tiếng Việt | Chưa review | `docs/limitations.md` #3 | TODO | T | Cao |
| 17 | Kênh chính thức xác minh | Số hotline/one-stop thật | `.env.example` placeholder | TODO | P | Cao |
| 18 | Pilot 8-10 người | Theo protocol | `docs/pilot_protocol.md` | TODO | P/T | Cao |
| 19 | Hardware benchmark thật (PhoWhisper) | Đo latency/mem | `docs/hardware_benchmark_plan.md` | TODO | T | Vừa |
| 20 | LLM cloud test (injection, schema) | Fixture cho gemini/groq | `docs/threat_model.md` T1/T5 | TODO | T | Vừa |
| 21 | Docs đầy đủ | README + 14 docs | `docs/` | DONE | T | Thấp |
| 22 | Quality gates | pytest/ruff/preflight | `scripts/preflight.py`, `Makefile` | DONE | T | Thấp |
