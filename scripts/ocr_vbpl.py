"""P4: OCR scanned official PDFs (data/private_cache/vbpq/*.pdf) to text.

Only processes PDFs where pypdf extraction yields <500 chars (scanned).
Outputs one .ocr.txt per document, written incrementally per page so a
crash does not lose finished pages. OCR cache per page kept in
data/private_cache/vbpq/_ocr_cache.jsonl.

Usage:
    python scripts/ocr_vbpl.py [--pages N] [--doc SID]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "private_cache" / "vbpq"
CACHE_JSONL = CACHE / "_ocr_cache.jsonl"

REQUIRE_VI = [  # must contain at least one Vietnamese marker to be trusted
    "CHÍNH PHỦ",
    "Quốc hội",
    "Điều",
    "Nghị định",
    "Thông tư",
]


def load_cache() -> dict[str, str]:
    out: dict[str, str] = {}
    if CACHE_JSONL.exists():
        for line in CACHE_JSONL.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                out[rec["key"]] = rec["text"]
    return out


def save_cache(cache: dict[str, str], key: str, text: str) -> None:
    cache[key] = text
    with CACHE_JSONL.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"key": key, "text": text}, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=0)
    ap.add_argument("--doc", type=str, default="")
    ap.add_argument("--scale", type=float, default=2.0)
    args = ap.parse_args()

    import easyocr
    import numpy as np
    import pypdfium2 as pdfium

    cache = load_cache()
    reader = easyocr.Reader(["vi"], gpu=False, verbose=False)

    docs = sorted(CACHE.glob("*.pdf"))
    if args.doc:
        docs = [d for d in docs if d.stem == args.doc]
    done, skipped = 0, 0
    t_start = time.time()
    for pdf_path in docs:
        sid = pdf_path.stem
        try:
            import pypdf

            pypdf_text = "\n".join(
                p.extract_text() or "" for p in pypdf.PdfReader(str(pdf_path)).pages
            )
        except Exception:  # noqa: BLE001
            pypdf_text = ""
        if len(pypdf_text.strip()) > 500:
            (CACHE / f"{sid}.ocr.txt").write_text(pypdf_text, encoding="utf-8")
            print(f"[SKIP-text] {sid} ({len(pypdf_text)} chars from pypdf)")
            skipped += 1
            continue

        out_path = CACHE / f"{sid}.ocr.txt"
        doc = pdfium.PdfDocument(str(pdf_path))
        n = len(doc)
        page_range = range(args.pages) if args.pages else range(n)
        pages_text: list[str] = []
        has_new = False
        for i in page_range:
            key = f"{sid}::p{i}"
            if key in cache:
                pages_text.append(cache[key])
                continue
            pil = doc[i].render(scale=args.scale).to_pil()
            t0 = time.time()
            res = reader.readtext(np.array(pil), detail=0, paragraph=True)
            text = "\n".join(res)
            save_cache(cache, key, text)
            pages_text.append(text)
            has_new = True
            print(f"  {sid} p{i + 1}/{n} ({time.time() - t0:.0f}s)")

        body = "\n\n".join(pages_text).strip()
        if body and (has_new or not out_path.exists()):
            out_path.write_text(body + "\n", encoding="utf-8")
        if body:
            done += 1
            print(f"[OCR] {sid}: {len(body)} chars -> {out_path.name}")
        else:
            print(f"[EMPTY] {sid}")
    print(f"\nDONE: {done} docs OCR'd, {skipped} text-based, {time.time() - t_start:.0f}s total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
