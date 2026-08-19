# Deliverables — nơi lưu artifact theo vai trò

> **Lưu ý trạng thái:** các quest, deadline và bảng “chờ nộp” bên dưới là kế hoạch lịch sử. Chỉ dùng quy ước đặt tên, privacy và evidence; kiểm tra task tracker hiện hành trước khi tạo deliverable mới.

> Mỗi thành viên nộp kết quả quest của mình vào đúng thư mục vai trò:
> `deliverables/C/` (Content & Compliance) · `deliverables/P/` (Pilot & Partnership) · `deliverables/T/` (Technical).

## Quy ước nộp (bắt buộc)

1. **Tên file**: `<quest-id>_<mô tả ngắn>.md` (vd `C1_law_verification_log.md`),
   dữ liệu CSV/JSON giữ đúng tên quest (`P1_pilot_recruits.csv`).
2. **Kèm header template** ở đầu file: xem `_TEMPLATE.md`.
3. **Trạng thái** ở dòng đầu file (sau template): `[DONE]`, `[IN-PROGRESS]`,
   `[BLOCKED - lý do]`, hoặc `[READY_FOR_HUMAN_REVIEW]`.
4. **Không nộp**: API key, mật khẩu, SĐT thật, audio/video chưa có consent.
   File chứa dữ liệu cá nhân phải để ẩn danh (`data/contacts.json` giữ nguyên,
   KHÔNG copy vào đây).
5. Nộp qua commit/PR theo quy trình dự án; ghi rõ owner, phạm vi và bằng chứng.

## Checklist tối thiểu trước khi nộp

- [ ] Đúng thư mục vai trò + tên file theo quest
- [ ] Template header đủ (owner, quest, deadline, status)
- [ ] Không chứa PII thật / secret
- [ ] Số liệu có nguồn (link văn bản pháp luật, ngày kiểm tra)
- [ ] Claim nào chưa kiểm chứng → đánh dấu `[READY_FOR_HUMAN_REVIEW]`

## Nộp ở đâu (map theo QUESTS.md)

| Quest | File dự kiến nộp | Thư mục |
|---|---|---|
| C1 | `C1_law_verification_log.md` | `deliverables/C/` |
| C2 | `C2_problem_statement.md` | `deliverables/C/` |
| C3 | `C3_eval_split.json` + `C3_hard_negatives.jsonl` | `deliverables/C/` |
| C4 | `C4_claim_check_form.md` | `deliverables/C/` |
| C5 | `C5_consent_form_v1.md` (giao P) | `deliverables/C/` |
| C6 | `C6_eval_labels.csv` + `C6_self_score.md` | `deliverables/C/` |
| P1 | `P1_pilot_recruits.csv` | `deliverables/P/` |
| P2 | `P2_pilot_schedule.md` + `P2_shot_list.md` | `deliverables/P/` |
| P3 | `P3_partner_email_draft.md` + `P3_partner_list.md` | `deliverables/P/` |
| P4 | `P4_demo_script_final.md` | `deliverables/P/` |
| P5 | `P5_internal_pilot_log.md` | `deliverables/P/` |
