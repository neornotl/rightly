"""Ingest markdown sources into chunks JSONL + metadata CSV.

Usage:
    python scripts/ingest_documents.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.retrieval.document_loader import DocumentLoader


def main() -> int:
    loader = DocumentLoader()
    try:
        records = loader.ingest()
    except Exception as exc:
        print(f"[INGEST ERROR] {exc}", file=sys.stderr)
        return 1
    print(
        f"Ingested {len(records)} chunks "
        f"-> {loader.chunks_dir / 'demo_chunks.jsonl'} (+ metadata.csv)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
