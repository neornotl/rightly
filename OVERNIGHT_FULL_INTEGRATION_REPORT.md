# Overnight Full Integration Report (v4.0)

Recorded: 2026-08-07 — Tieng Làng v4.0, overnight full-integration run.
Baseline before this run: `docs/baseline_before_full_integration.md`
(checkpoint commit `ccd2aab`, tag `before-full-integration-v4`).

Machine: Windows 10 (build 19045) · Python 3.14.5 · Intel Core i7-10510U
(4C/8T, no GPU) · 15.81 GB RAM · ~20.6 GB free disk.

## 1. What was built (P0-P8)

| Phase | Deliverable | Status |
|---|---|---|
| P0 | Real ASR: PhoWhisper models downloaded, smoke-tested on CPU | done |
| P1 | Real LLM: Groq integration validated (8/8 queries, JSON schema OK) | done |
| P2 | Real ASR eval: VIVOS test set, 30 clips, WER measured | done |
| P3 | TTS smoke (edge voice) + latency baselines | done |
| P4 | Real legal corpus: 11 official docs (vanban.chinhphu.vn) crawled; 9 scanned PDFs OCR'd; **1013 chunks** | done |
| P5 | Hybrid RAG: BM25 + dense (e5-small) + RRF, answerability gate, ablation | done |
| P6 | Citation validator: expiry / unsupported / unknown sources + policy downgrade | done |
| P7 | Full-system journeys J1-J7 with redacted traces | done |
| P8 | This report + `results/overnight_summary.json` | done |

Quality gates: **60 pytest passed · ruff clean · preflight 9/9 PASS**.

## 2. Corpus (P4)

- 11 official documents crawled from vanban.chinhphu.vn (registry:
  `data/source_registry.csv`, 11/11 ready): Luật Hộ tịch, Luật HN&GĐ, Luật Cư
  trú, Luật Căn cước, Luật Công chứng (mới), NĐ 123/2015, NĐ 126/2014,
  NĐ 154/2024, NĐ 62/2021 (hết hiệu lực — kept as a validator test case),
  NĐ 07/2025, NĐ 104/2025.
- Old official PDFs are **scanned images**: pypdf/pdfminer yield 0 chars;
  **EasyOCR (vi)** on CPU ~20-26 s/page, 9 docs in ~94 min (idempotent
  per-page cache in `data/private_cache/vbpq/_ocr_cache.jsonl`). 2 PDFs are
  text-based (Luật 26/2023, Luật 46/2024).
- OCR quality is usable for retrieval; residual confusions exist
  ("đăng ký"→"đẳng ký", "người"→"nguời") — see limitations.
- Outputs: `data/sources_real/*.md`, `data/chunks/real_chunks.jsonl` (1013 chunks).

## 3. Retrieval (P5)

Real-corpus ablation, 8 queries with manual source-level relevance labels
(`results/retrieval_ablation.json`; Q6/Q7 have no relevant source — they are
out-of-corpus "no-answer expected" probes):

| variant | r@5 | nDCG@5 | noise@5 | empty | lat (ms) |
|---|---|---|---|---|---|
| bm25 | 0.5104 | 0.5372 | 0.350 | 0 | 822 |
| dense (e5-small) | 0.5938 | 0.5996 | 0.325 | 0 | 21 |
| **hybrid_rrf (default)** | **0.5938** | **0.6199** | **0.075** | 2 | 997 |
| hybrid_rerank (mmarco) | 0.6042 | 0.6152 | 0.000 | 2 | 3312 |

Reranker note: tested `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` (all logits
negative on this domain — miscalibrated for Vietnamese legal text) and
`namdp-ptit/ViRanker` (sigmoid scores, but false-negatives in-domain queries
and ~13 s/query on CPU). **Default: no rerank; RRF ordering is already strong.**

Answerability gate (new, `app/retrieval/hybrid_retriever.py`): a query is
answered only if `BM25 top1 ≥ 12.2 OR dense top1 ≥ 0.88` (calibrated on the
real corpus; env-tunable `RETRIEVAL_BM25_GATE` / `RETRIEVAL_DENSE_GATE`).
Result: 6/6 in-corpus queries pass, 2/2 out-of-corpus (hộ chiếu, phạt khai
sinh quá hạn) correctly produce no chunks → ORANGE/REFUSE.

## 4. Citation validator (P6)

`app/validation/citation_validator.py` checks every cited source_id:
- **outdated**: document expired before today (curated `data/law_status.json`),
  flagged with its replacement — **NĐ 62/2021 hết hiệu lực 10/01/2025,
  thay thế bởi NĐ 154/2024** (verified case);
- **unsupported**: cited source not among retrieved chunks;
- **unknown**: source_id not in registry.

Failures downgrade the answer to ORANGE/REFUSE
(`CITATION_OUTDATED` / `CITATION_UNSUPPORTED`), logged as
`citation_rejected` session event. Report: `results/citation_validator_report.json`
(5 cases: 3 reject / 2 accept).

## 5. Full-system journeys (P7)

`results/full_system_trace_redacted.jsonl` — 7/7 behave as expected, live
pipeline (hybrid retrieval → safety routing → Groq LLM → citation validation →
TTS mock). Free-text fields are scrubbed; no secrets, no raw audio.

| journey | query | decision | chunks | latency |
|---|---|---|---|---|
| J1 | đăng ký khai sinh | YELLOW/ANSWER | 5 | ~2.3 s |
| J2 | hồ sơ kết hôn | YELLOW/ANSWER | 5 | ~1.7 s |
| J3 | đăng ký tạm trú | YELLOW/ANSWER | 5 | ~1.5 s |
| J4 | cấp lại giấy khai sinh | YELLOW/ANSWER | 5 | ~1.0 s |
| J5 | xác nhận tình trạng hôn nhân | YELLOW/ANSWER | 5 | ~2.5 s |
| J6 | thay đổi họ tên | YELLOW/ANSWER | 5 | ~14 s (Groq variance) |
| J7 | hồ sơ hộ chiếu (out-of-corpus) | ORANGE/REFUSE | 0 | ~0.5 s |

All J1-J6 answers passed citation validation (cited sources are retrieved
real documents). J7 refused without an LLM call (gate → INSUFFICIENT_SOURCE).

## 6. ASR / WER (P2)

PhoWhisper-base on 30 VIVOS test clips, CPU: **WER 17.98%**
(median 15.38%, p90 33.63%) — `results/wer_summary_real_vivos.json`.

## 7. Limit compliance

- Downloads: ≈6.0 GB total this run (HF models incl. ViRanker 2.3 GB
  evaluated-then-rejected; VIVOS archive 1.37 GB, only 30/125 clips used).
  Cleanup applied: ViRanker + VIVOS archive deleted → **≈2.5 GB retained**.
- LLM calls: ≈31/60 used (est.).
- No secrets committed (`.env` gitignored, preflight secret-scan clean).
- No raw audio in repo (`*.wav` ignored; `data/private_cache/` now gitignored).

## 8. Known limitations

- OCR residual errors in old scanned PDFs (mitigated by redundancy of 1013
  chunks; flagged `ocr_pending_review` in registry).
- Answerability gate thresholds are calibrated on 8 queries — may need
  recalibration for other question families.
- Groq answer latency varies (1-14 s); no timeout/caching yet.
- Hotline/one-stop channel values are placeholders (`1900XXXX`) — must be
  verified by the human team before deployment (config placeholders).
- LLM sometimes cites a single source for a multi-part question (J4 cited
  only `nd07_2025`); validator allows it because the source was retrieved.

## 9. Reproduce

```powershell
python scripts/crawl_vbpl.py --no-download   # rebuild registry (P4)
python scripts/ocr_vbpl.py                   # OCR scanned PDFs (idempotent)
python scripts/eval_retrieval_ablation.py    # P5 ablation
python scripts/eval_citation_validator.py    # P6 report
python scripts/run_full_system_trace.py      # P7 journeys
python scripts/build_overnight_summary.py    # P8 summary
python scripts/preflight.py                  # 9/9 gates
pytest tests -q                              # 60 tests
```

## 10. Artifact index

- `results/overnight_summary.json` — machine-readable summary of everything.
- `results/wer_summary_real_vivos.json`, `results/retrieval_ablation.json`,
  `results/citation_validator_report.json`, `results/full_system_trace_redacted.jsonl`
- `data/source_registry.csv`, `data/sources_real/*.md`,
  `data/chunks/real_chunks.jsonl`, `data/law_status.json`
- New code: `app/retrieval/hybrid_retriever.py`, `app/validation/`,
  `scripts/crawl_vbpl.py`, `scripts/ocr_vbpl.py`, `scripts/eval_retrieval_ablation.py`,
  `scripts/eval_citation_validator.py`, `scripts/run_full_system_trace.py`,
  `scripts/build_overnight_summary.py`, `tests/test_citation_validator.py`
