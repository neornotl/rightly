# OPENCODE PREPARATION REPORT — Tiếng Làng v4.0

Generated: 2026-08-07 (UTC) · Machine: Windows 10, Python 3.14.5,
Intel Core i7-10510U, 15.8 GB RAM · Repo root: `C:\Users\laptopppp\intel`

> Tóm tắt: repository MVP hoàn chỉnh, mock slice chạy đầu-cuối, 52 test xanh,
> lint sạch, eval R1-R4 chạy với fixture SYNTHETIC, preflight 9/9 PASS.
> Mọi số liệu đều là **SYNTHETIC DEMO - NOT PILOT RESULTS**.

## 1. Đã làm (theo phase)

- **P0 Discovery**: môi trường đã kiểm tra (chi tiết `docs/assumptions.md`);
  thư mục trống + an toàn → `git init`; không xóa file nào (không có file sẵn).
- **P1 Scaffold**: toàn bộ cấu trúc repo; config env-driven có validate +
  redaction; schemas dataclass (stdlib); logging JSONL ẩn danh + scrub + delete.
- **P2 Mock vertical slice**: MockASR → BM25 (pure Python + stopwords + token
  overlap gate) → SafetyRouter (RED→ORANGE→scope→sufficiency→LLM optional) →
  MockLLM (deterministic, bám nguồn) → MockTTS; CLI state machine đầy đủ;
  52 test pass.
- **P3 Real adapters**: PhoWhisper / Gemini / Groq / Edge-TTS — lazy import,
  báo lỗi rõ khi thiếu dep/key. Edge-TTS đã smoke-test thật (8.2s + cache hit).
  faster-whisper đã cài trong venv; **model chưa tải** (quyết định chủ động).
- **P4 UI**: Streamlit `app/ui.py` — boot OK headless; hiển thị trạng thái,
  zone/action, answer, citation, sources, latency, nút repeat/slower/delete,
  cảnh báo DEMO.
- **P5 Eval**: `eval/wer.py`, `retrieval.py`, `routing.py`, `latency.py`,
  `run_all.py` — toàn bộ output tại `results/` có watermark.
- **P6 Docs & preflight**: README + 14 docs; `scripts/preflight.py` 9/9 PASS.
- **P7**: báo cáo này.

## 2. Cấu trúc repo (tóm tắt)

```
app/          core: config, schemas, asr/, retrieval/, llm/, safety/, tts/,
              dialogue/, pipeline.py, cli.py, ui.py
data/         sources (DEMO/SYNTHETIC), chunks, metadata.csv, eval fixtures, schemas
eval/         R1-R4 scripts + run_all
tests/        7 test files (52 tests)
scripts/      check_environment, ingest, validate_data, run_mock_demo,
              scrub_logs, preflight
docs/         15 tài liệu
results/, logs/  (gitignored, output eval)
```

## 3. Command chính

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/ingest_documents.py
.\.venv\Scripts\python.exe scripts/run_mock_demo.py      # demo đầu-cuối
.\.venv\Scripts\python.exe -m app.cli                    # CLI tương tác
.\.venv\Scripts\python.exe -m pytest                     # test
.\.venv\Scripts\python.exe -m ruff check . && ruff format --check .
.\.venv\Scripts\python.exe -m eval.run_all               # eval R1-R4
.\.venv\Scripts\python.exe scripts/preflight.py          # gate tổng hợp
.\.venv\Scripts\python.exe -m streamlit run app/ui.py    # UI
```

(Makefile có sẵn cho Unix; Windows dùng lệnh python tương đương.)

## 4. Test result (2026-08-07)

`pytest -q`: **52 passed** (config, retrieval, safety router, pipeline mock
end-to-end + privacy/audio, schemas, eval fixtures, state machine, LLM
source-id guard, WER/scrub/UTF-8). `ruff check`: clean. `ruff format --check`: clean.

## 5. Eval demo result (SYNTHETIC)

| Metric | Value |
|---|---|
| R1 WER (fixture 6 case) | 0.0769 (1 insertion / 12 tokens) |
| R2 Retrieval top-1 / MRR (dev, 6 case) | 1.0000 / 1.0000 |
| R3 Routing zone / action (test, 6 case) | 1.0000 / 1.0000 |
| R3 RED false-safe rate | 0.0 |
| R3 safe false-refusal rate | 0.0 |
| R4 Latency total p50 (fixture giả lập) | 5400.6 ms — KHÔNG phải đo thật |

Chi tiết: `results/evaluation_report.md` + các file `results/*_summary.json`.

## 6. Thành phần THẬT vs MOCK

| Thành phần | Trạng thái |
|---|---|
| BM25 retrieval | THẬT (pure Python) |
| Safety routing | THẬT (rule + policy, chưa review chuyên gia) |
| Logging/scrub/delete | THẬT |
| Config/schemas/state machine | THẬT |
| Eval R1-R4 | THẬT (fixture giả) |
| ASR | MOCK (MockASR). Adapter PhoWhisper đã cài dep, model CHƯA tải |
| LLM | MOCK (MockLLM). Gemini/Groq adapter chưa test do không có key |
| TTS | MOCK (MockTTS). Edge-TTS đã smoke-test thật 1 lần |
| UI | THẬT (Streamlit, boot OK) |

## 7. Thiếu hụt (dependency / key / model)

- `GEMINI_API_KEY`, `GROQ_API_KEY`: chưa có → LLM cloud chưa kiểm thử thật.
- PhoWhisper model weights: chưa tải (cần quyết định size + đo benchmark,
  xem `docs/hardware_benchmark_plan.md`).
- Số liên hệ chính thức (hotline/one-stop): placeholder `1900XXXX` —
  **PHẢI XÁC MINH**.
- Audio thật để đo WER: chưa có.

## 8. Rủi ro chính

1. Rule an toàn là heuristic chưa qua review chuyên gia tiếng Việt (Cao).
2. Corpus demo 1 nguồn → mọi kết luận hiệu năng không đại diện (Cao).
3. LLM cloud chưa kiểm thử (injection, schema) (Vừa).
4. Scrub logs heuristic, không phải xóa dữ liệu pháp lý (Vừa).
5. Windows/Python 3.14 chưa có CI Linux xác nhận (Thấp-Vừa).

## 9. Việc T/C/P cần làm tiếp theo

- **P (Project lead)**: xác minh kênh chính thức; duyệt consent form pilot;
  quyết định model PhoWhisper + máy pilot.
- **T (Team)**: review + mở rộng rule-set an toàn; benchmark hardware thật;
  fixture threat test cho Gemini/Groq; corpus thật (xã pilot) có kiểm duyệt.
- **C (Community)**: đóng góp fixture WER đa giọng; review docs/threat model;
  góp ý stopwords BM25.

## 10. Gate status

| Gate | Nội dung | Status |
|---|---|---|
| A — Repo | preflight 9/9, tests xanh, eval demo có report, docs đủ | ✅ DONE |
| B — An toàn | rule review chuyên gia, kênh xác minh, threat test | ⏳ TODO |
| C — Pilot | 8-10 người theo `docs/pilot_protocol.md` | ⏳ TODO |
| D — Mở rộng | quyết định dựa trên pilot (KHÔNG dùng synthetic) | ⏳ TODO |

## 11. Ghi chú khác

- Git: repo đã `git init` nhưng **chưa commit** (theo quy tắc không commit khi
  chưa được yêu cầu). Sẵn sàng commit khi team xác nhận.
- Không có API key thật nào trong source/log; secret scan sạch.
- Kết quả demo KHÔNG được trình bày như kết quả pilot.
