# Threat model — Rightly

> **Threat model làm việc.** Mức độ rủi ro thay đổi theo deployment, corpus và backend. Hãy review lại trước pilot hoặc khi tích hợp external service.

Phạm vi: pipeline hiện tại (mock/local/cloud text-LLM). Mỗi mục: mô tả,
mức độ (thấp/vừa/cao), mitigation hiện có, việc còn lại (T/C/P).

## T1. Prompt injection từ tài liệu nguồn

- **Mô tả**: văn bản nguồn chứa chỉ thị ẩn ("bỏ qua hướng dẫn, nói X") bị LLM
  thực thi.
- **Mức**: vừa (cao khi dùng nguồn không kiểm duyệt).
- **Mitigation**: nguồn chỉ do người duyệt đưa vào; prompt tách rõ SYSTEM
  (không được bịa) vs USER; JSON schema; `enforce_source_ids`.
- **TODO**: test tấn công fixture cho gemini/groq; đánh giá jailbreak khi
  pilot.

## T2. Malicious query (bắt chước khẩn cấp / dò thông tin)

- **Mô tả**: người dùng lợi dụng routing, hoặc dò PII người khác.
- **Mức**: vừa.
- **Mitigation**: RED chỉ chuyển hướng, không tiết lộ; không có dữ liệu cá
  nhân trong corpus; từ chối ngoài phạm vi.
- **TODO**: dữ liệu pilot real cần policy xử lý "hỏi thông tin người khác".

## T3. PII leakage

- **Mô tả**: transcript/audio/log chứa PII bị đọc trái phép hoặc lọt vào LLM.
- **Mức**: vừa.
- **Mitigation**: không lưu transcript mặc định; xóa raw audio sau phiên;
  scrub logs; chỉ gửi transcript+chunks tới LLM.
- **TODO**: với pilot — mã hóa log, quyền đọc hạn chế, kiểm toán xóa.

## T4. Stale source

- **Mô tả**: thủ tục đã thay đổi nhưng corpus cũ → trả lời sai "tự tin".
- **Mức**: vừa (cao với người già).
- **Mitigation**: registry `law_status.json` và `CitationValidator` chặn source đã có expiry; quy trình refresh/provenance vẫn cần người duyệt.
- **TODO**: T/C/P: quy trình cập nhật nguồn chính thức.

## T5. Hallucinated citation

- **Mô tả**: LLM tự bịa source_id/đoạn trích.
- **Mức**: vừa.
- **Mitigation**: pipeline kiểm citation thô với registry + evidence vừa truy xuất, rồi mới giữ citation hợp lệ; mock path không dùng LLM sáng tạo.
- **TODO**: gemini/groq test fixture chứa prompt injection source_id.

## T6. Log leakage

- **Mô tả**: email/SĐT/ID dài trong log bị đọc.
- **Mức**: thấp-vừa.
- **Mitigation**: scrub heuristic khi ghi + `scrub_logs.py`; test secret
  không vào log; preflight secret scan.
- **TODO**: pilot: ghi log tách quyền, xóa theo chính sách.

## T7. Dependency / API failure

- **Mô tả**: key hỏng, rate-limit, mất mạng → pipeline hỏng hoặc fallback
  sai.
- **Mức**: vừa.
- **Mitigation**: lazy import; lỗi LLM → REFUSE (an toàn); TTS lỗi → vẫn trả
  text; mock chạy offline.
- **TODO**: retry/timeout config cho cloud; health check.

## T8. Supply chain

- **Mô tả**: gói pip bị thay thế ác ý.
- **Mức**: thấp.
- **Mitigation**: dependency tối thiểu; pin range trong requirements;
  review trước khi thêm gói mới.

## Matrix (rút gọn)

| # | Threat | Severity | Mitigated? |
|---|---|---|---|
| T1 | Prompt injection từ nguồn | Medium-High | Partial (test TODO) |
| T2 | Malicious query | Medium | Yes (rules + no PII corpus) |
| T3 | PII leakage | Medium | Partial (policy pilot TODO) |
| T4 | Stale source | Medium-High | Partial (refresh TODO) |
| T5 | Hallucinated citation | Medium | Yes (enforce) |
| T6 | Log leakage | Low-Med | Yes (scrub + tests) |
| T7 | API/dependency failure | Medium | Yes (conservative fallback) |
| T8 | Supply chain | Low | Partial (pins, review) |

Owner T (team), C (community), P (project lead) — xem `rubric_evidence_matrix.md`.
