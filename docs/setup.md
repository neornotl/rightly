# Setup guide

## Requirements

- Python >= 3.10 (tested on 3.14 / Windows 10; Ubuntu CI assumed ≥ 3.11).
- Internet chỉ cần để cài package; **mock mode chạy offline hoàn toàn**.

## 1. Create environment

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
```

Unix:

```bash
make setup   # = venv + install requirements.txt + requirements-dev.txt
```

## 2. Optional adapters

```powershell
pip install -r requirements-optional.txt
```

| Adapter | Package | Ghi chú |
|---|---|---|
| PhoWhisper ASR | `faster-whisper` | model tải lúc runtime, chủ động chọn |
| Gemini LLM | `google-genai` | cần `GEMINI_API_KEY` |
| Groq LLM | `groq` | cần `GROQ_API_KEY` |
| Edge-TTS | `edge-tts` | cần mạng lúc chạy |
| Streamlit UI | `streamlit` | `streamlit run app/ui.py` |

## 3. Environment file

```powershell
Copy-Item .env.example .env
```

Điền key (nếu dùng cloud). `.env` đã bị `.gitignore` — **không bao giờ**
commit file này. Mặc định (`APP_MODE=mock`) không cần `.env` gì cả.

## 4. Ingest demo data

```powershell
python scripts/ingest_documents.py
python scripts/validate_data.py
```

## 5. Run

```powershell
python scripts/run_mock_demo.py                 # demo đầu-cuối (mock)
python -m app.cli                               # CLI tương tác
python -m eval.run_all                          # eval R1-R4
python scripts/preflight.py                     # toàn bộ quality gate
python -m streamlit run app/ui.py               # UI (nếu cài streamlit)
```

## Windows note

`make` thường không có sẵn; dùng các lệnh `python` tương đương ở trên.
Makefile vẫn được giữ cho CI/Unix.

## Kiểm tra môi trường

```powershell
python scripts/check_environment.py
```
