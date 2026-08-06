# Assumptions and Decisions (Phase 0)

This document records environment findings and design decisions made during
preparation. Everything here is subject to review before pilot deployment.

## Environment (2026-08-06)

| Item | Value |
|------|-------|
| OS | Windows 10 (10.0.19045) |
| Python | 3.14.5 (C:\Python314) |
| CPU | Intel Core i7-10510U @ 1.80 GHz (Comet Lake, 4C/8T) |
| RAM | 15.8 GB |
| Working dir | `C:\Users\laptopppp\intel` (empty at start, no nested repo) |
| Internet | Available (pypi.org reachable) |
| Preinstalled (global) | faster-whisper 1.2.1, ctranslate2, onnxruntime, pydantic, numpy |

## Decisions

1. **Working directory**: The directory `intel` was empty, so the repository
   was created in place. Git was initialized here (no nested repo detected).
2. **Schemas**: Python `dataclasses` (standard library) instead of Pydantic for
   core schemas, so the mock vertical slice runs with **zero third-party
   dependencies**. Pydantic is not required by the core.
3. **Mock mode**: Full end-to-end mock slice (MockASR → BM25 → SafetyRouter →
   MockLLM → MockTTS) works with standard library only.
4. **`python-dotenv`**: Optional. `config.py` has a tiny internal `.env` parser
   fallback so `APP_MODE=mock` needs no install at all.
5. **BM25**: Self-implemented Okapi BM25 in pure Python (no numpy/scikit-learn
   required) for stability and reviewability. Embedding-based retrieval is out
   of scope for this phase.
6. **Real adapters are lazy**: PhoWhisper (`faster-whisper`), Gemini
   (`google-genai`), Groq (`groq`), Edge-TTS (`edge-tts`), Streamlit are
   optional imports. Missing dependencies produce clear messages, never a
   crash at import time.
7. **No large model auto-download**: PhoWhisper model weights are NOT
   downloaded during this phase. Machine has 15.8 GB RAM / CPU-only, which can
   run `phowhisper-small/base` but this must be a deliberate human decision
   (see `docs/hardware_benchmark_plan.md`).
8. **Audio never leaves the machine by default**; `APP_MODE=cloud` only affects
   LLM calls (text), never audio upload.
9. **Demo data is explicitly synthetic**: `data/sources/DEMO_SOURCE.md` is
   labeled DEMO/SYNTHETIC, describes a fictional commune ("Bình Minh") and is
   not official administrative guidance. Eval results are watermarked
   "SYNTHETIC DEMO - NOT PILOT RESULTS".
10. **Emergency/legal phone numbers**: Only placeholders in config
    (`OFFICIAL_*` placeholders), marked "must verify before deployment".
11. **Hold message**: A static "please hold" message exists for the HOLDING
    state; no LLM involvement.
12. **TTS**: Default is MockTTS (writes .txt/.wav placeholder). Edge-TTS is
    optional and requires network at runtime.
13. **Python 3.14 compatibility**: Verified at install time; pinning is in
    `requirements-*.txt`. faster-whisper 1.2.1 supports 3.14 (preinstalled).
14. **No FreeSWITCH/SIP/callback/multilingual/OpenVINO** in this phase —
    interfaces/roadmap only.
15. **`make` may not exist on Windows**: Makefile is provided for CI/Unix, and
    every target has an equivalent `python` command documented in README.
16. **Confidence scores**: None used — no calibration exists yet (principle 8).
17. **SAVE_TRANSCRIPTS=false, DELETE_RAW_AUDIO_AFTER_SESSION=true** defaults.

## Open questions for the human team

- Which official channels (hotlines, one-stop shop) will be verified for RED
  routing messages? (config placeholders ready)
- Who owns the pilot consent form and IRB-equivalent review? (see
  `docs/pilot_protocol.md`)
- Which PhoWhisper model size is acceptable for the deployment laptop?
