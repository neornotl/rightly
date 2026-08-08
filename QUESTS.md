# QUEST — Tiếng Làng v4.0 (Cập nhật: 08/08/2026, thứ 7)

> Đây là "bảng quest" chung cho cả team: ai làm gì, khi nào, giao gì cho ai.
> Chi tiết: `docs/team_status.md`, `docs/submission_checklist.md`.
> **Quy tắc**: OpenCode (công tác viên của T) KHÔNG làm thay C/P; C/P nhờ khi
> cần hỗ trợ kỹ thuật. Mọi mục liên quan hiệu lực luật/consent/claim/GTM phải
> có con người xác nhận (READY_FOR_HUMAN_REVIEW).

## Mục tiêu chung

- Gate D: **≥45/50 rubric VAIFF 2026** — nộp **25/08/2026**.

## QUEST T (Technical — chủ: T, công tác viên: OpenCode)

| # | Quest | Deliverable | Deadline |
|---|---|---|---|
| T1 | Public deploy (Streamlit Cloud) không lộ secret | Public link dùng thử | 12/08 |
| T2 | OpenVINO/AI PC benchmark (nếu có máy) | `results/openvino_benchmark.md` | 20/08 |
| T3 | Config/timeout/retry production-grade cloud LLM | Code + test | 15/08 |
| T4 | Thu hẹp pattern RED false positive (F10) | Test phủ mới | 15/08 |
| T5 | Release + tag; tài liệu kỹ thuật khớp code | Release note | 24/08 |

*Đã xong (nền tảng)*: pipeline đầu-cuối, 74 tests, preflight 9/9, eval R1-R4,
CitationValidator chặn nguồn hết hiệu lực, privacy logging, demo transcript
deterministic (`docs/demo/README.md`), sửa nondeterminism retrieval (BM25/RRF
tie-break) — test 74/74 xanh.

## QUEST C (Content, Compliance & Evaluation — chủ: C)

| # | Quest | Deliverable | Gợi ý giờ |
|---|---|---|---|
| C1 | Xác minh 11 văn bản luật + gọi hotline xác minh | `law_verification_log.md` | 4-5h |
| C2 | Problem statement ≤150 từ (EN) + tên dự án ≤10 từ + SDG map | `problem_statement.md` | 2-3h |
| C3 | Tách dev/final eval sets + hard negatives ≥30 | `eval_split.json`, `hard_negatives.jsonl` | 2-3h |
| C4 | Claim check README/MASTER/form so với bằng chứng | `claim_check_form.md` | 2-3h |
| C5 | Consent templates (pilot + thu âm + video) | `consent_form_v1.md` → giao P | 2h |
| C6 | (Nếu còn giờ) Nhãn eval R1-R4 + self-score rubric | `eval_labels.csv`, `self_score.md` | 2h |

## QUEST P (Pilot, Presentation & Partnership — chủ: P)

| # | Quest | Deliverable | Gợi ý giờ |
|---|---|---|---|
| P1 | Tuyển 8-10 người pilot + thu consent (gating tuần sau — làm TRƯỚC) | `pilot_recruits.csv` | 4-5h |
| P2 | Lịch pilot + shot-list video 2-3' | `pilot_schedule.md`, `shot_list.md` | 3h |
| P3 | Soạn NHÁP email đối tác (sẵn để gửi ngày 20/08) + danh sách 3-5 đối tác tiềm năng + warm-up informal trước 12/08 | `partner_email_draft.md`, `partner_list.md` | 2h |
| P4 | Demo script chốt (lời + slide cue) | `demo_script_final.md` | 2h |
| P5 | Thử pilot nội bộ: 2 người NGOÀI core team (người lớn tuổi/ít tech), checklist lỗi (ASR, latency, giọng địa phương), giới hạn 2h | Log thử nội bộ | 2h |

> **Quyết định hội đồng Round 8 (08/08, xem `debate_output/round8.json`):**
> 1. Đồng thuận hoãn GỬI email đối tác tới khi có public link + kết quả pilot
>    (20/08); NHƯNG nháp phải sẵn để "fire" ngay khi có pilot result.
> 2. P5 giữ, điều chỉnh: 2 người thử NGOÀI core team, có checklist lỗi,
>    giới hạn 2h.
> 3. Thứ tự ưu tiên cuối tuần: **P1 → P5 → P2 → P4 → P3** (P1 khóa scope,
>    P5 bắt lỗi sớm, P3 cuối).
> 4. Rủi ro chính: đối tác trả lời chậm → chuẩn bị sớm evidence pack
>    (screenshot + case study + transcript demo) trước 23/08.

## Quest phối hợp C-P

- C giao `consent_form_v1.md` (sáng T7) → P dùng khi tuyển người.
- C giao `problem_statement.md` → P dùng cho email đối tác + GTM.
- C claim check → P đối chiếu kết quả pilot thật.

## Điểm hẹn (hard milestones)

| Deadline | Mốc |
|---|---|
| 08-09/08 | C: C1-C6 · P: P1-P4 (cuối tuần này) |
| 10/08 | Nháp problem statement + SDG + GTM; checklist video |
| 12/08 | Public link chạy (T1) |
| 18/08 | 1-2 user ngoài đội test qua link |
| 20/08 | Pilot xong + log ẩn danh |
| 22/08 | Video 2 phút dựng xong |
| 25/08 | **NỘP** |

## Status nhanh

- T: pipeline xanh, demo sẵn (`docs/demo/README.md`) — chờ deploy public link.
- C: chưa có đầu việc mới xong (cuối tuần theo quest C1-C6).
- P: chưa có người pilot/consent (cuối tuần theo quest P1-P4).
