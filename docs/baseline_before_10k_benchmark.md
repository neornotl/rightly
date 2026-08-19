# Baseline Before 10k Benchmark Generation — Rightly

> **Baseline lịch sử.** Các số liệu, file count và kết quả kiểm tra bên dưới chỉ đúng tại thời điểm ghi nhận; không dùng làm KPI hoặc trạng thái hiện hành.

Generated: 2026-08-09 (UTC) · Machine: Windows 10, Python 3.14.5, Intel Core i7-10510U, 15.8 GB RAM · Repo root: `C:\Users\laptopppp\intel`

---

## 1. Git Status

- Branch: `master` (ahead of `origin/master` by 3 commits)
- **Modified files (24)**: .streamlit/secrets.toml.example, QUESTS.md, app/cli.py, app/config.py, app/dialogue/commands.py, app/dialogue/state_machine.py, app/llm/groq_llm.py, app/pipeline.py, app/ui.py, data/chunks/demo_chunks.jsonl, data/eval/latency_dev.jsonl, data/eval/wer_dev.jsonl, docs/MASTER.md, docs/competition_aiif26.md, docs/hardware_benchmark_plan.md, docs/submission_checklist.md, docs/team_status.md, requirements.txt, scripts/council_models.py, scripts/round12_debate.py, scripts/round13_debate.py, tests/test_eval_and_machine.py, tests/test_pipeline_mock.py
- **Untracked files (27)**: app/contacts.py, app/faq.py, app/forms.py, app/llm/fallback.py, app/ratelimit.py, data/faq.json, debate_output/*, docs/deploy_public.md, docs/fit_assessment_aiif26.md, privacy_checking.md, project_review.md, scripts/answer_report.py, scripts/benchmark_openvino.py, scripts/log_pilot_metrics.py, scripts/predeploy_check.py, scripts/round14_debate.py, scripts/round15_debate.py, scripts/round16_debate.py, scripts/round17_debate.py, scripts/vision_reader.py, tests/test_demo_connect.py, tests/test_f4_f5_cloud.py
- **No secrets detected in tracked files** (`.env` is gitignored)

---

## 2. Test / Lint / Format Status

| Check | Result | Details |
|-------|--------|---------|
| `pytest tests -q` | **PASSED** | 112 tests passed (note: earlier snapshot claimed 52/60; actual count is 112) |
| `ruff check .` | **PASSED** | Clean |
| `ruff format --check .` | **FAILED** | 34 files would be reformatted (whitespace/line-length only; no logic changes) |
| `preflight.py` | **PARTIAL** | Started but timed out at 120s; early checks passed (python version, config loads) |

**Note**: The format failures are purely stylistic (line wrapping, trailing commas, spacing). No functional code changes required.

---

## 3. Verified Project State (from Repo, Not Snapshots)

### 3.1 Architecture Components (Verified in Code)

| Component | Status | Implementation |
|-----------|--------|----------------|
| **ASR** | Adapter ready, model NOT loaded | `app/asr/phowhisper_asr.py` (lazy import); `faster-whisper` in requirements; model weights not downloaded |
| **Retrieval** | Hybrid BM25 + Dense (e5-small) + RRF | `app/retrieval/hybrid_retriever.py` (default); BM25 pure Python in `bm25_retriever.py` |
| **Answerability Gate** | Calibrated on 8 queries | `RETRIEVAL_BM25_GATE=12.2`, `RETRIEVAL_DENSE_GATE=0.88` (env-tunable) |
| **Safety Router** | Rule-based (RED→ORANGE→YELLOW) + optional LLM classifier | `app/safety/router.py`, `app/safety/rules.py`, `app/safety/policy.py` |
| **Citation Validator** | Expiry / unsupported / unknown | `app/validation/citation_validator.py` + `data/law_status.json` |
| **LLM** | MockLLM (default), Groq, Gemini adapters | `app/llm/mock_llm.py`, `groq_llm.py`, `gemini_llm.py`, `fallback.py` |
| **TTS** | MockTTS (default), Edge-TTS adapter | `app/tts/mock_tts.py`, `edge_tts.py` |
| **Pipeline** | Full end-to-end | `app/pipeline.py` |
| **CLI / UI** | State machine CLI + Streamlit | `app/cli.py`, `app/ui.py` |
| **Privacy Scrubber** | Heuristic PII scrub | `app/privacy/scrubber.py` |
| **Rate Limiter** | Token bucket per key | `app/ratelimit.py` |
| **Voice FAQ** | 11 scenarios, keyword match | `app/faq.py` + `data/faq.json` |

### 3.2 Corpus Status (Verified from `data/source_registry.csv` and `data/law_status.json`)

| Metric | Value |
|--------|-------|
| **Official legal documents** | 11 (from vanban.chinhphu.vn) |
| **Document types** | 6 Laws (Luật), 5 Decrees (Nghị định) |
| **Coverage topics** | Hộ tịch, Hôn nhân & Gia đình, Cư trú, Căn cước, Công chứng |
| **Expired document** | NĐ 62/2021 (expired 2025-01-10, replaced by NĐ 154/2024) |
| **OCR status** | 9 scanned PDFs OCR'd (EasyOCR vi, CPU ~94 min); 2 text-based PDFs |
| **Chunks** | 1,013 chunks in `data/chunks/real_chunks.jsonl` |
| **Demo synthetic source** | 1 (`demo_binhminh_procedures`, marked `is_demo=true`) |
| **Source registry status** | 11/11 `ocr_pending_review` or `pending_review` — **not yet `active_verified`** |

### 3.3 Evaluation Baselines (Verified from `results/overnight_summary.json` and Artifacts)

#### Retrieval Ablation (8 queries, manual source-level labels)

| Variant | Recall@5 | nDCG@5 | Noise@5 | Empty Retrievals | Latency (ms) |
|---------|----------|--------|---------|------------------|--------------|
| BM25 | 0.5104 | 0.5372 | 0.350 | 0 | 822 |
| Dense (e5-small) | 0.5938 | 0.5996 | 0.325 | 0 | 21 |
| **Hybrid RRF (default)** | **0.5938** | **0.6199** | **0.075** | 2 | 997 |
| Hybrid + Rerank (mmarco) | 0.6042 | 0.6152 | 0.000 | 2 | 3312 |

**Notes**: 
- Q6 (khởi sinh quá hạn) and Q7 (hộ chiếu) are out-of-corpus probes (expected_sources=[]).
- Reranker `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` miscalibrated for Vietnamese legal; `namdp-ptit/ViRanker` false negatives + 13s/query.
- **Default: Hybrid RRF without rerank.**

#### Answerability Gate
- Threshold: `BM25 top1 ≥ 12.2 OR dense top1 ≥ 0.88`
- Calibrated on **only 8 queries** — high risk of overfitting
- Results: 6/6 in-corpus pass, 2/2 out-of-corpus correctly rejected (0 false rejects)

#### Citation Validator (5 test cases)
| Case | Type | Result |
|------|------|--------|
| C1 | Outdated (ND62) | REJECT → ORANGE/REFUSE |
| C2 | Valid (ND154) | PASS |
| C3 | Unsupported | REJECT → ORANGE/REFUSE |
| C4 | Unknown source_id | REJECT → ORANGE/REFUSE |
| C5 | Multi valid | PASS |

#### Full-System Journeys (J1-J7)
| Journey | Query | Decision | Latency | Notes |
|---------|-------|----------|---------|-------|
| J1 | Đăng ký khai sinh | YELLOW/ANSWER | 2.5s | Citation OK |
| J2 | Hồ sơ kết hôn | YELLOW/ANSWER | 1.7s | Citation OK |
| J3 | Đăng ký tạm trú | YELLOW/ANSWER | 1.5s | Citation OK (includes expired ND62 chunk) |
| J4 | Cấp lại giấy khai sinh | YELLOW/ANSWER | 1.0s | Citation OK |
| J5 | Xác nhận tình trạng hôn nhân | YELLOW/ANSWER | 2.5s | Citation OK |
| J6 | Thay đổi họ tên | YELLOW/ANSWER | 14.0s | Citation OK (Groq variance) |
| J7 | Hồ sơ hộ chiếu | ORANGE/REFUSE | 0.5s | Correctly refused (insufficient source) |

#### ASR / WER (PhoWhisper-base on VIVOS 30 clips, CPU)
- **WER: 17.98%** (median 15.38%, p90 33.63%)
- **Source**: `results/wer_summary_real_vivos.json`
- **Note**: 30/125 VIVOS clips used; not pilot audio

#### Smoke Cloud Test (Groq, 12 queries)
- **12/12 passed**: 10 ANSWER, 1 REFUSE (insufficient), 1 REFUSE (illegal), 1 CLARIFY
- Latency: 300ms–57s (high variance on Groq)

---

## 4. Known Uncertainties (Per Instructions)

| Uncertainty | Current State | Verification Needed |
|-------------|---------------|---------------------|
| PhoWhisper model loaded/running? | Adapter code exists; model weights NOT downloaded | Run `scripts/smoke_phowhisper.py` |
| Audio evaluation: human vs synthetic? | **Synthetic only** (VIVOS 30 clips); no pilot audio collected | Pilot needed |
| LLM provider/model in use? | MockLLM default; Groq/Gemini adapters ready; `LLM_BACKEND` env var controls | Set `LLM_BACKEND=groq` + key |
| Groq ZDR confirmed by user? | **UNKNOWN** — not documented in repo | Ask user |
| Active verified legal sources? | **0** — all 11 sources `ocr_pending_review` / `pending_review` | C must review + approve |
| Recall@5/nDCG split? | 8 manual queries (no formal dev/test split) | Need proper split |
| Answerability threshold tuned on small sample? | **YES** — calibrated on 8 queries only | Recalibrate with more data |
| Gate B/C/D status? | **B (Safety): NOT GREEN** — rule review by VN expert pending<br>**C (Pilot): NOT GREEN** — 0/8-10 recruited<br>**D (Submission): NOT GREEN** — no evidence pack | Human review required |

---

## 5. Checkpoint Commit

```bash
git add -A
git commit -m "checkpoint: before 10k benchmark generation"
git tag before-10k-benchmark-v4
```

---

## 6. Summary for 10k Benchmark Planning

**Ready for Phase B (Source Catalog)**:
- Corpus: 11 official docs, 1,013 chunks, 1 expired doc tracked
- Retrieval: Hybrid RRF baseline established
- Safety: Router + citation validator working
- Evaluation: R1-R4 synthetic fixtures exist (but limited scope)

**Critical Gaps Before Benchmark Generation**:
1. **Source verification**: C must review 11 sources → mark `active_verified` in `law_status.json`
2. **Pilot audio**: No real user audio for WER baseline
3. **Answerability gate**: Recalibrate on larger query set
4. **Format cleanup**: Run `ruff format .` before generating benchmark code
5. **Preflight completion**: Fix timeout issue

**No inflated claims**: All metrics above are from actual repo artifacts (`results/overnight_summary.json`, `retrieval_ablation.json`, `citation_validator_report.json`, `wer_summary_real_vivos.json`), not from summary documents.
