# Contributing

Tiếng Làng is an accessibility-focused public-service access agent. We value
honest, verifiable contributions over feature count.

## Ground rules

1. Never fabricate results. Synthetic demo results must stay labeled as
   synthetic (watermark: "SYNTHETIC DEMO - NOT PILOT RESULTS").
2. Never commit real API keys or personal data. `.env` is git-ignored.
3. Never represent demo/synthetic data as official administrative guidance.
   Demo source files are labeled DEMO/SYNTHETIC.
4. Do not hard-code unverified emergency numbers or legal contacts; use config
   placeholders with "must verify" notes.
5. Prefer the standard library and pure-Python implementations for core paths.

## Workflow

1. Open an issue or pick one; state your intent.
2. Create a branch: `git checkout -b <topic>`.
3. Implement, with tests for every behavior change.
4. Run quality gates:
   - `make test` (or `python -m pytest`)
   - `make lint` (or `python -m ruff check . && python -m ruff format --check .`)
   - `make preflight` (or `python scripts/preflight.py`)
5. Open a PR with a short summary and the `OPENCODE_PREPARATION_REPORT.md`
   status if it changed.

## Code of conduct

See `CODE_OF_CONDUCT.md`. Be respectful; accessibility work has real
vulnerable users behind it.
