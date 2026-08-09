# Privacy & Security Checking — Tiếng Làng v4.0

> **NHÁP — chờ bạn (T) đọc và chốt.** Không push lên GitHub (theo yêu cầu).
> Nguồn: Hội đồng Round 9 — 6 vòng thảo luận liên tục, 5 mô hình + OpenCode
> (thành viên thứ 6), mỗi vòng mỗi thành viên phải phân tích ý kiến các thành
> viên khác rồi mới cập nhật ý kiến mình. Dữ liệu đầy đủ:
> `debate_output/round9.json`, `debate_output/round9_final.txt`.

## 1. Quá trình & trạng thái đồng thuận

- Số vòng: **6** (không giới hạn thời gian; dừng khi đạt đồng thuận tối đa).
- Biến động AGREEMENT qua vòng: m365-copilot YES (một phần PARTIAL giữa chừng
  rồi quay về YES 3 vòng cuối); nemotron-3-ultra YES từ vòng 4; nano-omni
  PARTIAL tới vòng cuối; laguna + minimax không ghi dòng AGREEMENT theo format
  (cắt token) nhưng nội dung đến vòng 6 đều là "đồng ý + chỉ còn bổ sung nhỏ".
- **Kết luận**: đồng thuận trên các điểm chính 5/5 (chi tiết bên dưới); phần
  còn bất đồng chủ yếu là **mức độ nghiêm trọng theo từng giai đoạn**, không
  phải nội dung biện pháp.

## 2. Ma trận rủi ro ĐỒNG THUẬN (sắp theo ưu tiên)

`[Tác động ẩn / Khả năng]` — ưu tiên giảm dần. (Quy ước: Cao/Trung/Thấp)

| # | Rủi ro | Giai đoạn áp dụng | Mức | Biện pháp giảm thiểu (đồng thuận) |
|---|---|---|---|---|
| 1 | **Transcript chứa PII đi ra LLM API ngoài** (Groq/Gemini) khi chạy cloud — không có DPA/0-retention bằng văn bản | public link, pilot | Cao/Cao | (a) rà lại cấu hình outbound; (b) poliy scrub PII trước khi gửi ra ngoài; (c) consent + chỉ bật cloud cho pilot khi đủ điều kiện; (d) hỏi đối tác về 0-retention/DPA (driver risk) |
| 2 | **Log JSONL lưu dài, chứa transcript + metadata, không retention/rotation** | mọi giai đoạn | Cao/Cao | chính sách retention (vd xóa sau 30 ngày), rotation hàng ngày, transcript mặc định TẮT |
| 3 | **API key / secret lộ khi deploy Streamlit Cloud** (debug mode, `st.secrets` trong traceback, exception log) | public link | Cao/Trung bình | secrets management đúng (Streamlit Secrets, không debug), test traceback không in key, không dính vào repo |
| 4 | **Prompt injection qua voice** (ASR hallucination → chỉ thị độc hại vào pipeline) | pilot, public | Medium-High | red-team/adversarial test TRƯỚC pilot; router + citation guard đã có; một số thành viên yêu cầu nâng mức (sửa lại ý kiến ban đầu của OpenCode: đúng là không nên xếp thấp) |
| 5 | **PII scrubber bằng regex không đủ cho tiếng Việt** (CCCD, BHYT, "xóm 3, thôn Đông", quasi-identifiers → tái nhận dạng) | mọi giai | Cao/Trung bình | LLM-based redaction hoặc human-in-the-loop; generalization (thô hoá địa chỉ/ngữ cảnh) trước khi ghi log; không coi regex là biện pháp chính |
| 6 | **Raw audio/TTS/session artifacts sót sót trên đĩa** do cấu hình sai hoặc crash | local, pilot | Trung bình | kiểm tra cờ `DELETE_RAW_AUDIO_AFTER_SESSION`, cleanup tự động results/ + logs/, test crash-path |
| 7 | **`data/contacts.json` (SĐT thật) nằm trong repo nộp hồ sơ** | nộp hồ sơ | Cao | tách khỏi repo nộp hoặc mã hoá; giữ private repo riêng |
| 8 | **Side-channel `/tmp` Streamlit Cloud** (artifact tạm, debug endpoint, path traversal) | public link | Trung bình | không ghi PII vào /tmp; kiểm tra cấu hình runtime; xoá sau mỗi request |
| 9 | **Vendor/Distribution risk**: sub-processors, địa chỉ dữ liệu, Nghị định 13/2023, GDPR 72h | pilot, nộp | Trung bình | yêu cầu DPA/BAA; tài liệu flow dữ liệu; kế hoạch incident response (thông báo 72h) |
| 10 | **DDoS/abuse public link** (trả phí LLM bị khai thác, spam) | public link | Trung bình | giới hạn rate, whitelist/kiểm tra, giới hạn token/char, quan sát chi phí |
| 11 | **Embedding npz cache bị đảo ngược/suy luận** | mọi giai | Thấp (nội dung công khai) | 1 thành viên cho rằng Medium ở bản sau; đa số đồng ý Thấp vì văn bản luật công khai — ghi nhận, giai đoạn pilot lại nhắc |
| 12 | **Consent/anonymisation pilot chưa chuẩn** (quyền rút lui, phương thức ẩn danh chưa rõ) | pilot | Cao | consent form (C) + quy trình ẩn danh rõ, 2 người ngoài team kiểm thử trước |

## 2.5 PHẢN BIỆN Round 10 — mức rủi ro ĐÃ ĐIỀU CHỈNH cuối (chốt 5/5 + OpenCode)

> Nguồn: `debate_output/round10.json` — mỗi thành viên bác bẻ ≥2 ý kiến của
> thành viên khác + tự bệnh. Đây là bảng chốt cuối sau phản biện.

| # | Rủi ro | Mức CHỐT (giai đoạn hiện tại) | Ghi chú phản biện |
|---|---|---|---|
| 1 | PII outbound → LLM cloud | **Likelihood Thấp–Medium / Impact Cao** (nâng lên Cao/Cao nếu bật cloud thật) | 3/5 phản biện "Cao/Cao" là định cựa: hiện mock local, exposure=0. Chỉ áp dụng khi pilot bật Groq/Gemini |
| 2 | Log JSONL không retention | **Cao** (giữ nguyên) | không ai phản biện |
| 3 | API key leak Streamlit | **Cao** (khi public link) | laguna phản biện ai nói "Thấp" là sai |
| 4 | Prompt injection qua voice | **Medium** (red-team TRƯỚC pilot vẫn bắt buộc) | m365+nano phản biện hạ: không tool execution/agent → tác động giới hạn, không phải top-5 privacy |
| 5 | PII scrubber regex VN yếu | **Medium-High** (vẫn là ràng buộc trước pilot) | laguna hạ bớt (mock, chưa outbound) — chốt trung gian |
| 6 | Audio/artifacts sót trên đĩa | **Medium** (verify code + %TEMP%/backup cloud cá nhân) | nano hạ Thấp (đã có delete design); minimax nâng Medium-High (chưa có bằng chứng os.remove mọi path) |
| 7 | contacts.json trong repo nộp | **Medium** hiện tại / **Cao** nếu đi theo artifact nộp | laguna làm rõ: local private chưa nối API |
| 8 | Side-channel /tmp Streamlit | **Thấp** (demo/pilot nhỏ, chưa multi-tenant) | nano + m365 phản biện hạ |
| 9 | Vendor risk (DPA, NĐ 13/2023) | **Medium** — quan trọng nhưng đứng sau việc phá demo | m365 tự bệnh: prototype 8-10 người, chưa quy mô xuyên biên giới |
| 10 | DDoS/abuse link | **Trung bình** (khi public) | giữ |
| 11 | Embedding npz inversion | **THẤP — ĐÃ XÁC MINH CODE**: npz chỉ cache vector corpus (văn bản luật công khai); query encode tại chỗ không lưu (`hybrid_retriever.py` L70-77 vs L92-95) | nemotron-3-ultra + minimax phản biện nâng "nếu cache query"; verify → điều kiện không xảy ra |
| 12 | Consent/anon pilot chưa chuẩn | **Cao** (pilot 20/08) | giữ |

**RỦI RO BỎ SÓT ĐƯỢC BỔ SUNG (đồng thuận thêm vào):**
- **#13 Mock-mode drift / false confidence** — demo deterministic bằng Mock LLM che latency/WER/hallucination thật; nếu hội đồng VAIIF26 test live sẽ trượt. → **Real-mode E2E smoke test ≥10 queries trước 20/08** (nemotron-3-ultra, không ai phản biện).
- **#14 Explainability router** — người dùng không biết vì sao bị từ chối/chuyển hướng (laguna) → đã có `user_message`, cần siết thêm.
- **#15 Router fail-open** — RED thành YELLOW khi lỗi = rủi ro trust (m365) → cần test fail-closed + số liệu production-like.
- **#16 Human dependency** — C chưa deliver, P chưa tuyển = rủi ro deadline lớn nhất (4/5 nhắc) → daily standup 15' + minimum viable deliverable (C: 5 kịch bản; P: ≥3 user).
- **#17 Mock LLM lặp PII từ RAG context** (minimax) → test với pilot data thật.

## 2.6 KẾT LUẬN CUỐI (sau phản biện)

- Đồng thuận: **top-5 privacy ưu tiên = outbound PII (khi cloud) · retention log · API key Streamlit · scrubber VN + quasi-identifiers · consent/anon pilot**.
- 3 việc NGAY tuần này: (1) real-mode smoke ≥10 queries; (2) C/P deliver tối thiểu + standup 15'; (3) quyết định cloud mode cho public link + bảo vệ key + retention.
- File này KHÔNG push — chờ T đọc và chốt.

## 3. Câu hỏi mở cần con người (C/T/P) trả lời1. C: consent form có định rõ "ẩn danh" là gì (bỏ tên, bỏ địa chỉ nhỏ nhất, giữ giọng nói?)? Pilot có thu audio thật không — nếu có, consent riêng cho audio?
2. C: quyết định retention log bao lâu (đề xuất 30 ngày) — T cài đặt theo quyết định này.
3. T: public link — chạy cloud LLM thật hay mock-only? Nếu thật, làm scrub outbound trước khi deploy (deadline 12/08). **→ ĐÃ CHỐT (08/08): CLOUD là chính (vốn + giới hạn phần cứng); local = phương án chuyên nghiệp/on-prem cho tổ chức. T đã hiện thực scrub outbound (`app/privacy/scrubber.py`, `PII_SCRUB_OUTBOUND=true`, 83 tests xanh). Còn lại: bảo vệ key Streamlit + rate limit khi deploy link.**
4. T/C: `contacts.json` — giữ trong repo private OK, nhưng loại khỏi bản nộp; hay ché khỏi repo luôn?
5. P: pilot — có cần test adversarial trước (tôi chuẩn bị bộ test nếu đội duyệt)?
6. C: claim "0-retention / không lưu PII" — đẩy mạnh ở đâu (form, README) phải phù hợp thực tế công nghệ đang chạy (mock/local ở mock = không outbound).

## 5. Việc cần làm tiếp (đề xuất, chờ T chốt)

| # | Việc | Owner | Deadline |
|---|---|---|---|
| 1 | Baseline: ghi nhận các rủi ro này vào `docs/threat_model.md`/`responsible_ai.md` | T (sau khi T duyệt file này) | 08/08 |
| 2 | Scrub PII trước outbound + giới hạn rate/char cho public link | T | 12/08 |
| 3 | Retention/rotation log (dọn 30 ngày, tắt transcript mặc định) | T | 12/08 |
| 4 | Quyết định consent + ẩn danh pilot | C | 09/08 |
| 5 | Red-team prompt injection (voice) — bộ test adversarial | T (hỗ trợ khi được nhờ) | 15/08 |
| 6 | Tách contacts.json khỏi bản nộp / mã hoá | C+T | 23/08 |

## 6. Lưu ý trung thực (honesty guard)

- Chưa có chính sách chính thức về DPA của Groq/Gemini. Không viết claim "dữ
  liệu không rời khỏi máy" khi cloud mode bật thật.
- Mọi ghi chép trên là BẢN NHÁP của hội đồng AI pool — các biện pháp phải
  được con người (T theo môn quyết định) đánh giá rồi thực hiện.