# Rightly

> Trợ lý hỏi đáp tiếng Việt, ưu tiên giọng nói, giúp người dân tiếp cận thông tin công và pháp luật bằng câu trả lời có căn cứ nguồn.

**Trạng thái:** MVP / preparation. Rightly không phải cơ quan nhà nước, không thay thế cán bộ, luật sư, bác sĩ hoặc dịch vụ khẩn cấp.

## Bắt đầu từ đây

| Bạn muốn làm gì? | Đọc / chạy |
| --- | --- |
| Hiểu hệ thống và các giới hạn | [Tổng quan kỹ thuật](docs/MASTER.md) · [Giới hạn](docs/limitations.md) |
| Cài và chạy cục bộ | [Hướng dẫn cài đặt](docs/setup.md) |
| Chạy giao diện web | `python -m streamlit run app/ui.py` |
| Chạy chế độ demo | `python scripts/run_mock_demo.py` |
| Kiểm tra chất lượng | `python -m pytest` · `python scripts/preflight.py` |
| Hiểu dữ liệu và đánh giá | [Data card](docs/data_card.md) · [Evaluation protocol](docs/evaluation_protocol.md) |

## Hệ thống làm gì?

Rightly nhận câu hỏi bằng chữ hoặc âm thanh, tìm các đoạn văn bản liên quan, áp dụng rào chắn an toàn rồi mới tạo và đọc câu trả lời.

```text
Văn bản / âm thanh
  → ASR (nếu có âm thanh)
  → chuẩn hóa và truy xuất nguồn
  → safety router
  → FAQ đã biên soạn hoặc LLM
  → kiểm tra trích dẫn và hiệu lực
  → TTS / giao diện
```

Quy tắc quan trọng: nếu thiếu nguồn, trích dẫn không hợp lệ, hoặc câu hỏi thuộc tình huống rủi ro, hệ thống phải hỏi lại, từ chối hoặc chuyển hướng — không đoán.

## Chế độ chạy

| Chế độ | Mục đích | Thành phần mặc định |
| --- | --- | --- |
| `mock` | Phát triển và demo không cần key | Mock ASR, BM25, Mock LLM, Mock TTS |
| `local` | Chạy LLM tại máy qua server tương thích OpenAI/Ollama | BM25 hoặc hybrid, Local LLM |
| `cloud` | Dùng Gemini, Groq hoặc Pateway | Query được scrub PII trước khi gửi ra ngoài |

Các backend được chọn trong `.env`; xem `.env.example` và [Setup](docs/setup.md). Audio thô không được gửi tới LLM cloud.

## Chạy nhanh trên Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts\run_mock_demo.py
```

Để mở UI, cài Streamlit (đã có trong `requirements.txt`) rồi chạy:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app/ui.py
```

## Dữ liệu, an toàn và quyền riêng tư

- Corpus runtime hiện là `data/chunks/real_chunks.jsonl`; registry hiệu lực là `data/law_status.json`.
- FAQ là nội dung được biên soạn, nhưng vẫn được gắn nguồn và truy xuất lại evidence trước khi trả lời.
- Audio trong `DATA_DIR` được xóa sau xử lý khi `DELETE_RAW_AUDIO_AFTER_SESSION=true`.
- Transcript không được lưu mặc định. Log được scrub theo heuristic; đây không phải cam kết ẩn danh tuyệt đối.
- Các số liên hệ/kênh chính thức chỉ được hiển thị khi đã được xác minh trong `data/contacts.json`.

Đọc thêm: [Responsible AI](docs/responsible_ai.md), [chính sách xóa dữ liệu](docs/privacy_deletion_policy.md), [threat model](docs/threat_model.md).

## Cấu trúc repository

```text
app/            pipeline, UI, safety, retrieval, adapter ASR/LLM/TTS
data/           chunks, FAQ, registry hiệu lực, dữ liệu đánh giá
docs/           tài liệu hiện hành và tài liệu lịch sử có nhãn
eval/           metric và runner đánh giá
scripts/        ingest, kiểm tra, benchmark, utility và artifact nghiên cứu
tests/           unit test và pilot-readiness gates
legal-corpus/  văn bản nguồn thô, không phải đường chạy runtime trực tiếp
```

## Tài liệu theo vai trò

- Kỹ thuật: [Master](docs/MASTER.md), [Architecture](docs/architecture.md), [Setup](docs/setup.md).
- Dữ liệu/evaluation: [Data card](docs/data_card.md), [Dataset card](docs/evaluation_dataset_card.md), [Protocol](docs/evaluation_protocol.md).
- Vận hành: [Deployment](docs/deployment_strategy.md), [Pilot](docs/pilot_protocol.md), [Gates](gates/README.md).
- An toàn: [Responsible AI](docs/responsible_ai.md), [Privacy](docs/privacy_deletion_policy.md), [Threat model](docs/threat_model.md).

Các file có ngày, tên “baseline”, “report”, “review”, “council” hoặc “checklist” là artifact lịch sử; không nên dùng chúng làm hướng dẫn vận hành mà không đối chiếu code và cấu hình hiện tại.

## License

MIT — xem [LICENSE](LICENSE).
