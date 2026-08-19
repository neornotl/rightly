# Baseline before full integration (overnight v4)

> **Baseline lịch sử.** Snapshot trước đợt tích hợp; không phản ánh corpus, test suite hay cấu hình hiện tại.

Recorded: 2026-08-07, before starting overnight full integration.
Machine: Windows 10 (build 19045), Python 3.14.5, Intel Core i7-10510U (4C/8T, no GPU),
15.81 GB RAM, free disk ~20.5 GB.

## Verification results (all green)

- `pytest`: 52 passed
- `ruff check`: clean
- `scripts/preflight.py`: 9/9 PASS (python version, config mock, 29 modules import,
  data validation chunks: 4 records / sources: ['demo_binhminh_procedures'],
  secret scan clean, pytest, ruff, mock demo, eval R1-R4)
- Git: 1 existing commit `7058b42` ("checkpoint: completed OpenCode preparation phases 0-7"),
  working tree clean, branch `master`

## Baseline metrics (mock slice, fixtures)

- WER (R1, synthetic fixture): 0.0769 (not real ASR yet)
- Retrieval top-1 (R2): 1.0
- Routing zone (R3): 1.0
- RED false-safe (R4): 0.0 (no false positives)
- Latency p50 (R4): 5400.6 ms (synthetic fixture with slow-motion factor)

## What is NOT in the baseline yet (scope of this overnight run)

- Real ASR model (PhoWhisper-base) — not downloaded
- Real LLM API calls (Groq) — no API key configured
- Real Vietnamese audio dataset — none downloaded
- Curated official legal/procedure corpus — only demo source
- Hybrid RAG (dense + RRF + reranker) — BM25 only
- Citation validator — not implemented

## Checkpoint

Git tag `before-full-integration-v4` created at commit of this doc, so all work
can be reverted/compared against this exact point.
