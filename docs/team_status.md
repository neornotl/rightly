# Daily Team Status

> **Nhật ký lịch sử.** Đây không phải bảng điều hành công việc hiện hành; các trạng thái DONE/TODO bên dưới không được tự động suy ra là còn đúng.

Cập nhật mỗi phiên làm việc. Mọi trạng thái dựa trên file/test/log/consent
status/evidence thực tế — không suy đoán. Owner: [T] Technical, [C] Content/
Compliance/Evaluation, [P] Pilot/Presentation/Partnership.

Cập nhật gần nhất: 09/08/2026 (tối — sau Round 17) — Mục tiêu Gate D (25/08/2026): **≥45/50 rubric
VAIIF26**.

## T - Technical

- Done:
  - Pipeline ASR → retrieval → LLM → validation → routing → TTS chạy đầu-cuối
    (mock + local). Hybrid RAG (BM25 + dense + RRF + answerability gate).
  - CitationValidator (registry `data/law_status.json`, 11 văn bản luật/NĐ
    thật); safety router RED/ORANGE/YELLOW + CRIMINAL_MATTER + citation guard
    (Council T2/T3); privacy logging (scrub, xóa raw audio).
  - **125→142 tests pass, ruff clean, preflight 9/9** (`results/evaluation_report.md`).
  - **09/08 (ngày FULL của T — đã xong)**: feature demo "Nối máy + Phiếu hồ sơ"
    (Command.CONNECT/State.CONNECTING, `app/contacts.py` tel: chỉ khi verified,
    `app/forms.py` phiếu không thu thập dữ liệu cá nhân, UI+CLI, 14 test mới);
    **F4** xoay key Groq (GROQ_API_KEY_2/3) + fallback Gemini
    (`app/llm/fallback.py`) + rate limit theo client (`app/ratelimit.py`);
    **F5** Voice FAQ 11 kịch bản (`app/faq.py`, `data/faq.json`, khớp không nhạy
    dấu, chạy sau safety router — tiết kiệm API khi demo); script log pilot
    WER/MOS/CSAT (`scripts/log_pilot_metrics.py`); OpenVINO benchmark sẵn sàng
    (`scripts/benchmark_openvino.py`, máy này CPU-only không NPU); deploy prep
    (`scripts/predeploy_check.py` 0 FAIL, `.streamlit/secrets.toml.example` đủ
    key mới, `docs/deploy_public.md`); **F8 (R17)**: xác nhận 2 bước nối máy
    (CLI hỏi lại có/không + UI popover consent trước tel:, chống false-positive
    ASR) + watermark đỏ phiếu (header+footer "KHÔNG CÓ GIÁ TRỊ PHÁP LÝ");
    Round 17 synthesis: `results/round17_synthesis.md` (2 YES có điều kiện +
    1 PARTIAL + 2 NO → duyệt 4 core, OpenVINO + corpus HOÃN 10-11/08).
- In progress:
  - [T] Bấm Deploy public (Streamlit Cloud + HF Spaces backup) — cần tài khoản;
    mọi thứ khác đã sẵn sàng. Mốc 12/08.
  - [T] Zalo OA đăng ký (10-11/08) — chờ P/C bổ sung SĐT thật.
- Blocked: (none)
- Needs review:
  - [T+C] Thu hẹp pattern RED false positive (F10) — chưa làm.
- Next action:
  - [T] 12/08: deploy public link + trả lời email Intel loan; chạy predeploy_check
    trước khi bấm nút. Khi P giao SĐT xác minh → đổi `verified=true` trong
    `data/contacts.json`. Khi C giao corpus 15-30 văn bản → chạy crawl/ingest +
    rebuild real_chunks.

## C - Content, Compliance & Evaluation

- Done:
  - `docs/MASTER.md` (toàn bộ hệ thống + từ điển thuật ngữ + audit + Round 5);
    `docs/data_card.md`, `docs/evaluation_dataset_card.md`,
    `docs/responsible_ai.md`, `docs/privacy_deletion_policy.md`.
  - `data/source_registry.csv`, `data/law_status.json` (11 nguồn),
    `data/source_metadata_real.csv`; `docs/rubric_evidence_matrix.md` (bản
    nháp đối chiếu rubric).
  - Eval R1–R4 protocol + fixture; kết quả synthetic demo (KHÔNG gọi là pilot).
- In progress: (không có — OpenCode không can thiệp; C tự chạy, khi cần hỗ
  trợ kỹ thuật thì nhờ [T])
- Blocked: (none)
- Needs review: (none)
- Next action: (theo kế hoạch cuối tuần do hội đồng đề xuất — xem "Kế hoạch
  cuối tuần Sat/Sun" bên dưới)

## P - Pilot, Presentation & Partnership

- Done:
  - `docs/pilot_protocol.md` (3 task chuẩn + 1 tự do, consent, ẩn danh);
    `docs/demo_script.md` (kịch bản demo 4 phần).
- In progress: (none)
- Blocked:
  - Chưa có người tham gia pilot / consent / thiết bị / video — toàn bộ cần
    con người (P).
- Needs review: (none)
- Next action:
  - [P] Chốt danh sách 8–10 người + lịch; chuẩn bị consent (nháp từ C);
    danh sách cảnh cần quay cho video 2 phút.

## Kế hoạch cuối tuần Sat 08/08 + Sun 09/08 (hội đồng Round 7, 5/5)

> Nguồn: `debate_output/round7.json` (laguna-s-2.1, nemotron-nano-omni,
> minimax-m3, m365-copilot, nemotron-3-ultra). Điểm rubric là ước lượng hội
> đồng, không phải điểm chính thức. OpenCode (T) KHÔNG làm thay C/P — chỉ hỗ
> trợ kỹ thuật khi được nhờ.

### C (con người) — tổng ~14-16h

| # | Đầu việc | Deliverable | Giờ | Rubric ước lượng |
|---|---|---|---|---|
| 1 | Xác minh 11 văn bản luật + hotline (gọi xác minh, ghi log) | `law_verification_log.md` (ngày gọi, người xác nhận, số điều) | 4-5h | +3-5 (Trustworthy, Citation) |
| 2 | Problem statement ≤150 từ + tên dự án + SDG map | `problem_statement.md` | 2-3h | +2-4 (Problem Framing, SDG) |
| 3 | Tách dev/final eval sets (chống leakage) + hard negatives ≥30 | `eval_split.json`, `hard_negatives.jsonl` | 2-3h | +1-3 (Eval Rigor) |
| 4 | Claim check README/MASTER/form | `claim_check_form.md` | 2-3h | +2-3 (Credibility, RA) |
| 5 | Consent templates (pilot + thu âm + video) | `consent_form_v1.md` → bàn giao P **sáng thứ 7** | 2h | +1-2 (Ethics, Privacy) |
| 6 | (Nếu còn giờ) Nhãn eval R1-R4 + self-score rubric | `eval_labels.csv`, `self_score.md` | 2h | +2 |

### P — tổng ~12-16h (ưu tiên tuyển SỚM — làm chậm sẽ kéo lùi pilot + video)

| # | Đầu việc | Deliverable | Giờ | Ghi chú |
|---|---|---|---|---|
| 1 | Tuyển 8-10 người pilot + thu consent | `pilot_recruits.csv` | 4-5 | Gating tuần sau — làm trước nhất |
| 2 | Lịch pilot tuần sau + shot-list video | `pilot_schedule.md`, `shot_list.md` | 3h | Video 2-3' |
| 3 | NHÁP email đối tác + danh sách đối tác tiềm năng (KHÔNG gửi) | `partner_email_draft.md` | 2h | Gửi chính thức HOÃN tới khi có public link + pilot (theo ý T 08/08) |
| 4 | Demo script chốt (lời + slide cue) | `demo_script_final.md` | 2h | |
| 5 | Thử pilot nội bộ 2 người (bắt lỗi trước người thật) | Log thử nội bộ | 2-3h | Bổ sung theo ý T |

### C-P phối hợp
- C giao `consent_form_v1.md` (sáng T7) → P dùng ngay khi tuyển.
- C giao `problem_statement.md` → P đưa vào email đối tác + GTM.
- C claim check → P đối chiếu khi chạy pilot thật.

### T hỗ trợ (chỉ khi được nhờ)
- Public link: sẵn sàng deploy khi C/P cần link cho pilot/email đối tác.
- Hỗ trợ kỹ thuật split eval, hard negatives, hotline status khi C cần.
- Chạy test/preflight bất kỳ lúc nào.

## Cross-role blockers

- Item: Public link có người dùng thật (M2 +2đ) — Owner: [T+P] — Required
  handoff: T deploy bản an toàn → P tuyển 1–2 người ngoài đội test — Deadline:
  18/08.
- Item: Pilot 8–10 người (M1 + evidence) — Owner: [P+C] — Required handoff:
  C cung cấp tác vụ chuẩn + consent → P tổ chức — Deadline: 20/08.
- Item: Video 2 phút với consent — Owner: [P] — Required handoff: P quay,
  C duyệt claim trong video — Deadline: 22/08.
- Item: Máy Intel AI PC / OpenVINO — Owner: [T] — Required handoff: phần cứng
  từ đội — Deadline: 20/08 (nếu có máy; nếu không, ghi rõ giới hạn).
- Item: Hotline/đầu mối chuyển tuyến xác minh (`data/contacts.json`) — Owner:
  [C] — Required handoff: C xác minh → T đưa vào Policy — Deadline: 20/08.

## Hội đồng AI pool

- **6 thành viên**: 5 mô hình API (laguna-s-2.1:free, nemotron-3-ultra,
  nemotron-nano-omni, minimax-m3, m365-copilot) + **OpenCode — thành viên
  thường trực**, điều phối phiên họp và **có quyền biểu quyết** như mọi
  thành viên khác.
- Round 7 (08/08): kế hoạch cuối tuần cho C/P (`debate_output/round7.json`).
- Round 8 (08/08): duyệt hoãn gửi đối tác 5/5 có điều kiện (nháp sẵn fire
  20-21/08, danh sách đối tác + warm-up, evidence pack trước 23/08); P5 giữ
  (sanity-check 60-90', mở 3-5 người, rubric 5 tiêu chí); thứ tự
  P1→P5→P2→P4→P3 (3/5 đa số) — `debate_output/round8.json` +
  `round8_retry.json` (m365 đã fix, họp đủ 5/5).

## Gate status

- Gate A (Core Ready): **READY_FOR_HUMAN_REVIEW** — pipeline, 73 tests,
  preflight 9/9, safety, privacy logging. Cần [C] review + [T] xác nhận.
- Gate B (Evidence Ready): **IN_PROGRESS** — thiếu source verification
  report, SDG, problem statement, claim check.
- Gate C (Pilot Ready): **TODO** — chưa có người tham gia, consent, thiết bị.
- Gate D (Submission Ready): **TODO** — phụ thuộc A/B/C + video, form, GTM.
