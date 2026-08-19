# Rightly — tài liệu kỹ thuật hiện hành

> Nguồn sự thật của tài liệu này là mã trong `app/`, cấu hình trong `.env.example`, registry/chunks dưới `data/` và các test hiện có. Báo cáo theo mốc thời gian ở nơi khác trong repo chỉ có giá trị lịch sử.

## 1. Mục đích và ranh giới

Rightly là trợ lý tiếng Việt, ưu tiên giọng nói, giúp người dân tìm thông tin công/pháp luật từ corpus đã chuẩn bị. Hệ thống cố gắng trả lời có căn cứ, nhưng không phải kênh chính thức và không đưa ra phán quyết pháp lý.

| Rightly có thể làm | Rightly không làm |
| --- | --- |
| Nhận text/audio, tìm evidence và diễn giải ngắn | Xác nhận quyết định pháp lý cá nhân hoặc thay cơ quan nhà nước |
| Hỏi lại, từ chối hoặc chuyển hướng khi rủi ro | Xử lý cấp cứu, bạo lực, tranh chấp hay vụ việc hình sự thay con người |
| Đọc câu trả lời, đưa nguồn và tạo phiếu tham khảo | Tự gọi điện, gửi hồ sơ hoặc lưu dữ liệu cá nhân để làm thủ tục |

## 2. Đường chạy

```text
input → ASR (nếu cần) → retrieval → SafetyRouter → FAQ/LLM
      → citation & spoken-response validation → TTS → kết quả + log
```

`Pipeline` trong `app/pipeline.py` là điểm điều phối chung cho UI, CLI và các caller khác.

1. `process_text` hoặc `process_audio` tạo câu hỏi; audio qua ASR trước khi vào core pipeline.
2. Retriever dùng `real_chunks.jsonl` nếu có; chỉ mock mode mới được hạ về demo chunks.
3. Router dùng rule trước LLM: RED/ORANGE không được LLM ghi đè.
4. FAQ có thể trả lời các câu khớp mạnh; nếu không, LLM dùng query hiện tại, evidence và tối đa ba lượt context trong RAM.
5. Câu trả lời không có citation bị từ chối. Với non-mock mode, validator đối chiếu citation với evidence vừa lấy và `law_status.json`.
6. TTS là best-effort; hỏng TTS vẫn trả text. Log transcript chỉ được lưu khi cấu hình cho phép.

## 3. Thành phần

| Thư mục / file | Vai trò |
| --- | --- |
| `app/config.py` | Đọc/validate env, hòa trộn Streamlit secrets, bảo vệ secret khi hiển thị |
| `app/pipeline.py` | Factory backend, flow xử lý, privacy lifecycle, FAQ, citation, TTS |
| `app/safety/` | Rule, router và thông điệp chính sách cho các vùng RED/ORANGE/YELLOW |
| `app/retrieval/` | Ingest/chunk loader, BM25 và hybrid dense/RRF tùy chọn |
| `app/llm/` | Mock, Gemini, Groq, Pateway, local và fallback |
| `app/asr/`, `app/tts/` | Adapter giọng nói với dependency lazy |
| `app/validation/` | Citation validity và chất lượng đáp án đọc thành tiếng |
| `app/ui.py`, `app/cli.py` | Giao diện Streamlit và CLI |
| `data/` | Corpus chunks, FAQ, contacts, registry hiệu lực, fixture eval |
| `tests/`, `tests/gates/` | Regression test và pilot-readiness gates |

## 4. Cấu hình vận hành

Các giá trị hợp lệ được kiểm trong `load_settings()`; đừng dựa vào ghi chú cũ nếu khác code.

| Nhóm | Biến quan trọng |
| --- | --- |
| Mode/backend | `APP_MODE`, `ASR_BACKEND`, `RETRIEVAL_BACKEND`, `LLM_BACKEND`, `TTS_BACKEND` |
| Cloud/local | `GEMINI_API_KEY`, `GROQ_API_KEY[_2.._5]`, `PATEWAY_*`, `OLLAMA_*` |
| Privacy | `DELETE_RAW_AUDIO_AFTER_SESSION`, `SAVE_TRANSCRIPTS`, `PII_SCRUB_OUTBOUND`, `LOG_RETENTION_DAYS` |
| Retrieval | `MIN_RETRIEVAL_SCORE`, `RETRIEVER_GATE`, `RETRIEVAL_BM25_GATE`, `RETRIEVAL_DENSE_GATE` |
| Vận hành | `RATE_LIMIT_PER_IP`, `RATE_LIMIT_WINDOW_SECONDS`, `MAX_RESPONSE_CHARS` |

Mẫu an toàn nằm tại `.env.example`. Secret chỉ đặt ở `.env` hoặc dashboard secrets, không đưa vào Markdown, code hay log.

## 5. An toàn và quyền riêng tư

- RED: khẩn cấp/bạo lực → `ESCALATE`; không tạo câu trả lời LLM.
- ORANGE: ví dụ hình sự, tranh chấp, tin đồn pháp luật, ngoài phạm vi, thiếu nguồn → hướng dẫn/từ chối.
- YELLOW: chỉ trả lời khi evidence đủ.
- PII scrub áp dụng cho query và session memory trước khi một backend cloud nhận chúng.
- Xóa audio chỉ áp dụng với file nằm dưới `DATA_DIR`; tránh xóa file người dùng ngoài phạm vi.
- `SessionStore.delete_session()` xóa log của session và `Pipeline` xóa memory RAM của session đó.

Các heuristic không phải biện pháp bảo vệ hoàn hảo. Xem [Responsible AI](responsible_ai.md), [Privacy](privacy_deletion_policy.md) và [Threat model](threat_model.md).

## 6. Dữ liệu và grounding

| Thành phần | Vai trò hiện tại |
| --- | --- |
| `data/chunks/real_chunks.jsonl` | Corpus runtime đã chunk hóa |
| `data/law_status.json` | Registry trạng thái, expiry và replacement source |
| `data/faq.json` | 50 FAQ curated; có `source_ids`/search text |
| `data/contacts.json` | Contact chỉ callable khi `verified=true` |
| `data/eval/` | Fixture phát triển/đánh giá, không đồng nghĩa pilot result |
| `legal-sources/` | Nguồn văn bản thô, không phải input trực tiếp của pipeline runtime |

Citation validation kiểm tra ba điều: source có trong registry, chưa hết hiệu lực và đã có trong evidence vừa truy xuất. Đây là guard rail, không thay thế quy trình pháp lý rà soát nội dung nguồn.

## 7. Cách làm việc an toàn

```powershell
python -m pytest
python scripts/validate_data.py
python scripts/preflight.py
```

Sau khi thay đổi logic, hãy chạy test liên quan trước; trước pilot/deploy, chạy toàn bộ preflight và xem [gates](../gates/README.md). Các script crawl, benchmark, debate/council và report không phải tất cả đều là đường chạy production.

## 8. Bản đồ tài liệu

- [README](../README.md): entry point ngắn.
- [Architecture](architecture.md): luồng và ranh giới thành phần.
- [Setup](setup.md): cài đặt và chạy.
- [Data card](data_card.md), [evaluation dataset card](evaluation_dataset_card.md), [evaluation protocol](evaluation_protocol.md).
- [Deployment strategy](deployment_strategy.md), [pilot protocol](pilot_protocol.md), [hardware benchmark](hardware_benchmark_plan.md).
- [Limitations](limitations.md), [Responsible AI](responsible_ai.md), [Privacy](privacy_deletion_policy.md), [Threat model](threat_model.md).

## 9. Trạng thái tài liệu

Các file `baseline_*`, `*_report`, `project_review.md`, `QUESTS.md`, checklist nộp bài và tài liệu “council” ghi lại quyết định hoặc snapshot của thời điểm tạo file. Chúng hữu ích để truy vết, nhưng không thay thế tài liệu hiện hành này.
