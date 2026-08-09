# QUEST — Rightly (Cập nhật: 08/08/2026, thứ 7)

> Đây là "bảng quest" chung cho cả team: ai làm gì, khi nào, giao gì cho ai.
> Chi tiết: `docs/team_status.md`, `docs/submission_checklist.md`.
> **Quy tắc**: OpenCode (công tác viên của T) KHÔNG làm thay C/P; C/P nhờ khi
> cần hỗ trợ kỹ thuật. Mọi mục liên quan hiệu lực luật/consent/claim/GTM phải
> có con người xác nhận (READY_FOR_HUMAN_REVIEW).
> **Nơi nộp sản phẩm**: `deliverables/C/` (vai trò C), `deliverables/P/` (vai
> trò P) — quy ước tên file + template xem `deliverables/README.md`.

## Mục tiêu chung

- Gate D: **≥45/50 rubric Intel Vietnam AI Impact Festival 2026 (VAIIF26)** —
  bảng Học sinh 13-17 — nộp **25/08/2026**.

## QUEST T (Technical — chủ: T, công tác viên: OpenCode)

| # | Quest | Deliverable | Deadline |
|---|---|---|---|
| T1 | Public deploy (Streamlit Cloud) không lộ secret | Public link dùng thử | 12/08 |
| T2 | OpenVINO/AI PC benchmark (nếu có máy) | `results/openvino_benchmark.md` | 20/08 |
| T3 | Config/timeout/retry production-grade cloud LLM | Code + test | 15/08 |
| T4 | Thu hẹp pattern RED false positive (F10) | Test phủ mới | 15/08 |
| T5 | Release + tag; tài liệu kỹ thuật khớp code | Release note | 24/08 |

*Đã xong (nền tảng)*: pipeline đầu-cuối, 94 tests, preflight 9/9, eval R1-R4,
CitationValidator chặn nguồn hết hiệu lực, privacy logging, demo transcript
deterministic (`docs/demo/README.md`), sửa nondeterminism retrieval (BM25/RRF
tie-break), scrub outbound PII cloud (`app/privacy/scrubber.py`), T3 cloud LLM
hardening (timeout/retry/classify_safe — `deliverables/T/README.md`).

*Đang chờ*: T1 cần API key (Groq/Gemini) + tài khoản Streamlit; T2 cần xác
nhận máy AI PC.

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

> **Quyết định hội đồng Round 8 (08/08, 5/5 phiếu — `debate_output/round8.json`
> + `round8_retry.json`):**
> 1. **Hoãn GỬI email đối tác: đồng thuận 5/5** tới khi có public link (12/08)
>    + pilot result (20/08); NHƯNG nháp + danh sách đối tác phải sẵn trước
>    20/08, gửi ngay theo đợt 20-21/08 để kịp evidence trước 25/08.
> 2. **P5 giữ (5/5)**, điều chỉnh: chạy như "sanity check" 60-90 phút, mở rộng
>    3-4 người (đa giọng Bắc-Nam nếu được), chấm nhanh 5 tiêu chí (ASR
>    accuracy, latency, intent match, fallback, UX).
> 3. Thứ tự ưu tiên cuối tuần (đa số 3/5): **P1 → P5 → P2 → P4 → P3**
>    (2/5 đề xuất P5 trước P1 để validate core loop — chấp nhận P1 dẫn trước
>    vì tuyển cần lead-time dài).
> 4. Rủi ro chính: đối tác trả lời chậm → evidence pack (screenshot + video
>    ngắn + transcript demo) chuẩn bị trước 23/08; GTM gửi theo đợt nếu cần.

> **Quyết định hội đồng Round 12 (08/08, họp kín 3 phiên — `debate_output/
> round12.json`, tổng hợp `results/round12_synthesis.md`):**
> 1. **Top 3 chung cuộc KHÔNG trong tầm tay nếu chấm hôm nay** (đồng thuận
>    15-35%); chỉ cạnh tranh (43+/50) nếu pilot thật xong trước hạn.
> 2. **Mũi neo hồ sơ (5/5): "AI vì cộng đồng & Tiếp cận" (Community AI /
>    Accessibility, SDG 10/11)** — narrative: "Hạ tầng tiếp cận dịch vụ công
>    bằng giọng nói cho nhóm yếu thế". KHÔNG neo vào Responsible AI (thiếu
>    audited evidence), Innovation, Startup. Dự phòng: "Dịch vụ công số" nếu
>    có thư UBND xã xác nhận pilot.
> 3. **3 hành động quyết định trước 25/08 (5/5):**
>    (a) Pilot thật 5-10 người (cao tuổi/nông thôn) + video ≤3' + ≥3-5
>    testimony có dấu thời gian + task success rate — xong trước 22/08;
>    (b) Đo WER/MOS trên ≥30-50 mẫu giọng thật (Bắc/Trung/Nam), công bố bảng
>    số liệu; WER >15% → UI nhập text làm primary demo mode;
>    (c) Đổi narrative hồ sơ sang "AI vì cộng đồng" + public link ổn định
>    12/08 + corpus luật thật trọng điểm (C1: 25-30+ văn bản có metadata
>    hiệu lực).
> 4. Điểm kỳ vọng: 30-38/50 hiện tại → **41-44/50 nếu pilot+testimony+video
>    xong**. Câu chốt (m365): "Chứng minh người dân thật sự dùng được và hưởng
>    lợi, đừng chỉ chứng minh AI thông minh."
> 5. P1 (tuyển pilot) trở thành đường găng #1 của P; C1 nâng thành corpus
>    trọng điểm 25-30+ văn bản (không cần kho luật đầy đủ).

> **Quyết định hội đồng Round 13 (08/08, họp kín 3 phiên — `debate_output/
> round13.json`, tổng hợp `results/round13_synthesis.md`):**
> 1. **Xác minh cuộc thi đúng: Intel(R) Vietnam AI Impact Festival 2026** (bảng
>    AI Changemakers; BTC NIC+SHTP+SHTP-IC+Intel VN; chủ đề
>    "Enriching Lives with AI Innovation"). **Hồ sơ = Google Form duy nhất: tên
>    ≤10 từ + mô tả ≤150 từ + video ≤2 phút + consent có chữ ký.** Rubric
>    chính thức đã đọc (M1 15đ, M2 20đ, M3 15đ) — khớp bảng nội bộ. Toàn bộ
>    sự kiện + link: `docs/competition_aiif26.md`.
> 2. **Đổi tư duy (5/5): "Đây là bài thi IMPACT + PRESENTATION, không phải bài
>    thi RAG"** — KHÔNG thêm feature AI lớn; điểm còn thiếu ở bằng chứng người
>    dùng thật, triển khai thật, video 2 phút. Cắt: uptime 99%, benchmark
>    30-50 giọng tách biệt, fine-tune, multi-language, mobile app, OpenVINO
>    thật (giữ narrative "ready" ≤0.3 ngày).
> 3. **TOP-12 hành động hợp nhất (5/5, ~13 người-ngày):** (1) Pilot 5-7 người
>    thật + consent + 3 testimony 15-20s + log WER/MOS từ cuộc gọi thật — P+C
>    ×13/08 (+5); (2) Video 2' "Bà Năm": problem→demo live→impact→ethics,
>    phụ đề, đúng ≤2:00 — C+T+P ×16/08 (+5-6); (3) Public link Streamlit free
>    + 3 key Groq xoay vòng + backup link + voice FAQ record 3 câu — T ×12/08
>    (+3); (4) 150 từ ĐÚNG 150 + SDG 3,10,11,16 + số liệu già hóa có nguồn —
>    C ×11/08 (+3); (5) Consent chuẩn form gắn kèm pilot — P+C ×12/08 (+1-2);
>    (6) GTM MỀM: LOI/email Hội NCT–giáo viên–UBND, KHÔNG treo điểm vào chữ
>    ký UBND — P+C ×18/08 (+1.5); (7) Corpus trọng điểm 15-30 văn bản thật +
>    metadata hiệu lực — T ×13/08 (+1.5); (8) Technical Rigor 1 trang (WER/MOS
>    từ log pilot) — T ×14/08 (+1.5); (9) Ethics/privacy disclosure + trang
>    ethical_ai 1 trang (9 nguyên tắc Intel) — C+T ×15/08 (+1); (10-12) FAQ
>    giám khảo + script demo 60s; sweep hồ sơ + submission proof ×22-24/08.
> 4. **Dự báo điểm: 43-46/50 (kỳ vọng ≈44-45, "khóa luận video" có thể 46-47);
>    thận trọng nhất 42.** Lỗ trống chấp nhận: OpenVINO thật (-1-2 M3),
>    offline/low-bandwidth (-1 M1), GTM chính quyền (-0.5 M2).
> 5. **Dòng đỏ:** không pilot người thật + không video 2' chất lượng + không
>    public link → mất trọn M1 evidence + M2 deployment, nguy cơ <40/50.
> 6. Freeze feature từ 13/08; "phi-code" chiếm ~70% điểm cộng → C/P là đường
>    găng, T chỉ phục vụ 5 vật chứng (link, corpus, log, voice FAQ, demo).

> **Quyết định hội đồng Round 14 (08/08, họp kín 3 phiên — `debate_output/
> round14.json` + vision `debate_output/vision_round14.json`, tổng hợp
> `results/round14_synthesis.md`):**
> 1. **BẢNG THI: HỌC SINH 13-17** (xác nhận 08/08). Top 3 và Top 1 đều xét THEO
>    TỪNG BẢNG: bảng Học sinh có 3 vé riêng (không cạnh tranh Sinh viên); Top 1
>    bảng → 1 đội/bảng đại diện VN đi Intel AI Global Impact Festival 2026.
>    Consent thí sinh <18: chữ ký phụ huynh/giám hộ.
> 2. **VOTE SDG PRIMARY (form bắt buộc chọn 1): SDG 16 — Peace, Justice &
>    Strong Institutions** (4/5; bỏ SDG 3 "health-washing" không có KPI y tế).
>    Dùng Target 16.3 (access to justice) + 16.10 (access to information) trong
>    150 từ + video. Ít đội 13-17 chọn → khác biệt.
> 3. **SONG NGỮ (đề xuất C) — CHỐT THU HẸP:** Form 150 từ = tiếng Anh 100%
>    (bản VN nội bộ); video 2' = giọng VN + phụ đề EN hard-burned; UI = 100%
>    tiếng Việt. Không dịch toàn bộ (lãng phí + rủi ro claim).
> 4. **XÁC SUẤT CHỐT:** Top 3 bảng Học sinh: 30-35% hôm nay → **45-55%** sau
>    Top-12. Top 1 bảng: 8-15% → **18-25%**. 3 yếu tố quyết định: pilot thật
>    + transcript, SDG 16 map chuẩn, video Bà Năm chất lượng phụ đề EN.
> 5. **Cắt OpenVINO/hardware** (scope creep ROI âm trong 17 ngày); giữ narrative
>    "CPU-only int8 chạy PC phổ thông" + limitation trung thực.
> 6. Tên cuộc thi chuẩn: Intel Vietnam AI Impact Festival 2026 (VAIIF26) — đã
>    rà soát/sửa toàn repo; transcript cũ giữ nguyên (nhật ký), chú thích trong
>    `docs/competition_aiif26.md`.

> **Quyết định hội đồng Round 15 (08/08, họp kín 3 phiên — `debate_output/
> round15.json`, tổng hợp `results/round15_synthesis.md`):**
> 1. **Mục tiêu >80% / >50% KHÔNG thực tế trong 17 ngày** (5/5). Trần trung thực:
>    Top 3 bảng Học sinh **65-75%**, Top 1 bảng **28-40%** sau TOP-6 booster.
>    Mục tiêu điều chỉnh chính thức: Top 3 = **70-75%**, Top 1 = **35-40%**.
> 2. **TOP-6 BOOSTER** (ROI tuyệt đối): (1) Pilot thật **20-30 NCT + KPI** (P lead,
>    18/08, +12-15% Top 3); (2) **Video pilot thật "Bà Năm"** không diễn + editor
>    (C+P, 16/08, +8-10%); (3) **SĐT thật + Zalo OA** (T+P, 13/08, +8-10%);
>    (4) **Intel AI PC/NUC loan + OpenVINO live** — email BTC `thi.theu.nguyen@intel.com`
>    NGAY 09/08 (T, trả lời 12/08, +6-8%); (5) **LOI/UBND xã + Hội NCT đóng dấu**
>    (P, 14/08, +5-7%); (6) **A/B demo 1022 vs Rightly** (T+C, 15/08, +5-8%).
>    LOẠI: Streamlit paid tier (ROI≈0), WER/MOS VIVOS lab (không differentiation —
>    chỉ làm phụ chứng Technical Rigor).
> 3. **Hành động 09/08:** SÁNG — P: email Intel xin mượn AI PC/NUC + nộp LOI
>    UBND xã/Hội NCT; CHIỀU — C: lên xã quay video pilot thật (không diễn);
>    T: chuẩn bị OpenVINO path (fallback CPU) + kích hoạt SIM/Zalo.
> 4. **Dòng đỏ:** dồn người-ngày vào booster không chạm rubric (paid tier, VIVOS,
>    pilot 3 miền rộng) → mất thời gian của pilot thật + video + LOI.

> **Quyết định hội đồng Round 16 (09/08, họp kín 3 phiên — `debate_output/
> round16.json`, tổng hợp `results/round16_synthesis.md`):**
> 1. Đề xuất đội trưởng "product-first (T hoàn thiện sản phẩm, P/C chờ)":
>    **BÁC BỎ bản thuần túy** (5/5). Phương án chốt: **SONG SONG CÓ KIỂM SOÁT** —
>    T = 100% sản phẩm (3 gap chặn mốc), P/C = 100% field work, không họp dài,
>    không kéo T vào giấy tờ. Critical path = waiting time bên ngoài (Intel 2-4
>    ngày, UBND 2-7 ngày, tuyển NCT 3-7 ngày), không phải bug code.
> 2. **3 gap CHẶN MỐC 13/08 (T làm hôm nay, xong trước 17h):** (1) Deploy public
>    + backup link (2-3h, Streamlit Cloud + HF Spaces/Render); (2) xoay key Groq
>    + fallback Gemini + rate-limit (1h); (3) Voice FAQ 5-10 kịch bản NCT (2h).
>    SĐT/Zalo + OpenVINO + UX nâng cao KHÔNG chặn pilot 13/08 — để sau (SĐT/Zalo
>    chỉ cần cho 18/08 scale 20-30).
> 3. **Checklist tối nay 09/08:** T — Deploy → Key → Voice FAQ (5-6h). P — email
>    Intel loan + LOI UBND/Hội NCT + xác nhận nguồn pilot 13/08 (2h). C — danh
>    sách NCT + consent + kịch bản phỏng vấn + bắt đầu quay cảnh thật (2h).
> 4. Dòng đỏ R16: "Trượt 13/08 = vỡ M1 = vỡ Top 3; đừng để đến 16/08 mới biết
>    thiếu cảnh thật."

## Quest phối hợp C-P

- C giao `consent_form_v1.md` (sáng T7) → P dùng khi tuyển người.
- C giao `problem_statement.md` → P dùng cho email đối tác + GTM.
- C claim check → P đối chiếu kết quả pilot thật.

## Feature backlog (demo — hạn trước FREEZE 13/08)

| # | Feature | Trạng thái | Ghi chú |
|---|---|---|---|
| F1 | Nối máy tới cơ quan (Command.CONNECT + State.CONNECTING) | ✅ 09/08 | CLI + UI; chỉ mở tel: khi `verified=true` (P phải xác minh số thật trước demo public) |
| F2 | Phiếu chuẩn bị hồ sơ (registration slip) | ✅ 09/08 | Markdown, trường cá nhân để trống, có privacy note; không gửi/lưu thông tin |
| F3 | Deploy public sẵn sàng (Streamlit Cloud + HF Spaces backup) | ✅ 09/08 (chờ bấm nút) | `scripts/predeploy_check.py` 0 FAIL; `docs/deploy_public.md`; secrets template đủ; T bấm Deploy 12/08 |
| F4 | Xoay key Groq (2-3 key) + fallback Gemini + rate-limit | ✅ 09/08 | `app/llm/fallback.py`; `app/ratelimit.py`; GROQ_API_KEY_2/3; test 10/10 |
| F5 | Voice FAQ 11 kịch bản (chống lỗi ASR môi trường xôn xao) | ✅ 09/08 | `app/faq.py` + `data/faq.json`; khớp không nhạy dấu; chạy SAU safety router; chặn ~60-70% câu demo → tiết kiệm API |
| F6 | Script log pilot WER/MOS/CSAT | ✅ 09/08 | `scripts/log_pilot_metrics.py` → `data/eval/pilot_metrics.jsonl` (ẩn danh) — P dùng 13/08 |
| F7 | OpenVINO benchmark sẵn sàng | ✅ 09/08 (HOÃN chạy) | `scripts/benchmark_openvino.py`; theo R17: chạy khi có máy mượn 12/08+, không claim trước khi đo |
| F8 | 2-step confirm nối máy + watermark phiếu (R17) | ✅ 09/08 | CLI hỏi lại có/không; UI popover consent trước tel:; phiếu có watermark đỏ "KHÔNG CÓ GIÁ TRỊ PHÁP LÝ" |
| F9 | SĐT thật + Zalo OA live | ⏳ 13/08 | P xác minh số → `verified=true`; Zalo OA đăng ký 10-11/08 (T+P) |
| F10 | Corpus mở rộng 15-30 văn bản | ⏳ HOÃN 10-11/08 (R17) | Hiện 11 nguồn thật; C giao link → T crawl/ingest + rebuild real_chunks |

## Điểm hẹn (hard milestones)

| Deadline | Mốc |
|---|---|
| 08-09/08 | C: storyboard video 2' + nháp 150 từ + SDG + số liệu nguồn · P: tuyển user pilot + consent T7 này · T: deploy public link + xoay 3 key Groq |
| 09/08 | **SÁNG: P email BTC xin mượn AI PC/NUC (thi.theu.nguyen@intel.com) + nộp LOI UBND xã/Hội NCT · CHIỀU: C quay video pilot thật lên xã; T chuẩn bị OpenVINO path + kích hoạt SIM/Zalo** |
| 10/08 | Gửi LOI/email Hội NCT (P); thư mẫu đối tác |
| 11/08 | LOCK 150 từ + SDG **16** (C) |
| 12/08 | Public link chạy + backup link + voice FAQ record (T); consent chuẩn form (P+C); **trả lời Intel loan PC** |
| 13/08 | Pilot 5-7 người XONG + 3 testimony + log ASR (P); **SĐT thật + Zalo OA live** (T+P); corpus trọng điểm 15-30 văn bản (T); FREEZE FEATURE |
| 14/08 | Technical Rigor 1 trang (WER/MOS từ log pilot) (T); **LOI/UBND + Hội NCT đóng dấu** (P) |
| 15/08 | Trang ethical_ai 1 trang (C+T); **A/B demo 1022 vs Rightly** (T+C) |
| 16/08 | **Video pilot thật "Bà Năm" RENDER XONG (không diễn, giọng VN + phụ đề EN)** (C+T+P) |
| 18/08 | **Pilot 20-30 NCT XONG + KPI** (task success/CSAT/latency) (P lead); GTM evidence mềm: LOI/xác nhận (P+C); FAQ giám khảo + script demo 60s (C) |
| 22-24/08 | Sweep hồ sơ cuối: form + video + link + minh chứng + submission proof |
| 25/08 | **NỘP** |

## Status nhanh

- T: pipeline xanh — việc ngay: public link Streamlit + xoay key, corpus 15-30
  văn bản, script log WER/MOS, voice FAQ record.
- C: việc ngay: storyboard video 2' + 150 từ + SDG map + số liệu (08-11/08).
- P: việc ngay: tuyển 5-7 user pilot T7 hôm nay, consent v1 có sẵn.
