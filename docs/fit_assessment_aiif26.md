# Đánh giá mức độ tương thích — Tiếng Làng v4.0 × Intel Vietnam AI Impact Festival 2026

Ngày: 08/08/2026 · Tác giả: OpenCode (tổng hợp dữ liệu verified + rubric chính thức +
kết quả Round 13) · Đọc cùng: docs/competition_aiif26.md, docs/rubric_evidence_matrix.md

## 1. Kết luận tổng thể

**Độ tương thích: 8/10 — dự án SẠCH ăn cuộc thi này, nhưng "đồng tác giả" bên ngoài
hồ sơ (video/150 từ/consent) chưa có gì, và có 5 điểm lệch nhỏ phải xử lý trong hồ sơ.**

| Khía cạnh | Mức khớp | Nhận xét |
|---|---|---|
| Chủ đề "Enriching Lives with AI Innovation" | RẤT CAO | AI vì cộng đồng + người cao tuổi + tiếng nói = đúng tâm chủ đề |
| Hạng mục Học sinh 13–17, nhóm ≤3 | ĐẠT (xác nhận 08/08 — cần chốt tuổi/trường học từng thành viên) | Team T/C/P = 3 người; cả 3 trong độ tuổi và đang học THCS/THPT/CĐ nghề |
| Định dạng hồ sơ (≤10 từ / ≤150 từ / video ≤2' / consent) | THẤP (0/4 có sẵn) | Đây là toàn bộ "mặt trình diễn" — đang là lỗ hổng lớn nhất |
| Rubric M1 Impact (15đ) | TRUNG BÌNH (dựa vào pilot/video) | Sản phẩm đúng trọng tâm; bằng chứng người dùng chưa có |
| Rubric M2 Innovation (20đ) | CAO (prototype + ethics đã có) | Thiếu public deployment + GTM |
| Rubric M3 Technical (15đ) | CAO NHẤT | Pipeline hoàn chỉnh, tests, RAG+Agent+multimodal |
| Ethics check của Intel (điều kiện giải quốc tế) | RẤT CAO | Threat model, privacy, safety routing, citation — hiếm đội SV làm tới |

## 2. Đối chiếu từng yêu cầu cuộc thi

### 2.1 Điều kiện dự thi — **BẢNG HỌC SINH (13-17 TUỔI)** [xác nhận 08/08]
- Đội thi bảng **Học sinh**: 13–17 tuổi, đang học THCS/THPT/cơ sở GD nghề
  nghiệp — **phải xác nhận cả 3 thành viên đủ và đúng bậc học** (T/C/P).
- Nhóm ≤3: T + C + P = 3 → đạt (OpenCode không phải thành viên).
- Consent "có chữ ký người có thẩm quyền": thí sinh <18 tuổi → chữ ký
  **phụ huynh/người giám hộ** (hoặc đại diện nhà trường nếu form yêu cầu) —
  C mở Google Form kiểm tra đúng vai ký + bản mẫu.
- Tuổi tính tại thời điểm nộp/hoặc dự thi — C xác nhận trong form.
- Một người chỉ dự 1 bảng → không trùng lặp tên giữa 2 bảng.
- **Rủi ro loại hồ sơ** nếu sai consent/độ tuổi → xử lý ngày 09-10/08: chốt chữ
  ký phụ huynh ngay khi ký consent pilot.

### 2.2 Chủ đề và định vị
- Chủ đề 2026 "Làm phong phú cuộc sống thông qua đổi mới sáng tạo với AI" — dự án
  voice-first cho NCT/nông thôn khớp trực tiếp; hồ sơ nên mở bằng câu "AI xóa rào
  cản kỹ thuật số cho người cao tuổi Việt Nam" (đúng chữ "enriching lives").
- Các đội thắng toàn cầu gần đây của VN đều thuộc nhóm "AI vì cộng đồng/accessibility"
  (Your Voice - ĐH Lạc Hồng 2025: dịch ngôn ngữ ký hiệu) → hướng đi được BTC ưa
  chuộng, đồng thời cảnh báo cạnh tranh trực tiếp → phải có "bằng chứng thật"
  (pilot/video) mới thắng được nhóm này.

### 2.3 Định dạng hồ sơ (giới hạn cứng) — trạng thái hôm nay

| Yêu cầu | Có sẵn? | Cần làm |
|---|---|---|
| Tên ≤10 từ | CHƯA | Ví dụ: "Rightly — AI voice agent cho pháp luật Việt Nam" (đếm từ kỹ) |
| Mô tả ≤150 từ | CHƯA (có draft trong các doc) | Lock 11/08, cấu trúc problem→AI→impact→SDG→ethics |
| Video/vlog ≤2 phút | CHƯA | Render 16/08 theo storyboard "Bà Năm" |
| Consent mẫu + chữ ký phụ huynh/giám hộ | CHƯA | Tải bản mẫu từ form; ký pilot 12/08 |
| Link dự án public (tự nguyện, đính kèm video/form) | Code sẵn, chưa deploy | Streamlit Cloud + 3 key Groq 12/08 |

## 3. Đối chiếu rubric chính thức từng điểm (chấm kỳ vọng)

Ước điểm "hôm nay" dựa trên bằng chứng hiện có; cột "sau Top-12" theo lộ trình Round 13.

### M1 — Enriching Lives: Impact & Inclusion (15đ)

| Tham số | Tối đa | Nay | Sau | Bằng chứng/việc cần |
|---|---|---|---|---|
| Problem statement rõ | 2 | 1 | 2 | Viết lại khít trong 150 từ |
| Evidence vấn đề (citations) | 1 | 1 | 1 | Số liệu già hóa dân số (GSO) có nguồn |
| Target audience rõ | 2 | 1 | 2 | Định nghĩa NCT/nông thôn/ít kỹ năng số |
| UX equivalent cho mọi người | 1 | 1 | 1 | Voice-first + text UI |
| Gỡ rào cản người khuyết tật | 1 | 1 | 1 | Voice-first; kể rõ trong video |
| Khả thi tài chính | 1 | 0 | 1 | "Chi phí 0đ/người dùng" + LOI |
| Offline/low-bandwidth | 1 | 0 | 0.5 | Không có offline; nêu giới hạn trung thực |
| Đa ngôn ngữ/đa phương thức | 1 | 0 | 0 | Tiếng Việt + voice/text (giải thích, không claim) |
| Tác động xã hội rõ | 1 | 0.5 | 1 | Con số + testimony |
| AI vượt software truyền thống | 1 | 1 | 1 | Voice RAG với luật — không làm nổi bằng menu |
| SDG map | 1 | 0 | 1 | SDG 3, 10, 11, 16 |
| Môi trường | 1 | 1 | 1 | PhoWhisper int8 local, cloud-first không đồ audio |
| Đường bền vững | 1 | 0 | 1 | Zalo OA + LOI + mã nguồn mở |
| **M1 cộng dồn** | **15** | **7.5** | **13.5** | |

### M2 — AI Innovation: Application & Implementation (20đ)

| Tham số | Tối đa | Nay | Sau | Bằng chứng/việc cần |
|---|---|---|---|---|
| Không force-fit AI | 1 | 1 | 1 | RAG+ASR+TTS là lõi |
| AI là công nghệ chính | 2 | 2 | 2 | Toàn pipeline AI |
| Ý tưởng mới/original | 3 | 2 | 2 | Voice-first luật VN mới cho NCT (adaptation+) |
| Thể hiện tri thức AI | 2 | 2 | 2 | Repo/README/docs |
| Dữ liệu thu thập & phân tích | 1 | 1 | 1 | 11 nguồn luật thật + corpus 15-30 |
| Giải trình chọn dữ liệu | 1 | 1 | 1 | data_card + law_status metadata |
| Đạo đức AI | 1 | 1 | 1 | SafetyRouter, 113/115, refusal |
| Quyền riêng tư | 1 | 1 | 1 | PII scrubber, xóa audio, retention 30 ngày |
| Giảm bias | 1 | 0.5 | 1 | Đa giọng vùng (VIVOS) + kế hoạch |
| Môi trường | 1 | 0.5 | 1 | Tài liệu hóa mức năng lượng |
| Prototype chạy | 1 | 1 | 1 | Demo deterministic + smoke 12/12 |
| Triển khai: public link | 2 | 0 | 2 | URL public hoạt động + smoke log + hướng dẫn tự thử |
| GTM/deployment | 1 | 0 | 0 | Không theo đuổi LOI/đối tác; không claim điểm khi chưa có traction |
| **M2 cộng dồn** | **20** | **13** | **18** | |

### M3 — Technical Knowledge and Skills (15đ)

| Tham số | Tối đa | Nay | Sau | Bằng chứng/việc cần |
|---|---|---|---|---|
| Tech stack rõ | 2 | 2 | 2 | README/architecture |
| Hardware | 3 | 1 | 1.5 | Desktop; narrative "AI PC/OpenVINO ready" |
| Software (multi + API) | 3 | 3 | 3 | Python + API Groq/Gemini/OpenVINO path |
| UI custom | 3 | 3 | 3 | Streamlit custom cho NCT (chữ to, nút lớn) |
| Emerged AI (GenAI/Agents/RAG/multimodal) | 4 | 4 | 4 | Voice RAG + agent routing + multi-modal |
| **M3 cộng dồn** | **15** | **13** | **13.5** | |

**Tổng kỳ vọng theo hướng self-serve: hiện khoảng 31-36/50 → sau khi hoàn thiện public link, evidence kỹ thuật, consent/pilot và video khoảng 40-44/50. Mốc 45 chỉ là stretch, không nên lập kế hoạch dựa trên GTM/đối tác.**

## 4. Điểm lệch cần xử lý để "khớp" cuộc thi (compatibility gaps)

1. **Mặt trình diễn = 0**: bài dự thi là video+150 từ, không phải repo → chuyển ngay
   trọng tâm công sức (đã nằm trong Top-12 #1-#2).
2. **Offline/low-bandwidth (M1 1đ)**: không có thật → KHÔNG claim; thay bằng câu
   chuyện trung thực "voice-first giảm tải nhập liệu, hoạt động tốt trên 4G phổ thông".
3. **Đa ngôn ngữ (M1 1đ)**: không hỗ trợ → tránh claim; giải thích "tiếng Việt có
   giọng địa phương" thay vì đa ngôn ngữ.
4. **Hardware (M3 1-1.5đ)**: không có AI PC → giữ mức desktop + OpenVINO-ready
   narrative, chuẩn bị câu trả lời khi BTC hỏi (slide backup).
5. **Gia tốc có sẵn chưa dùng**: `data/private_cache/vivos` có sẵn **760 file wav
   tiếng Việt thật (19 diễn giả, 82MB)** → T có thể chạy WER/MOS trên speech THẬT ngay hôm
   nay cho "Technical Rigor" mà KHÔNG cần thu âm mới — tăng M2 "data analysis" +
   M3 depth; dùng log pilot làm nguồn chính, VIVOS làm phụ trợ.
6. **Consent/độ tuổi là rủi ro loại hồ sơ** — ưu tiên xử lý 09-10/08 (C+P).
7. **M2 GTM/deployment (1đ)**: hướng self-serve không có bằng chứng adoption/đối tác thì để 0,
   không nói marketing như thể đó là traction. Tập trung public link, hướng dẫn tự thử
   và số liệu kỹ thuật có thể tái lập.

## 5. Cảnh báo cạnh tranh

- VN đã có đội thắng Global 2025 nhóm accessibility (Your Voice). BTC thích "AI vì
  cộng đồng" → sân chơi đông; điểm khác biệt của chúng ta: **độ sâu trách nhiệm
  pháp lý + evidence kỹ thuật** (validator hiệu lực văn bản, refusal an toàn) — kể
  câu chuyện này trong video.
- Dự án phải đứng được trước câu hỏi "sao không dùng hotline 1022/chatbot sẵn có?"
  → chuẩn bị 1 slide/30 giây trong video: 1022 có giờ, giọng hướng dẫn chưa thân
  thiện, không trích luật theo câu hỏi cụ thể; **Rightly** trả lời trực tiếp + dẫn
  luật + chuyển khẩn cấp.

## 7. Cơ hội Top 3 / Top 1 theo bảng — phân tích sâu (dữ liệu năm ngoái chính thức)

> Nguồn: PDF "Vietnam AI Impact Festival 2025" (link chính thức SHTP-IC) +
> techsignin.com (Global 2025). Đây là phân tích cơ hội, KHÔNG phải cam kết.

### 7.1 Các đội thắng quốc gia 2024–2025 (chính thức)

| Năm | Giải | Đội | Bảng | Đặc điểm cốt lõi |
|---|---|---|---|---|
| 2025 | Global Award | Your Voice (ĐH Lạc Hồng) | Sinh viên | Dịch ngôn ngữ ký hiệu real-time (CV + avatar); 2,5 triệu người khiếm thính; SDG 4 |
| 2025 | Country Award | Hap (Hà Ngô + Phúc Phan — THPT Chuyên Lam Sơn + Chuyên Lê Hồng Phong) | **Học sinh 13-17** | Kính thông minh + thiết bị rung đeo cổ, YOLOv8 + **OpenVINO**, màn hình-free, low-cost, offline; SDG 3; sau đó thắng Regional Award Global 2025 |
| 2024 | Country Award | AERO ResQ (PTIT) | Sinh viên | Drone + phát hiện Wi-Fi probe để cứu nạn thảm họa; SDG 11 |
| 2024 | Country Award | S-REC | Sinh viên | Tuyển dụng tự động hóa bằng AI (dùng "Intel's AI technologies"); SDG 8 |

### 7.2 Mẫu hình của đội thắng (pattern) — đối chiếu với chúng ta

1. **Chủ đề accessibility/cộng đồng chiếm giải cao nhất 2 năm liên tiếp**
    (Your Voice + Hap). **Rightly** — xóa rào cản kỹ thuật số cho người cao tuổi
    nông thôn — cùng trục này. → Thuận lợi lớn: đúng gu hội đồng.
2. **Đội thắng bảng 13-17 (Hap) dùng HARDWARE + OpenVINO** — Intel "ưu ái" dự án
   chạy trên toolkit của họ. Chúng ta KHÔNG có phần cứng và KHÔNG nên claim
   OpenVINO giả. → Bất lợi ~2-3đ M3 (hardware 0-3), nhưng rubric M3 hardware chỉ
   chiếm 3/50đ — bù được bằng M1/M2.
3. **Mọi đội thắng đều nêu SỐ LIỆU tác động lớn** (2,5 triệu người khiếm thính;
   tổ chức cứu hộ). Chúng ta cần số liệu tương đương: ~7 triệu người cao tuổi VN
   (ước 2024), ~60% nông thôn, hơn 60% người ≥60 tuổi không thành thạo kỹ thuật
   số (nguồn GSO/WHO — C phải trích nguồn chính xác).
4. **SDG alignment được BTC in vào hồ sơ đội thắng** — chúng ta đã chọn SDG 3, 10,
   11, 16; chọn 1 SDG chính (3: Good Health & Well-Being) nêu rõ trong video.
5. **Đội thắng 13-17 thường có "wow hardware"** → để cân bằng, video của chúng ta
   phải có: (a) cảnh người thật (NCT) dùng thành công, (b) chứng minh kỹ thuật
   nhà nghề (demo tự động + WER + latency), (c) câu chuyện "vì sao chatbot thường
   không đủ" (voice-first + 1022 không trả lời theo câu hỏi + dẫn luật).
6. **Thành viên đội thắng 13-17 đều từ trường chuyên/top** — không phải yếu tố
   chấm điểm nhưng ảnh hưởng chất lượng bài. Đội mình thắng bằng độ sâu engineering
   + evidence thật (hiếm ở bảng này).

### 7.3 Ước lượng cơ hội (thành thật, có khoảng)

**Cách xét giải (xác nhận từ trang chính thức SHTP-IC + YBOX):** Top 3 và Top 1
đều xét THEO TỪNG BẢNG (mỗi hạng mục độ tuổi), không xét chung cả 2 bảng:
- Top 3: 3 giải/bảng → bảng Học sinh 13-17 có 3 vé riêng (tổng 6 đội thắng quốc gia).
- Top 1: 1 đội/bảng → 2 đội VN đi Intel AI Global Impact Festival (khớp 2025:
  Your Voice bảng SV + Hap bảng HS).
- Mục tiêu Gate D: **Top 3 bảng Học sinh**; Top 1 bảng = vé Global (ưu tiên sau).

Giả định: số bài nộp bảng 13-17 không công bố, ước 50-150 bài toàn quốc.

| Mục tiêu | Xác suất hôm nay | Xác suất nếu thực thi TOP-6 booster R15 đúng hạn | Điều kiện quyết định |
|---|---|---|---|
| **Top 3 bảng Học sinh 13–17 (3 vé riêng của bảng)** | 30-35% (R14 chốt) | **65-75%** (R15 chốt; mục tiêu điều chỉnh: 70-75% — KHÔNG >80%) | Pilot 20-30 NCT thật + KPI + video "Bà Năm" không diễn + SĐT/Zalo live + LOI UBND/Hội NCT đóng dấu + A/B 1022 → giữ 45-48/50; SDG 16 map chuẩn; claim sạch |
| **Top 1 bảng (đi tiếp Global)** | 8-15% | **28-40%** (R15 chốt; mục tiêu điều chỉnh: 35-40% — KHÔNG >50%) | Đòi hỏi vượt nhóm hardware (Hap-style): Intel AI PC/NUC loan + OpenVINO live demo + pilot 20-30 NCT đa miền + transcript + video "wow" không diễn |

Logics ủng hộ (so với Hap 2025):
- Hap nhắm 2 triệu người khiếm thị 18-30 tuổi; chúng ta nhắm ~7 triệu NCT (bùng nổ
  già hóa 2025-2035) → quy mô impact lớn hơn nếu số liệu đúng.
- Hap KHÔNG có pilot người dùng thật trong video công bố; chúng ta CÓ kế hoạch
  pilot + log ẩn danh → điểm "Evidence" M1/M2 có thể vượt.
- Chúng ta có Responsible AI đầy đủ (privacy, refusal, citation) — hiếm thấy ở bảng
  học sinh; đúng 9 nguyên tắc Ethical AI Guidelines của Intel.
Logics bất lợi:
- Không hardware/OpenVINO → mất 1.5-2đ M3 và "wow factor" so với Hap.
- Đối thủ 13-17 có thể là đội thầy kèm/trường chuyên với video dựng chuyên nghiệp.
- Impact là chủ quan — biên độ điểm ±4-5 quanh dự báo 43-46.

### 7.4 Kết luận điều hành

**CẬP NHẬT PHÁN QUYẾT ROUND 15 (08/08, xem `results/round15_synthesis.md`):**
- **Mục tiêu >80% (Top 3) / >50% (Top 1): KHÔNG thực tế trong 17 ngày** (5/5).
  Trần trung thực sau TOP-6 booster: Top 3 = **65-75%**, Top 1 = **28-40%**.
  Mục tiêu chính thức điều chỉnh: Top 3 = **70-75%**, Top 1 = **35-40%**.
- **TOP-6 BOOSTER** (chi tiết bảng §7.3 + `round15_synthesis.md`): pilot 20-30
  NCT + KPI; video "Bà Năm" không diễn + editor; SĐT thật + Zalo OA; Intel AI
  PC/NUC loan + OpenVINO (email BTC 09/08, không khóa kế hoạch theo nó); LOI
  UBND/Hội NCT đóng dấu; A/B demo 1022 vs Rightly. **Loại:** Streamlit paid
  tier, WER/MOS VIVOS lab (chỉ làm phụ chứng).
- **Lưu ý R15 so với R14:** R14 cắt OpenVINO/hardware; R15 mở lại NHƯNG chỉ
  dưới dạng "Intel loan PC" (chi phí 0, xin qua BTC) — nếu Intel từ chối, giữ
  narrative CPU-only như cũ, không mua hardware.

**CẬP NHẬT PHÁN QUYẾT ROUND 14 (08/08, xem `results/round14_synthesis.md`):**
- **SDG Primary (form bắt buộc chọn 1): SDG 16** (Peace, Justice & Strong
  Institutions) — 4/5 hội đồng. Target 16.3 access to justice + 16.10 access to
  information; tránh SDG 3 "health-washing" (không có KPI y tế); ít đội 13-17
  chọn → khác biệt. Hap 2025 dùng SDG 3 (y tế thật) — không bắt chước.
- **Song ngữ (đề xuất C) — chốt thu hẹp:** form 150 từ = tiếng Anh 100%; video
  2' = giọng VN + phụ đề EN hard-burned; UI = 100% tiếng Việt. Không dịch
  toàn bộ (lãng phí + rủi ro claim/consent).
- **Cắt OpenVINO/hardware** (scope creep, ROI âm trong 17 ngày); thay bằng
  narrative "CPU-only int8 chạy PC phổ thông" + limitation trung thực.
- Tên cuộc thi chuẩn: Intel Vietnam AI Impact Festival 2026 (VAIIF26) — đã
  sửa toàn repo, transcript cũ là nhật ký (giữ nguyên).

- **Top 3 là mục tiêu THỰC TẾ** nếu giữ kỷ luật Top-12 (đặc biệt video + pilot +
  150 từ). Đây là mục tiêu chính của Gate D (≥45/50).
- **Top 1 là "không xa, nhưng đắt"**: phải thắng bằng pilot thật + số liệu lớn +
  kể chuyện — 3 mảng duy nhất chúng ta có thể vượt nhóm hardware. Không đặt áp lực
  nếu pilot không đủ người (giữ trung thực, không thổi claim).
- Quyết định gỡ "giả OpenVINO" khỏi narrative (không có máy) — thay bằng
  "CPU-only, int8, chạy được trên PC phổ thông" = bất lợi nhỏ, giữ được claim check.

## 8. Hành động tăng tương thích ngay (Top-12 Round 13 + phán quyết R14)

1. 09/08: C mở Google Form nộp bài → liệt kê TẤT CẢ trường (gồm câu Primary SDG)
   + yêu cầu video/consent (chú ý mục ký cho thí sinh <18); chốt hồ sơ bảng Học
   sinh (3 thành viên 13-17 + trường học).
2. 09/08: T chạy WER/MOS trên VIVOS (760 wav sẵn có) → số liệu speech thật.
3. 09-10/08: C viết 5 phiên bản 150 từ; chốt tên ≤10 từ.
4. 11/08: lock 150 từ tiếng Anh + **SDG 16** (target 16.3/16.10) + số liệu nguồn;
   P gửi LOI.
5. 12/08: public link + voice FAQ + consent chuẩn; 13/08: pilot thật; 16/08: video
   (giọng VN + phụ đề EN); 22-24/08: sweep hồ sơ.
