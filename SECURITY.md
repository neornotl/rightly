# Security Policy

## Reporting a vulnerability

Do NOT open a public issue for security problems. Contact the maintainers
privately (the address will be published when the project has a maintainer
email; until then, use a private GitHub advisory if/when the repository is
published).

Please include:

- Affected version / commit.
- Steps to reproduce.
- Impact assessment (data exposed, escalation path, etc.).

## Supported versions

| Version | Status |
|---------|--------|
| 4.0.x   | Active development (pre-pilot) |

## Security posture (summary)

- No real secrets in the repository; API keys live in `.env` (git-ignored).
- Default mode never sends audio to the cloud.
- PII handling follows `docs/privacy_deletion_policy.md`.
- Threat model: `docs/threat_model.md`.
- Logs are scrubbed by `scripts/scrub_logs.py`; the scrubber is heuristic and
  must not be treated as a full redaction guarantee.

## Reporting channels

TBD before deployment. Placeholders are intentionally not real numbers.
