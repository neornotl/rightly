"""P4: Crawl official legal documents from vanban.chinhphu.vn.

For each known docid:
  - fetch the legacy detail page (?pageid=27160&docid=NNN)
  - parse metadata from the #block_detail table
  - download the official signed PDF from datafiles.chinhphu.vn
  - extract text with pypdf, normalize, write a markdown source
  - write data/source_registry.csv (status=pending_review) and chunks

Usage:
    python scripts/crawl_vbpl.py [--no-download]
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "private_cache" / "vbpq"
SOURCES = ROOT / "data" / "sources_real"
CHUNKS = ROOT / "data" / "chunks"
REGISTRY = ROOT / "data" / "source_registry.csv"

BASE = "https://vanban.chinhphu.vn/?pageid=27160&docid={docid}"
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "vi-VN,vi;q=0.9",
}

LABELS = {
    "Số ký hiệu": "ky_hieu",
    "Ngày ban hành": "ngay_ban_hanh",
    "Ngày có hiệu lực": "ngay_hieu_luc",
    "Loại văn bản": "loai",
    "Cơ quan ban hành": "co_quan",
    "Người ký": "nguoi_ky",
    "Trích yếu": "trich_yeu",
}

# docid -> (expected ky hieu, purpose note)
DOCS: list[tuple[int, str, str]] = [
    (182158, "123/2015/NĐ-CP", "Nghị định chi tiết thi hành Luật Hộ tịch"),
    (178129, "60/2014/QH13", "Luật Hộ tịch"),
    (175351, "52/2014/QH13", "Luật Hôn nhân và Gia đình"),
    (178372, "126/2014/NĐ-CP", "Nghị định chi tiết thi hành Luật HN&GĐ"),
    (202609, "68/2020/QH14", "Luật Cư trú"),
    (211821, "154/2024/NĐ-CP", "Nghị định chi tiết thi hành Luật Cư trú"),
    (212416, "07/2025/NĐ-CP", "NĐ sửa đổi hộ tịch/quốc tịch/chứng thực"),
    (212474, "46/2024/QH15", "Luật Công chứng (mới, hiệu lực 01/07/2025)"),
    (213663, "104/2025/NĐ-CP", "NĐ quy định chi tiết thi hành Luật Công chứng"),
    (209628, "26/2023/QH15", "Luật Căn cước"),
    (203460, "62/2021/NĐ-CP", "NĐ xử phạt hộ tịch (hết hiệu lực)"),
]


def fetch(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_metadata(html: str) -> dict[str, str]:
    m = re.search(r'id="block_detail"(.*)$', html, re.S)
    seg = m.group(1) if m else html
    seg = re.sub(r"<script.*?</script>", "", seg, flags=re.S)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "|", seg))
    tokens = [t.strip() for t in txt.split("|") if t.strip()]
    meta: dict[str, str] = {}
    for i, tok in enumerate(tokens):
        if tok in LABELS and i + 1 < len(tokens) and LABELS[tok] not in meta:
            meta[LABELS[tok]] = tokens[i + 1]
    pdfs = re.findall(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', html, re.I)
    meta["pdf_url"] = pdfs[0] if pdfs else ""
    return meta


def source_id_from(ky_hieu: str) -> str:
    m = re.match(r"(\d+)/(\d{4})", ky_hieu.strip())
    if not m:
        return "vb_" + ky_hieu.lower()
    num, year = m.groups()
    prefix = "nd" if ky_hieu.upper().endswith("CP") or "NĐ-CP" in ky_hieu else "luat"
    return f"{prefix}{num}_{year}"


def normalize_text(pages_text: str) -> str:
    lines: list[str] = []
    for raw in pages_text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw).strip()
        if not line:
            continue
        if re.fullmatch(r"\d{1,3}", line):
            continue
        if line.startswith("CÔNG BÁO/Số") or line.startswith("Công báo/Số"):
            continue
        if re.fullmatch(r"[.,\-—]+", line):
            continue
        lines.append(line)
    body = "\n".join(lines)
    body = re.sub(r"(?m)^(Điều \d+[\.\s]|Chương [IVXLCDM]+\s)", r"\n\n\1", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return body


def build_front_matter(meta: dict[str, str], sid: str, docid: int) -> str:
    title = meta.get("trich_yeu", "").strip()
    loai = meta.get("loai", "")
    co_quan = meta.get("co_quan", "")
    return (
        f"---\nsource_id: {sid}\ntitle: {loai} {meta.get('ky_hieu', '')} {title}\n".strip() + "\n"
        f"source_type: gov_legal\n"
        f"publisher: {co_quan}\n"
        f"published_date: {meta.get('ngay_ban_hanh', '')}\n"
        f"url: {BASE.format(docid=docid)}\n"
        f"notes: Official text from vanban.chinhphu.vn\n"
        "---\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-download", action="store_true")
    ap.add_argument("--max-docs", type=int, default=0)
    args = ap.parse_args()

    from app.retrieval.document_loader import DocumentLoader

    CACHE.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    CHUNKS.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    ok_docs = 0
    docs = DOCS[: args.max_docs] if args.max_docs else DOCS
    for docid, expect, note in docs:
        sid = ""
        try:
            html = fetch(BASE.format(docid=docid)).decode("utf-8", errors="replace")
            meta = parse_metadata(html)
            ky = meta.get("ky_hieu", "")
            if not ky:
                print(f"[SKIP] docid {docid}: no ky_hieu parsed")
                continue
            sid = source_id_from(ky)
            pdf = meta.get("pdf_url", "")
            pdf_path = ""
            if pdf:
                pdf_path = CACHE / f"{sid}.pdf"
                if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
                    if args.no_download:
                        print(f"[NO-DL] {docid} {ky}")
                    else:
                        data = fetch(pdf)
                        if len(data) > 1000:
                            pdf_path.write_bytes(data)
                        else:
                            pdf_path = ""
            else:
                print(f"[WARN] docid {docid} {ky}: no PDF link")

            body = ""
            status = "pending_review"
            ocr_txt = CACHE / f"{sid}.ocr.txt"
            if pdf_path and pdf_path.exists():
                import pypdf

                reader = pypdf.PdfReader(str(pdf_path))
                body = normalize_text("\n".join(p.extract_text() or "" for p in reader.pages))
            if len(body.strip()) < 500 and ocr_txt.exists():
                body = normalize_text(ocr_txt.read_text(encoding="utf-8"))
                status = "ocr_pending_review"
            elif len(body.strip()) < 500:
                status = "scanned_pending_ocr"

            md = build_front_matter(meta, sid, docid) + "\n" + body + "\n"
            if body.strip():
                (SOURCES / f"{sid}.md").write_text(md, encoding="utf-8")
            else:
                md = ""
            print(f"[OK] {docid} -> {sid} | {ky} | {meta.get('loai', '')} | pdf={len(body)} chars")
            rows.append(
                {
                    "source_id": sid,
                    "docid": docid,
                    "ky_hieu": ky,
                    "loai": meta.get("loai", ""),
                    "co_quan": meta.get("co_quan", ""),
                    "ngay_ban_hanh": meta.get("ngay_ban_hanh", ""),
                    "ngay_hieu_luc": meta.get("ngay_hieu_luc", ""),
                    "trich_yeu": meta.get("trich_yeu", ""),
                    "url_vb": BASE.format(docid=docid),
                    "pdf_local": str(pdf_path) if pdf_path else "",
                    "chars": len(body),
                    "status": status,
                    "notes": note,
                }
            )
            ok_docs += 1
        except Exception as exc:  # noqa: BLE001
            print(f"[ERR] docid {docid}: {type(exc).__name__}: {exc}")
            rows.append(
                {
                    "source_id": sid or f"docid_{docid}",
                    "docid": docid,
                    "ky_hieu": expect,
                    "status": "error",
                    "notes": note,
                }
            )

    with REGISTRY.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    loader = DocumentLoader(
        sources_dir=SOURCES,
        chunks_dir=CHUNKS,
        metadata_csv=ROOT / "data" / "source_metadata_real.csv",
        out_name="real_chunks.jsonl",
    )
    records = loader.ingest()
    print(
        f"\nRegistry: {REGISTRY} ({len(rows)} rows, {ok_docs} ok) | "
        f"chunks: {len(records)} -> {CHUNKS / 'real_chunks.jsonl'}"
    )
    return 0 if ok_docs else 2


if __name__ == "__main__":
    raise SystemExit(main())
