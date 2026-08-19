# Project Review — Rightly (Hội đồng Round 10)

> **Tài liệu lịch sử.** Đây là ý kiến review ở Round 10, không phải trạng thái chất lượng hiện tại.

> **NHÁP — chờ T đọc, KHÔNG push.** Nguồn: `debate_output/round10.json`
> (5 mô hình + OpenCode, phản biện chéo + rà soát toàn dự án, 08/08/2026).
> Đối chiếu dữ liệu thật: 74 tests, preflight 9/9, eval R1–R4, demo
> deterministic 5 kịch bản, GitHub private `neornotl/rightly-v4`.

## 1. Điểm mạnh (đồng thuận, 5 mục)

1. **Kiến trúc safety-first có đầy đủ lớp**: ASR → normalize → retrieval
   hybrid → SafetyRouter (RED/ORANGE/YELLOW) → LLM → CitationValidator → TTS;
   mock-mode chạy không cần key, demo deterministic.
2. **Chất lượng kỹ thuật có bằng chứng**: 74 tests, ruff sạch, preflight 9/9,
   eval R1–R4 có baseline + dataset card.
3. **Guard chống hallucination hoạt động thật**: validator chặn nguồn hết
   hiệu lực (ND 62/2021 → REFUSE) + từ chối ngoài phạm vi (INSUFFICIENT).
4. **Retrieval hybrid (BM25+dense+RRF)** + đã sửa nondeterminism tie-break.
5. **Repo có cấu trúc cộng đồng** (README/COC/CONTRIBUTING/LICENSE/SECURITY,
   QUESTS, MASTER) — hồ sơ nộp không bỡ ngỡ.

## 2. Red flag nguy hiểm nhất (ưu tiên xử lý trước 25/08)

| # | Red flag | Owner | Vì sao gấp | Hành động |
|---|---|---|---|---|
| 1 | **C/P chưa deliver + chưa tuyển** (4/5 thành viên nhắc) | C, P | Rủi ro deadline #1: không pilot/video = mất điểm M1, M2 | standup 15'/ngày; MVP deliverable: C 5 kịch bản + problem statement, P ≥3 user + consent |
| 2 | **Mock-mode drift — chưa có smoke test LLM thật** | T | Demo mock che latency/WER/hallucination; chấm VAIIF26 có thể test live | real-mode E2E ≥10 queries trước 20/08 (Groq/Gemini có key) |
| 3 | **Chưa có AI PC/OpenVINO** (3/5 nhắc) | T + đội | Mất 1–2đ M3 nếu không chứng minh local path | giữ desktop benchmark + ghi limitations; máy có thì đo OpenVINO |
| 4 | **Public link (12/08) — CLOUD đã chốt (08/08)** | T | Mất +2đ M2; link chậm kéo lùi P (tuyển user ngoài) | **ĐÃ CHỐT: cloud làm chính (vốn + giới hạn phần cứng), local = on-prem chuyên nghiệp cho tổ chức. Scrub outbound xong (`app/privacy/scrubber.py`, `PII_SCRUB_OUTBOUND=true`, 83 tests xanh). Còn: bảo vệ key Streamlit + rate limit khi deploy** |
| 5 | **Retrieval tie-break mới cần kiểm thử sâu hơn** (biên) | T | Mới sửa, chưa phủ biên | thêm test edge: điểm bằng, hash seed khác, nhiều lần chạy |

## 3. Rủi ro bị bỏ sót trước đây (đã bổ sung)

- Mock-mode drift / false confidence (xem mục 2.2)
- Explainability của router (người dùng hiểu vì sao bị chuyển hướng)
- Router fail-open (RED→YELLOW khi lỗi) — cần test fail-closed
- PII lặp lại từ RAG context qua Mock LLM
- npz cache: **đã verify an toàn** (chỉ cache corpus công khai)

## 4. Chấm độ sẵn sàng (ước lượng hội đồng, KHÔNG phải rubric chính thức)

- Kỹ thuật (M3): **mạnh** — 14-15/15 nếu có OpenVINO + real-mode smoke
- Nội dung/chứng cứ (M1/M2): **yếu nhất** — mọi điểm phụ thuộc C/P chưa động
- Tổng hợp: nếu C/P làm xong quest tuần này (C1-C6, P1-P5) + T real-smoke +
  public link → mục tiêu ≥45/50 khả thi; nếu không, rớt về ~36-40.

## 5. 3 việc PHẢI làm ngay tuần này (đồng thuận)

1. **T**: real-mode E2E smoke ≥10 queries (mock → Groq/Gemini), ghi latency/
   WER thật vào `results/` — hết trước 12/08. [CLOUD đã chốt — làm bằng cloud keys]
2. **C + P**: standup 15' mỗi sáng; C giao tối thiểu 5 kịch bản eval + consent
   + problem statement; P giao ≥3 user pilot đã consent.
3. **T**: ~~quyết định cloud mode~~ **ĐÃ CHỐT cloud (08/08)** — việc còn lại:
   bảo vệ key Streamlit + rate limit + retention log 30 ngày trước deploy 12/08.

## 6. Lưu ý

Báo cáo này là NHÁP hội đồng AI pool — con người (T) xác nhận trước khi biến
thành hành động. Số liệu "điểm ước lượng" chỉ để sắp thứ tự ưu tiên, không
thay thế rubric chính thức.
