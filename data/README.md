# Dữ liệu nguồn Rightly

> **Nguồn sự thật:** pipeline runtime ưu tiên `chunks/real_chunks.jsonl`; `law_status.json` là registry kiểm tra hiệu lực/citation. Các file demo chỉ dùng cho phát triển hoặc fallback mock.

Quy tắc dữ liệu trong repository này:

- Mọi tài liệu trong `sources/` phải ghi nhãn `DEMO` / `SYNTHETIC` nếu không phải nguồn chính thức.
- Không đưa hướng dẫn hành chính thật dưới dạng giả thật.
- `chunks/` chứa cả demo chunks và corpus runtime đã chuẩn bị; không chỉnh tay JSONL.
- `metadata.csv` là output của pipeline ingest demo, không phải catalog đầy đủ của corpus runtime.

## Cách tạo dữ liệu

```
python scripts/ingest_documents.py
```

Script đọc mọi `*.md` trong `sources/`, cắt chunk (900 ký tự, overlap 120), ghi `chunks/demo_chunks.jsonl` và `metadata.csv`.

## Lưu ý triển khai

- Corpus runtime phải được cập nhật có kiểm soát, kèm provenance, trạng thái hiệu lực và kiểm tra citation.
- `law_status.json` là lớp guard rail cho source ID, expiry và replacement; không thay thế việc rà soát pháp lý nguồn.
- Xem [data card](../docs/data_card.md) và [evaluation dataset card](../docs/evaluation_dataset_card.md) trước khi thay dữ liệu.
