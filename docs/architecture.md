# Architecture

## Component diagram

```mermaid
flowchart LR
    U[User voice] --> MIC[(Microphone / audio file)]
    MIC --> ASR[ASR: MockASR | PhoWhisper]
    ASR --> NORM[Normalize + rule checks]
    NORM --> RETR[Retriever: BM25]
    RETR --> ROUTER[SafetyRouter]
    ROUTER -->|RED/ORANGE| POLICY[Policy messages]
    ROUTER -->|YELLOW + sufficient| LLM[LLM: MockLLM | Gemini | Groq]
    LLM --> ANSWER[GroundedAnswer]
    ANSWER --> TTS[TTS: MockTTS | EdgeTTS]
    TTS --> SPEAK[Speaker / spoken text]
    ROUTER -->|requires_human| HUMAN[Human-in-the-loop / official channel]
```

## Module I/O

| Module | Input | Output |
|---|---|---|
| `app/config.py` | env vars / `.env` | `Settings` (validated) |
| `app/asr/*` | `audio_path` | `ASRResult(transcript, latency_ms, backend)` |
| `app/retrieval/*` | `query, top_k` | `list[RetrievedChunk]` |
| `app/safety/rules.py` | normalized text | `RuleHits` |
| `app/safety/router.py` | query, chunks, optional LLM classifier | `SafetyDecision` |
| `app/llm/*` | query, chunks | JSON doc (answer fields) |
| `app/tts/*` | text | audio path / spoken text file |
| `app/dialogue/state_machine.py` | target state | new state (validated) |
| `app/pipeline.py` | session_id + text/audio | `PipelineResult` |

## Pipeline control flow (mock mode)

1. `Pipeline.process_text(session_id, text)` → normalize → BM25 search →
   `SafetyRouter.route(...)` → if `would_answer` → LLM → TTS.
2. `Pipeline.process_audio(session_id, path)` → MockASR reads sibling `.txt`
   transcript (or fallback) → same core → raw audio deleted after session if
   inside `DATA_DIR` and `DELETE_RAW_AUDIO_AFTER_SESSION=true`.

## Error / fallback paths

| Failure | Behavior |
|---|---|
| LLM backend missing key / dep / parse error | `insufficient_decision()` — refuse, never fake answer |
| TTS failure | log `tts_failure`; result still returned with text |
| Retriever empty / below threshold | `REFUSE` (ORANGE) |
| Rule engine exception | router treats as ambiguous → `CLARIFY` |
| ASR: file missing / bad format | `AudioFormatError` with clear message |
| LLM invents source_id | `enforce_source_ids()` sanitizes to allowed set |

## Threat boundaries

- **Audio**: never leaves the machine in default config; `APP_MODE=cloud`
  only affects text LLM calls.
- **LLM context**: only transcript + retrieved chunks (never audio, never raw
  PII beyond the query itself).
- **Routing authority**: rules run before and override LLM; LLM classification
  is advisory only.
- **Data**: `data/sources` is human-curated; ingest marks `is_demo`.
- **Logs**: scrubbed heuristic; deletion API in `SessionStore`.

Full analysis: `docs/threat_model.md`.
