# Tiếng Làng v4.0 — MASTER DOC (kỹ thuật)

Tài liệu tổng hợp để hiểu **toàn bộ** hệ thống Tiếng Làng: từ cốt lõi (mock
vertical slice) đến các tầng nâng cao (hybrid RAG, LLM cloud, safety routing,
privacy, đánh giá). Đây là tài liệu "một cửa" — các tài liệu chuyên sâu khác
được dẫn ở cuối.

> Trạng thái dự án: **PREPARATION / MVP (mock-first)**. Mọi kết quả hiện tại là
> SYNTHETIC DEMO, chưa phải pilot. Xem `README.md` và `docs/`.

---

## 1. Hệ thống là gì?

**Tiếng Làng** = trợ lý hỏi-đáp **bằng giọng nói, bám nguồn chính thống**
(source-grounded) cho thủ tục hành chính, quyền lợi công và quy định pháp luật
(dân sự, pháp luật) tại cấp xã/phường — như một kênh hotline hỏi đáp nhanh cho:

- Người cao tuổi, người khiếm thị, người khó đọc.
- Người **bận rộn, không có thời gian tự tìm hiểu** — gọi điện hỏi nhanh thay vì
  tự tra cứu.

Phạm vi pháp luật: trả lời **quy định pháp luật** (dựa trên văn bản luật/nghị
định trong corpus, `source_type=gov_legal`) và **dân sự** thường nhật. Riêng
**vụ việc hình sự** (khởi tố, tạm giam, tội phạm...) được xử lý rào kĩ: không
đưa kết luận, chuyển hướng sang hotline/công an (xem 6.1, `CRIMINAL_MATTER`).

Nguyên tắc an toàn cốt lõi (xuyên suốt mã nguồn):

1. **Rule-based trước, LLM sau** — luật RED/ORANGE luôn ghi đè LLM
   (`app/safety/router.py`, `app/safety/rules.py`).
2. **Không trả lời khi không đủ nguồn** — ngưỡng retrieval + validator
   citation.
3. **Không bịa nguồn** — mọi `source_id` của câu trả lời phải nằm trong nguồn
   đã truy xuất và có trong registry văn bản (`data/law_status.json`).
4. **Privacy mặc định** — audio thô bị xóa sau phiên, transcript không log trừ
   khi bật, log luôn được scrub.

---

## 1.1 Từ điển thuật ngữ (đọc trước nếu không rành kỹ thuật)

Giải thích bằng tiếng Việt thường, để đọc được toàn bộ tài liệu mà không cần
biết về lập trình/AI. Khi gặp từ nào khó, quay lại tra ở đây.

| Thuật ngữ | Giải thích đơn giản |
|---|---|
| **AI / LLM** | Trí tuệ nhân tạo sinh văn bản (chatbot thông minh). Ở dự án này là phần "suy nghĩ và soạn câu trả lời" bằng tiếng Việt. |
| **ASR** | Nghe giọng nói rồi chuyển thành chữ viết (như Siri, trợ lý ảo). |
| **TTS** | Ngược lại: chuyển chữ thành giọng nói để đọc câu trả lời cho người dùng nghe. |
| **Pipeline (dây chuyền)** | Chuỗi các bước xử lý theo thứ tự: nghe → hiểu → tìm tài liệu → soạn câu trả lời → đọc ra. |
| **RAG / Retrieval (tìm nguồn)** | Bước "tìm tài liệu liên quan" trước khi trả lời: hệ thống lấy các đoạn văn bản phù hợp từ kho dữ liệu luật/thủ tục rồi mới dựa vào đó để trả lời. |
| **BM25** | Một cách tìm văn bản theo **từ khóa**: so khớp chữ đúng (như tìm kiếm từ khóa). |
| **Dense / embedding** | Một cách tìm văn bản theo **ý nghĩa**: câu hỏi khác chữ nhưng cùng nghĩa vẫn tìm được. |
| **Hybrid retrieval** | Kết hợp cả hai cách tìm trên để vừa đúng chữ vừa hiểu ý. |
| **Chunk (đoạn văn bản)** | Văn bản gốc được cắt thành từng đoạn nhỏ để máy tìm kiếm dễ dàng hơn. |
| **Gate answerability (cổng kiểm chứng)** | Bộ lọc: nếu không tìm thấy đoạn tài liệu đủ chắc chắn thì KHÔNG trả lời (thà im lặng còn hơn nói bừa). |
| **Source-grounded (bám nguồn)** | Nguyên tắc: mọi câu trả lời phải dựa trên văn bản nguồn thật, không tự bịa. |
| **Citation / source_id** | Trích dẫn: mỗi câu trả lời đính kèm mã nguồn (văn bản luật nào, đoạn nào) để kiểm chứng được. |
| **CitationValidator** | Bộ kiểm tra trích dẫn: soát lại câu trả lời có khớp với nguồn đã truy xuất không; chặn nguồn hết hiệu lực hoặc không có trong sổ theo dõi. |
| **Registry văn bản (`law_status.json`)** | Sổ theo dõi các văn bản luật: văn bản nào còn hiệu lực, văn bản nào đã hết hiệu lực/thay thế. |
| **Safety routing (điều hướng an toàn)** | Bộ não an toàn của hệ thống: phân loại câu hỏi vào 3 vùng màu — **VÀNG** (trả lời có nguồn), **CAM** (không trả lời, đổi hướng/từ chối/hỏi lại), **ĐỎ** (khẩn cấp, báo người thật). |
| **Zone/Action** | Vùng (VÀNG/CAM/ĐỎ) và hành động (ANSWER=trả lời, CLARIFY=hỏi lại, GUIDE=đổi hướng, REFUSE=từ chối, ESCALATE=báo khẩn cấp). |
| **Mock mode (chế độ chạy thử)** | Chạy toàn bộ hệ thống bằng dữ liệu giả, không cần AI thật/API key — dùng để phát triển và demo nội bộ. |
| **Local inference (chạy AI tại máy)** | Chạy AI ngay trên máy tính của người dùng, không gửi dữ liệu lên mạng — bảo vệ thông tin cá nhân tốt nhất. |
| **Cloud (chạy AI trên mạng)** | Ngược lại: gửi câu hỏi lên máy chủ bên ngoài (Groq, Gemini...) để AI xử lý. |
| **PII** | Thông tin nhận dạng cá nhân: tên, số điện thoại, CCCD, địa chỉ... — cần bảo vệ nghiêm ngặt. |
| **Scrub log (làm sạch nhật ký)** | Tự động xóa/bỏ thông tin nhạy cảm (tên, số điện thoại...) trước khi ghi nhật ký hệ thống. |
| **OCR** | Đọc chữ từ ảnh (ví dụ chụp ảnh hợp đồng rồi máy đọc được chữ trong ảnh). |
| **Eval R1–R4** | Bộ đánh giá chất lượng 4 hạng mục: R1 nhận dạng giọng nói (WER), R2 tìm nguồn, R3 điều hướng an toàn, R4 độ trễ. |
| **WER** | Tỉ lệ lỗi chữ khi nhận dạng giọng nói: càng thấp càng chính xác. |
| **Fixture** | Dữ liệu mẫu cố định dùng để kiểm thử lặp lại, so sánh được giữa các lần chạy. |
| **Preflight / quality gate** | Bộ kiểm tra tự động (kiểm thử, chất lượng mã, chạy thử, đánh giá) — vượt hết mới coi là ổn. |
| **Pilot** | Thử nghiệm với người dùng thật với quy mô nhỏ (8–10 người) trước khi triển khai rộng. |
| **CSAT / Task Success Rate** | Đo độ hài lòng của người dùng / tỉ lệ hoàn thành nhiệm vụ trong thử nghiệm thực tế. |

---

## 2. Kiến trúc tổng thể

```
Người dùng nói / gõ
  │
  ▼
[ASR]        MockASR | PhoWhisper (local)        app/asr/
  │
  ▼
[Chuẩn hóa]  normalize_query (lowercase, dấu)    app/safety/rules.py
  │
  ▼
[Retrieval]  BM25 | Hybrid (BM25 + dense + RRF)  app/retrieval/
  │
  ▼
[SafetyRouter]  RED → ORANGE → scope → đủ nguồn  app/safety/
  │              → ambiguous → LLM classify*
  │              (* chỉ APP_MODE=cloud)
  ▼
[LLM]        MockLLM | Gemini | Groq             app/llm/
  │           trả JSON {answer_text, source_ids, ...}
  │
  ▼
[Grounding]  CitationValidator (registry + retrieved)  app/validation/
  │
  ▼
[TTS]        MockTTS | Edge-TTS                  app/tts/
  │
  ▼
[UI]         CLI (state machine) | Streamlit     app/cli.py, app/ui.py
  │
  ▼
[Log]        JSONL ẩn danh, scrub, delete session  app/logging_utils.py
```

Điểm vào duy nhất của mọi đường dẫn là `Pipeline` (`app/pipeline.py`) — cả text
(`process_text`) lẫn audio (`process_audio`) đều đi qua `_run()`.

---

## 3. Cấu trúc code

```
app/
├── pipeline.py          # Dây chuyền E2E: nhà máy adapter + vòng xử lý chính
├── config.py            # Settings từ env/.env, validate, redact secret
├── schemas.py           # Dataclass dùng chung (Zone, Action, GroundedAnswer...)
├── logging_utils.py     # JSONL log ẩn danh, scrub heuristic, SessionStore
├── cli.py               # CLI chạy state machine (mock không cần key)
├── ui.py                # Streamlit UI (tùy chọn)
├── asr/                 # BaseASR | MockASR | PhoWhisperASR
├── retrieval/           # base | document_loader | bm25_retriever | hybrid_retriever
├── safety/              # rules (regex) | router (thứ tự kiểm tra) | policy (lời thoại)
├── llm/                 # BaseLLM | MockLLM | GeminiLLM | GroqLLM
├── validation/          # CitationValidator (P6)
├── tts/                 # BaseTTS | MockTTS | EdgeTTS
└── dialogue/            # state_machine (12 trạng thái) | commands (lệnh giọng nói)
```

Còn lại:

```
eval/        # R1 WER, R2 Retrieval, R3 Routing, R4 Latency + run_all
scripts/     # ingest, crawl VBPL, OCR, scrub, preflight, validate_data, eval...
tests/       # pytest (69 tests) — bao phủ pipeline, safety, retrieval, privacy
data/        # sources, chunks, eval fixtures, law_status, registry, private_cache
docs/        # 18 tài liệu chuyên sâu (danh sách cuối file)
results/     # đầu ra eval + trace; logs/ = JSONL phiên
```

---

## 4. Cấu hình (app/config.py)

Mọi thứ cấu hình qua **env var** (hoặc `.env`), validate chặt tại
`load_settings()`; lỗi cấu hình → `ConfigError` (CLI thoát mã 2).

| Env | Mặc định | Ý nghĩa |
|---|---|---|
| `APP_MODE` | `mock` | `mock` / `local` / `cloud` (cloud bật LLM classify trong router) |
| `ASR_BACKEND` | `mock` | `mock` / `phowhisper` |
| `RETRIEVAL_BACKEND` | `bm25` | `bm25` / `hybrid` |
| `LLM_BACKEND` | `mock` | `mock` / `gemini` / `groq` |
| `TTS_BACKEND` | `mock` | `mock` / `edge` |
| `MIN_RETRIEVAL_SCORE` | `0.01` | ngưỡng điểm tối thiểu để đủ nguồn (RRF ~0.01–0.1; >0.5 → cảnh báo) |
| `RETRIEVER_GATE` | `bm25_dense` | gate "answerability" của hybrid (`none` để tắt) |
| `RETRIEVAL_BM25_GATE` / `RETRIEVAL_DENSE_GATE` | `12.2` / `0.88` | ngưỡng gate, hiệu chỉnh trên corpus thật |
| `RETRIEVER_RERANK` | `false` | cross-encoder rerank (chỉ sắp xếp lại, không quyết định) |
| `MAX_CONTEXT_CHARS` / `MAX_RESPONSE_CHARS` | `12000` / `2000` | giới hạn ký tự |
| `DELETE_RAW_AUDIO_AFTER_SESSION` | `true` | xóa audio thô sau phiên |
| `SAVE_TRANSCRIPTS` | `false` | có lưu transcript vào log không |
| `GEMINI_API_KEY` / `GROQ_API_KEY` | — | key cloud (bắt buộc khi LLM_BACKEND tương ứng) |
| `EDGE_TTS_VOICE` / `EDGE_TTS_RATE` | `vi-VN-HoaiMyNeural` / `+0%` | giọng đọc |
| `OFFICIAL_*` | placeholder | số nóng / bộ phận một cửa — **phải xác minh trước deploy** |

Bảo mật cấu hình: `safe_repr()`/`safe_settings_summary()` redact mọi key chứa
`api_key/token/secret/password`; secret không bao giờ in ra.

---

## 5. Dây chuyền xử lý — từng bước

Toàn bộ tại `Pipeline._run()` (`app/pipeline.py:207`). Các bước:

1. **Normalize** (`app/safety/rules.py:132`) — lowercase + gộp khoảng trắng,
   **giữ nguyên dấu** (khác với retrieval, nơi bỏ dấu để đối khớp bền vững).
   Văn bản rỗng sau normalize → router trả CLARIFY ngay.
2. **Retrieval** (`app/pipeline.py:222`) — `retriever.search(query.text,
   top_k=5)`.
3. **Routing** (`app/pipeline.py:229`) — `router.route()` xem §6.
4. **LLM** (`app/pipeline.py:236`) — chỉ khi `would_answer(decision)`. Gửi
   query + **tối đa 3 chunks** (`chunks[:3]`). Nếu LLM raise →
   `insufficient_decision()` (REFUSE) + ghi `llm_failure`.
5. **Guard không-trích-dẫn (T2, mới)** (`app/pipeline.py:254`) — answer có
   nội dung nhưng `source_ids` rỗng → REFUSE ngay, ghi `citation_rejected`
   kind=`no_citation`.
6. **CitationValidator** (`app/pipeline.py:266`, chỉ khi `app_mode != mock`) —
   validate **citations thô** (chưa lọc) trước; hỏng → REFUSE với lý do
   `CITATION_UNSUPPORTED`/`CITATION_OUTDATED`. Chỉ **sau khi** validator OK
   mới sanitize (`kept = raw_ids ∩ retrieved`).
7. **TTS** (`app/pipeline.py:293`) — `result_for_tts()` chuyển kết quả thành
   lời nói (hoàn toàn tách biệt với answer text); lỗi TTS chỉ ghi `tts_failure`
   chứ không đánh chìm câu trả lời.
8. **Log** (`app/pipeline.py:320`) — một dòng JSONL `pipeline_result` với
   zone/action/reason_codes/source_ids/latency; transcript chỉ khi bật.

**Xử lý audio** (`process_audio`, `app/pipeline.py:171`): ASR → transcript →
`_run()`; khối `finally` đảm bảo **luôn** áp `_apply_audio_privacy()` (xóa raw
audio **chỉ khi** file nằm trong `data_dir` và `DELETE_RAW_AUDIO_AFTER_SESSION`
bật) — kể cả khi ASR/pipeline gặp lỗi (F13).

---

## 6. Safety routing (app/safety/)

### 6.1 Rules — `rules.py`

Regex thuần (không LLM), chạy **trước mọi LLM call**:

- `_EMERGENCY_PATTERNS` (RED): cấp cứu, đột quỵ, tự tử, cháy... → ESCALATE, cần
  người.
- `_VIOLENCE_THREAT_PATTERNS` (RED): đe dọa, bạo lực, cướp, xâm hại...
- `_CRIMINAL_PATTERNS` (ORANGE/GUIDE): hình sự, khởi tố, tạm giam, tội phạm,
  bắt giữ — **không tự ý đưa ra kết luận hệ trọng**; lời thoại gợi ý liên hệ
  hotline/công an để tư vấn trực tiếp.
- `_LEGAL_PATTERNS` (ORANGE/GUIDE): tòa án, kiện tụng, tranh chấp...
- `_OUT_OF_SCOPE_PATTERNS` (ORANGE/GUIDE): xổ số, cá cược, tử vi...
- `_DOUBT_WORDS` (ambiguous): "hay là", "không biết"...

`check_rules()` trả `RuleHits`. Lưu ý: `_COMPILED`/`_N_*` là dead code (F8);
mỗi nhóm compile riêng khi gọi.

### 6.2 Router — `router.py` (thứ tự kiểm tra là hợp đồng)

1. Không phải text sau normalize → CLARIFY.
2. `emergency` → ESCALATE RED.
3. `violence` → ESCALATE RED.
4. `criminal` → GUIDE ORANGE (`CRIMINAL_MATTER`).
5. `legal` → GUIDE ORANGE.
6. `out_of_scope` → GUIDE ORANGE.
7. **Đủ nguồn**: `[c for c in chunks if c.score >= min_score]` — rỗng →
   REFUSE `INSUFFICIENT_SOURCE`. (F3: mặc định 0.01 khớp thang RRF; hybrid còn
   có gate answerability ở tầng retriever.)
8. Ambiguity: có từ ngờ vực + không chunk → CLARIFY; ≥ 2 từ ngờ vực → CLARIFY.
9. `APP_MODE=cloud` + LLM có `classify_safe` → LLM phân loại; fail → không
   auto-answer (conservative).
10. Fallback → ANSWER (YELLOW) với `SAFE_GROUNDED_QUERY`.

LLM **không bao giờ** tự quyết routing; rule hit luôn thắng.

### 6.3 Policy — `policy.py`

Chuyển hit → `SafetyDecision` (zone/action/reason_codes/user_message/
requires_human) với lời thoại tiếng Việt cẩn trọng, chung chung, không tự nhận
mình là cơ quan nhà nước.

---

## 7. Retrieval (app/retrieval/)

### 7.1 BM25 — `bm25_retriever.py`

Thuần Python (không numpy/sklearn). Điểm quan trọng:

- **Tokenizer**: regex 2 nhóm — ASCII `[a-zA-Z0-9_]+` + một tập ký tự Việt có
  dấu; sau đó **NFD bỏ dấu + casefold** (`normalize_vietnamese`). Vì bỏ dấu nên
  mọi token so khớp là dạng không dấu ("thủ" → "thu").
- **Stopwords tiếng Việt** (không dấu): "toi", "cua", "la", "gi"...
  (`_VIETNAMESE_STOPWORDS`) — chặn query chung chung đẩy điểm.
- **Điểm**: Okapi BM25 k1=1.5, b=0.75, `idf = log(1 + (N-df+0.5)/(df+0.5))`.
- **Guards**:
  - `min_token_overlap = 2` — chunk phải chứa ≥ 2 token phân biệt của query;
    **tự động bỏ qua khi query chỉ có 1 token** (F4 fix — từ đơn hợp lệ như
    "khai" vẫn tìm được).
  - **T3 (mới)**: query 1 token mà token xuất hiện trong >50% corpus (df quá
    cao, ví dụ "tục") → trả `[]` (quá generic).
- Chỉ trả về các chunk có score > 0.

### 7.2 Hybrid — `hybrid_retriever.py`

BM25 + dense (`intfloat/multilingual-e5-small`, cosine, normalize embedding,
cache `.npz` — cache chỉ hợp lệ khi danh sách chunk_id khớp) → **RRF fusion**
(k=60, score = Σ 1/(60+rank+1)) → optional rerank (`cross-encoder/
mmarco-mMiniLMv2-L12-H384-v1`) — **rerank chỉ sắp xếp lại, không quyết định**
(trừ gate="none").

**Gate "answerability"** (chuẩn trên corpus thật): `max_bm25 >= 12.2 OR
max_dense >= 0.88` nếu không → `[]`. Nghĩa là: câu hỏi ngoài corpus ("hộ
chiếu", "phạt khai sinh quá hạn") bị chặn từ tầng retrieval — layer chống
"trả lời đại".

**F5 fix** (`app/pipeline.py:46`): `RETRIEVAL_BACKEND=hybrid`:
- Có `real_chunks.jsonl` → dùng corpus thật + cache riêng; `exclude_demo` bật
  khi `app_mode != mock`.
- Không có → mode mock: dùng demo chunks + cache **của riêng demo**
  (`demo_embeddings.npz`), không filter demo; mode khác: **raise RuntimeError**
  (fail loud, không lặng lẽ trả rỗng).

### 7.3 Document loader — `document_loader.py`

- Front matter `--- key: value ---` mini-parser; `source_id` lấy từ meta hoặc
  tên file; `is_demo` = có từ khóa DEMO/SYNTHETIC trong license/notes/nội dung.
- Chunk theo đoạn văn, mục tiêu 900 ký tự, para dài bị cắt với overlap 120;
  `chunk_id = f"{source_id}::c{idx:03d}"`.
- Ghi `demo_chunks.jsonl` + `metadata.csv`.

---

## 8. LLM (app/llm/)

`BaseLLM.generate_answer(query, chunks, max_chars) -> dict` JSON với keys:
`answer_text, spoken_citation, source_ids, limitations, next_step`.

- **MockLLM** (mặc định): template rút 3 câu đầu từ chunk nội dung tốt nhất
  (bỏ qua chunk bắt đầu bằng `#` hoặc chứa "LƯU Ý QUAN TRỌNG"); source_ids
  **luôn** từ chunks đã truy xuất → không thể bịa nguồn. Là safe fallback của
  mọi chế độ.
- **GroqLLM**: system prompt yêu cầu grounded + JSON; retry 3 lần khi
  JSONDecodeError; map `chunk_id` → `source_id` nếu LLM trả chunk_id;
  **không** lọc source_ids ở tầng này (F2 — để validator bắt hallucination).
- **GeminiLLM**: cùng schema; lưu ý system prompt hiện nằm trong user parts
  (F6 — đã biết, cải thiện sau), chỉ retry 1 lần qua SDK.
- Cả hai đều `.removeprefix("```json")` để chịu được LLM bọc code block.

**Không gửi gì ngoài**: transcript + chunks đã truy xuất. Không gửi audio.

---

## 9. Grounding: CitationValidator (app/validation/citation_validator.py)

Chạy khi `app_mode != mock`. Registry thủ công có kiểm chứng:
`data/law_status.json` (`sources: {source_id: {ky_hieu, trich_yeu, expired_on,
replaced_by}}`).

`validate(answer, retrieved_sources)` — mỗi `source_id` trong answer:
1. **unknown** — không có trong registry → fail.
2. **outdated** — `expired_on <= today` → fail, kèm `replacement` (mô tả văn
   bản thay thế).
3. **unsupported** — có registry, còn hiệu lực, nhưng **không nằm trong** các
   nguồn đã truy xuất → fail.

Kết quả: `CitationVerdict(ok, issues)`. Pipeline biến fail thành ORANGE/REFUSE
(`citation_decision(outdated=...)`). **Thứ tự quan trọng (F2 fix)**: validator
xem citations thô; sanitize chỉ xảy ra sau khi verdict OK.

---

## 10. TTS (app/tts/)

- **MockTTS**: trả về text, không tạo file thật.
- **EdgeTTS**: `vi-VN-HoaiMyNeural`, cache theo sha256(`voice|rate|text`)
  trong `results/tts_cache` (không gọi mạng khi trùng text). Cần mạng lúc chạy.
- `result_for_tts()` tạo PipelineResult tối giản chỉ để dựng lời nói — lời nói
  ≠ answer text (có thêm lời dẫn, hạn chế...).

---

## 11. Hội thoại (app/dialogue/)

- **state_machine.py**: 12 trạng thái (WELCOME → DISCLAIMER → LISTENING →
  TRANSCRIBING → RETRIEVING → SAFETY_CHECK → HOLDING → SPEAKING →
  CLARIFYING/ESCALATING/DONE/ERROR) với bảng chuyển tiếp hợp lệ `_EDGES`;
  chuyển sai → `TransitionError`. Machine thuần, test được.
- **commands.py**: lệnh giọng nói tiếng Việt (nói lại, nói chậm, bước tiếp
  theo, nguồn ở đâu, hỏi người thật, kết thúc, trợ giúp) — match prefix trong
  transcript.

### CLI (app/cli.py)

`python -m app.cli [--transcript "..."] [--audio path] [--once]`. In đầy đủ
routing/retrieval/answer/guidance/latency. `delete_session()` được gọi ở cuối
(cleanup log). Windows console được ép UTF-8.

### UI (app/ui.py)

Streamlit tùy chọn: trạng thái config, hỏi-đáp, hiển thị zone/action/reason
codes/answer/chunks/latency, nút xóa phiên. Không hiện secret.

---

## 12. Privacy & logging (app/logging_utils.py)

- Session ID: `uuid4().hex[:16]`; timestamp UTC ISO.
- `JsonlLogger.log()`: **mọi** record được `scrub_value()` trước khi ghi:
  - email → `[EMAIL_REDACTED]`
  - chuỗi giống số điện thoại → `[PHONE_REDACTED]` — **chỉ khi** chuỗi có
    9–15 chữ số (`_scrub_phones`, F1 fix) để không làm hỏng session_id hex
    16 ký tự / timestamp ISO.
  - chuỗi dài ≥24 ký tự → `[ID_REDACTED]`
  - **keys máy sinh được bảo toàn** (`_PRESERVED_KEYS`: session_id,
    timestamp, chunk_id, source_id); transcript/query/text được scrub nội
    dung.
- `SessionStore.delete_session()`: đọc lại file, giữ các dòng không khớp
  session_id, ghi tạm rồi replace; trả số dòng đã xóa. (F1 fix giúp nó khớp
  được session_id thật thay vì bản đã bị scrub.)
- Heuristic scrub **không** thay thế xóa dữ liệu pháp lý —
  xem `docs/privacy_deletion_policy.md`.

---

## 13. Dữ liệu (data/)

| Thư mục | Nội dung |
|---|---|
| `sources/` | markdown DEMO/SYNTHETIC (xã Bình Minh hư cấu) |
| `sources_real/` | văn bản pháp luật thật (luat46_2024, nd154_2024, nd104_2025...) |
| `chunks/` | `demo_chunks.jsonl`, `real_chunks.jsonl`, `real_embeddings.npz` (cache dense) |
| `eval/` | fixture dev/test cho R1–R4 + schemas |
| `law_status.json` | registry văn bản (expired_on, replaced_by) cho validator |
| `source_registry.csv`, `source_metadata_real.csv`, `metadata.csv` | danh mục nguồn |
| `private_cache/` | trang VBPL đã crawl (OCR) — **chưa đưa vào .gitignore đầy đủ** (F11) |

Sinh corpus thật: `scripts/crawl_vbpl.py` (crawl thuvienphapluat) +
`scripts/ocr_vbpl.py` + `scripts/ingest_documents.py` (đọc `sources/` hoặc
`sources_real/` tùy cấu hình).

---

## 14. Đánh giá (eval/) — R1–R4

| Trục | Module | Đo gì |
|---|---|---|
| R1 WER | `eval/wer.py` | ASR trên fixture `wer_dev.jsonl` (có hỗ trợ VIVOS thật) |
| R2 Retrieval | `eval/retrieval.py` | recall/precision top-k theo `retrieval_*.jsonl` |
| R3 Routing | `eval/routing.py` | độ khớp zone/action so với `routing_*.jsonl` |
| R4 Latency | `eval/latency.py` | thời gian từng tầng (ASR→TTS) |

`python -m eval.run_all` → ghi CSV + `*_summary.json` + `evaluation_report.md`
vào `results/`, tất cả kèm chú thích **SYNTHETIC DEMO - NOT PILOT RESULTS**.

Script hỗ trợ: `scripts/validate_data.py` (schema + cấu trúc fixtures),
`scripts/eval_retrieval_ablation.py`, `scripts/eval_citation_validator.py`,
`scripts/eval_vivos_real_wer.py`.

---

## 15. Tests & quality gates

```powershell
python -m pytest                        # 69 tests, -q
python -m ruff check .                  # lint (E,F,W,I; E501 ignore)
python -m ruff format --check .         # format
python scripts/validate_data.py         # dữ liệu
python scripts/preflight.py             # gate tổng: test+lint+format+demo+eval+secret scan
```

Bộ test chính:
- `test_pipeline_mock.py` — E2E mock, hallucination bị REFUSE, **answer không
  trích dẫn bị REFUSE (T2)**, audio bị xóa khi ASR fail (F13), hybrid raise
  khi thiếu real chunks (F5).
- `test_privacy_logging.py` — scrub giữ nguyên session_id/timestamp/hex 16
  ký tự; delete_session khớp đúng (F1).
- `test_config.py` — default `MIN_RETRIEVAL_SCORE == 0.01`, validate env.
- `test_safety_router.py`, `test_retrieval.py` (gồm **T3** — token generic
  1-token trả rỗng), `test_citation_validator.py`, `test_schemas.py`,
  `test_eval_and_machine.py`.

---

## 16. Audit vừa qua (16 findings) + kết quả

Đã review toàn bộ codebase, đối chiếu bằng 5 LLM trong AI pool (2 vòng xác
nhận 100%), sửa ngay các bug quan trọng:

| # | Severity | Bug | Trạng thái |
|---|---|---|---|
| F1 | CRITICAL | scrub hỏng session_id/timestamp → delete_session không hoạt động | **Đã sửa** (digit-guard 9–15 + preserve keys) |
| F2 | HIGH | filter source_ids trước validator → hallucination lọt | **Đã sửa** (validate trước, sanitize sau) |
| F3 | HIGH | min_retrieval_score mặc định 1.0 → mọi hybrid query bị từ chối | **Đã sửa** (0.01 + warn nếu >0.5) |
| F4 | MEDIUM | query 1 token bypass overlap guard | **Đã sửa** (bỏ tautology; guard hợp lý + T3) |
| F5 | MEDIUM | hybrid fallback demo + exclude_demo → trả rỗng lặng lẽ | **Đã sửa** (fail loud ở production; demo dùng cache riêng) |
| F6 | MEDIUM | Gemini system prompt nằm nhầm user parts | Chưa (F7/F6 bàn giao sau) |
| F7 | MEDIUM | Groq không retry 429/5xx | Chưa |
| F8–F9, F11, F12, F14–F16 | LOW | dead code, cache chỉ check chunk_id, secret scan thiếu mẫu, hardcode counts, normalize 2 lần, path tuyệt đối trong JSONL | Đã biết; chưa xử lý hết |
| F10 | LOW→MEDIUM | pattern "cướp"/"cháy" quá rộng → false RED | Cần review chuyên gia tiếng Việt |
| F13 | LOW→MEDIUM | audio không xóa khi ASR raise | **Đã sửa** (finally) |
| B17 | — | `SessionStore` ghi file không thread-safe | Đã biết (chưa lock) |
| B18 | — | LLM call không timeout | Đã biết |

Quyết định **council round 4** (5 models, đa số): T1 giữ `MIN_RETRIEVAL_SCORE
= 0.01`; T2 thêm guard REFUSE khi trả lời không trích dẫn (**đã code**);
T3 thêm df-guard cho query 1-token (**đã code**).

---

## 17. Hạn chế đã biết (đọc kỹ trước pilot)

- Rule an toàn là heuristic, cần chuyên gia tiếng Việt review (đặc biệt
  F10). Xem `docs/responsible_ai.md`.
- BM25 không hiểu ngữ nghĩa; không có confidence calibration.
- PhoWhisper/Edge-TTS/Gemini/Groq cần cài gói tùy chọn + (với cloud) mạng;
  chưa pilot trên phần cứng thật.
- `data/private_cache/` và token `nvapi-*`/`gho_*` chưa vào secret scan.
- Số điện thoại / lời thoại chính thức là placeholder — phải xác minh.
- Log JSONL tuyến tính, không phải database; xóa phiên chỉ xóa những gì log
  có.

---

## 18. Lộ trình gợi ý (theo thứ tự tác động)

1. F7 retry/backoff 429 + timeout (B18) cho Groq/Gemini.
2. F6 đưa system prompt vào `system_instruction` của Gemini.
3. F10: thu hẹp pattern RED gây false positive; thêm test case phủ.
4. F12: DenseIndex cache validate theo nội dung (không chỉ chunk_id).
5. F11: cập nhật secret scan (nvapi/gho_) + ignore `data/private_cache`.
6. B17: thread-safe log (lock) nếu triển khai nhiều người dùng.
7. Pilot 8–10 người theo `docs/pilot_protocol.md`.
8. Xác minh & nạp danh bạ hotline/đầu mối chuyển tuyến (xem "Danh bạ người
   tư vấn" bên dưới) — Hội đồng Round 5 chốt đây là **blocker uy tín #1**.

### Danh bạ người tư vấn (lưu sđt người tư vấn vào data của mình)

Ý tưởng người sáng lập: lưu số điện thoại **người tư vấn** (cán bộ, chuyên
viên, đầu mối từng lĩnh vực) vào `data/contacts.json` của hệ thống. Lợi ích:

- Người dân gọi lại / hỏi lại → hệ thống **biết số của ai** trong lĩnh vực đó,
  chuyển hướng đúng người, tư vấn dễ dàng và tốt hơn (thay vì placeholder
  `1900XXXX`).
- Đầu mối chuyển tuyến (hotline cơ quan, công an, trợ giúp pháp lý...) nạp 1
  lần, dùng lại ở mọi lời thoại GUIDE/RED.

Thiết kế đề xuất (cấu trúc `data/contacts.json`):

```json
{
  "contacts": [
    {
      "id": "bo-phan-mot-cua-xa-binh-minh",
      "category": "bo_phan_mot_cua",
      "label": "Bộ phận một cửa xã Bình Minh",
      "phone": "020X XXX XXX",
      "verified": false,
      "note": "Cần xác minh trước khi triển khai"
    }
  ]
}
```

- `category` nối với lời thoại: `bo_phan_mot_cua`, `hotline`, `cong_an`,
  `tro_giup_phap_ly`, `khac`.
- `verified: true` mới được hiển thị khi đưa ra sử dụng thật; chưa xác minh
  thì dùng câu chung chung như hiện tại (không đọc số ảo).
- Sđt của **người tư vấn** là dữ liệu của hệ thống (không phải PII của người
  dân); vẫn đặt trong `.gitignore`-able nếu đội vận hành muốn riêng tư, và
  không bao giờ ghi vào log.
- Bước hiện thực hóa: tạo file → nạp số thật (xác minh bằng cuộc gọi thử) →
  thay placeholder trong `Policy` → test R3.

### Ưu tiên đồng thuận Hội đồng Round 5 (5 mô hình)

1. Xác minh hotline/đầu mối chuyển tuyến (chi phí thấp, blocker uy tín).
2. Backend tối thiểu đa người dùng: auth, rate-limit, giám sát, audit log.
3. Thay mock ASR/TTS bằng pipeline thật + đo WER/độ trễ trên audio thật.
4. Pilot 8–10 người thật (đo Task Success Rate, CSAT).
5. Local inference (ASR/TTS/OCR ảnh) — vừa bảo vệ PII vừa là điểm khác biệt.

### Ý tưởng sau pilot (chưa triển khai)

- **Gửi ảnh qua chat để AI xem xét** (vd gửi ảnh hợp đồng lao động, giấy tờ
  cần hỏi) → OCR + LLM đọc tài liệu cá nhân. **Yêu cầu privacy cao**: ảnh/tài
  liệu là PII nhạy cảm, nên ưu tiên **inference local** (LLM/OCR chạy trên máy
  người dùng, không gửi dữ liệu lên cloud) — thiết kế ngay tầng "multimodal
  local-first" kèm quy tắc xóa ảnh sau phiên như audio thô.

---

## 19. Hội đồng Round 5 — tiềm năng phát triển & độ sẵn sàng thực tế

Hỏi 5 mô hình AI độc lập (laguna, nemotron-3-ultra, nemotron-nano, minimax-m3,
m365-copilot) 2 chủ đề: tiềm năng phát triển sản phẩm, và đánh giá tiến độ kỹ
thuật so với đưa vào sử dụng thực tế. Nội dung gốc: `results/round5_debate.json`.

### Chấm điểm độ sẵn sàng (trung bình ~6.3/10)

| Mô hình | Điểm | Lý do chính |
|---|---|---|
| minimax-m3 | 5/10 | Đủ demo nội bộ, chưa đủ dùng công khai |
| laguna-s-2.1 | 6/10 | Kiến trúc vững nhưng chưa kiểm chứng audio thật |
| nemotron-3-ultra | 6.5/10 | Core RAG+Safety+Validation production-grade; trừ 3.5 vì chưa pilot/audio/server |
| nemotron-nano | 7/10 | Vượt 73 tests, ruff, R1–R4; thiếu xác thực ASR/TTS + auth/rate-limit |
| m365-copilot | 7/10 | Kiến trúc, safety, grounding, kiểm thử nội bộ tương đối trưởng thành; chưa chứng minh ngoài synthetic |

### Điểm mạnh khác biệt (đồng thuận 5/5)

- Voice-first tiếng Việt + **bám nguồn + trích dẫn + safety routing** là điểm
  khác biệt thật so với cổng DVC/chatbot hành chính text-only, không chống
  outdated/hallucinated.
- "Biết nói không" (gate answerability + CitationValidator) và chuyển hướng an
  toàn cho hình sự — lấp đúng khoảng trống người cao tuổi/bận rộn gọi như
  hotline.

### Nhóm người dùng / hướng kế tiếp (đồng thuận)

- Người bận rộn (shipper, công nhân) hỏi nhanh quyền lợi BHXH/lao động; người
  cao tuổi/nông thôn vùng sâu (chỉ có điện thoại, 4G yếu); doanh nghiệp nhỏ/hộ
  kinh doanh (đăng ký kinh doanh, thuế); bộ phận một cửa và tổng đài tỉnh
  (B2B/B2G: AI hỗ trợ cấp 1).
- Hướng giá trị nhất 6–12 tháng: **xác minh hotline + danh bạ chuyển tuyến**,
  **local inference** (ASR/TTS/OCR ảnh — vừa chống rò PII vừa giảm chi phí
  cloud khi scale), **pilot người dùng thật**, mở rộng corpus (nghĩa vụ quân
  sự, đất đai — nhu cầu cao, ít cạnh tranh).

### Khoảng trống nghiêm trọng nhất (5 mô hình đều nêu)

1. ASR/TTS chưa validate trên audio thật (giọng già, vùng miền, nhiễu).
2. Chưa có server đa người dùng (auth, rate-limit, giám sát, audit log).
3. Số hotline/one-stop placeholder `1900XXXX` chưa xác minh — rủi ro uy tín
   và pháp lý ngay khi triển khai.
4. Eval dùng fixture synthetic — chưa có ground truth từ chuyên gia/luật sư.
5. Chưa có quy trình cập nhật văn bản pháp luật liên tục.

### Rủi ro lớn nhất

Sai luật gây hại cho người dân → trách nhiệm pháp lý; hotline sai làm sụp uy
tín; chi phí cloud khi scale; ASR tiếng Việt vùng miền chưa kiểm chứng; người
dùng hiểu sai/áp dụng sai dù câu trả lời đúng luật.

### Điều kiện tối thiểu để "sẵn sàng pilot thực tế"

- Hotline/đầu mối chuyển tuyến đã xác minh.
- ASR/TTS được test với nhiều giọng địa phương; latency trung bình < 2s.
- Có cơ chế báo lỗi/phản hồi người dùng + giám sát hệ thống + audit log.
- Tỉ lệ trả lời qua CitationValidator đạt mức ổn định; test E2E với người
  thật tối thiểu vài phiên.

> Kết luận hội đồng (m365-copilot): *"Tiếng Làng có định vị rõ ràng, khác
> biệt, tiềm năng tác động xã hội cao; kỹ thuật đã vượt giai đoạn prototype
> nhưng cần chứng minh bằng pilot thực tế và vận hành production trước khi mở
> rộng quy mô."*

---

## 20. Bản đồ tài liệu (docs/)

| Tài liệu | Nội dung |
|---|---|
| `architecture.md`, `setup.md`, `demo_script.md` | kiến trúc, cài đặt, kịch bản demo |
| `evaluation_protocol.md`, `evaluation_dataset_card.md` | cách chấm R1–R4, nguồn fixture |
| `data_card.md`, `assumptions.md`, `baseline_before_full_integration.md` | dữ liệu & giả định |
| `responsible_ai.md`, `threat_model.md`, `privacy_deletion_policy.md`, `limitations.md` | an toàn & riêng tư |
| `deployment_strategy.md`, `hardware_benchmark_plan.md`, `pilot_protocol.md` | triển khai & pilot |
| `rubric_evidence_matrix.md` | bằng chứng đối chiếu tiêu chí đánh giá cuộc thi |
| `data/contacts.json` | danh bạ người tư vấn / đầu mối chuyển tuyến (sđt) |
| `team_status.md` | trạng thái hằng ngày theo vai T/C/P + gate A–D |
| `submission_checklist.md` | kế hoạch ≥45/50 VAIFF 2026, mốc thời gian đến 25/08 |

Báo cáo gần đây: `OPENCODE_PREPARATION_REPORT.md`,
`OVERNIGHT_FULL_INTEGRATION_REPORT.md`, `results/evaluation_report.md`,
`results/round5_debate.json` (hội đồng Round 5: tiềm năng & độ sẵn sàng).
