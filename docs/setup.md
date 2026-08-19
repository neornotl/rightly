# Cài đặt và chạy Rightly

## Điều kiện

- Python 3.10 trở lên.
- Chế độ `mock` chỉ cần dependency trong `requirements.txt`.
- Các backend cloud/local/ASR thật có dependency và cấu hình bổ sung.

## 1. Tạo môi trường

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
```

Trên macOS/Linux, thay đường dẫn Python bằng `.venv/bin/python`; có thể dùng `make setup`.

## 2. Tạo cấu hình local

```powershell
Copy-Item .env.example .env
```

Mặc định trong `.env.example` là `mock`; không cần API key. Không commit `.env` hoặc `.streamlit/secrets.toml`.

Các lựa chọn hợp lệ hiện được validate trong `app/config.py`:

| Biến | Giá trị |
| --- | --- |
| `APP_MODE` | `mock`, `local`, `cloud` |
| `ASR_BACKEND` | `mock`, `phowhisper` |
| `RETRIEVAL_BACKEND` | `bm25`, `hybrid` |
| `LLM_BACKEND` | `mock`, `gemini`, `groq`, `pateway`, `local` |
| `TTS_BACKEND` | `mock`, `edge` |

## 3. Chạy

```powershell
# Demo text end-to-end
.\.venv\Scripts\python.exe scripts\run_mock_demo.py

# CLI tương tác
.\.venv\Scripts\python.exe -m app.cli

# Giao diện Streamlit
.\.venv\Scripts\python.exe -m streamlit run app/ui.py
```

`scripts/ingest_documents.py` chỉ cần khi chủ động tái tạo demo chunks. Không chạy nó nếu mục tiêu là giữ nguyên corpus runtime hiện có.

## 4. Backend tùy chọn

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-optional.txt
```

| Nhu cầu | Việc cần thêm |
| --- | --- |
| PhoWhisper | cài `faster-whisper`, tải model có chủ đích, đặt `ASR_BACKEND=phowhisper` |
| Groq / Gemini / Pateway | đặt backend tương ứng và key trong `.env` hoặc secrets |
| Local LLM | chạy Ollama/OpenAI-compatible server, đặt `LLM_BACKEND=local` và `OLLAMA_*` |
| Hybrid retrieval | cài stack embedding cần thiết; nếu thiếu app tự về BM25 |

## 5. Kiểm tra trước khi chia sẻ

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe scripts\validate_data.py
.\.venv\Scripts\python.exe scripts\preflight.py
```

Không coi một lần chạy green là chứng nhận production. Trước pilot/deploy, xem [gates](../gates/README.md), [privacy](privacy_deletion_policy.md) và [deployment strategy](deployment_strategy.md).
