# Submission Checklist — Intel Vietnam AI Impact Festival 2026 (VAIIF26) (≥45/50, hạn 25/08/2026)

Mục tiêu Gate D. Mọi mục đánh status theo quy tắc role.md: TODO /
IN_PROGRESS / BLOCKED / READY_FOR_HUMAN_REVIEW / VERIFIED / DONE.
OpenCode chỉ được phép đánh READY_FOR_HUMAN_REVIEW, không tự DONE các mục
cần xác nhận con người (hiệu lực văn bản, consent, claim, GTM, video).

## 1. Toán điểm mục tiêu (đồng thuận hội đồng Round 6: ~36–42; cần ≥45)

| Khu | Tối đa | Mục tiêu | Điều kiện để đạt |
|---|---|---|---|
| M1 Impact & Inclusion | 15 | **14** | Pilot người cao tuổi có consent, task metrics, accessibility evidence và testimony |
| M2 AI Innovation: App & Impl | 20 | **17** | Public self-serve link + local edge inference + ethics/evaluation; GTM để 0 |
| M3 Technical & Skills | 15 | **15** | NPU benchmark thật, offline demo, stack/software/UI/RAG evidence tái lập |
| **Tổng** | 50 | **46** | Kịch bản stretch; chỉ đạt nếu NPU, pilot và video đều xác minh được |

Điểm tối đa kỳ vọng nếu đủ máy AI PC + pilot đầy đủ: M1 14 + M2 19 + M3 15
= 48. Rủi ro lớn nhất làm rớt xuống <45: thiếu public link thật, thiếu GTM,
thiếu pilot/user testimony.

## 2. Checklist theo track (owner theo role.md)

### [T] Technical & AI Engineering

- [ ] [T] Deploy public link (Streamlit Cloud) không lộ secret — **+2đ M2**
  (deadline 18/08; P thêm 1–2 user ngoài đội)
- [ ] [T] Benchmark NPU/AI PC thật: model/version, NPU utilization, RAM,
  latency p50/p95, cold start, throughput và cloud baseline. Không gọi là
  OpenVINO nếu backend thực tế không dùng OpenVINO.
- [ ] [T] Offline failure test: rút mạng sau bootstrap, chạy ít nhất 3 task,
  quay video timestamp + log `offline=true`; test restart/OOM/timeout fail-closed
- [ ] [T] Config/timeout/retry production-grade cho cloud LLM (F7) — nền cho
  deploy ổn định
- [ ] [T] Thu hẹp pattern RED false positive (F10) + test phủ — chất lượng R3
- [ ] [T] Full-system trace ẩn danh mới nhất + hardware/model/latency ghi rõ
- [ ] [T] Local release bundle có checksum, model tag, config, runbook và lệnh tái lập
- [ ] [T] Release + tag; tài liệu kỹ thuật khớp code (ĐoD T)

### [C] Content, Compliance & Evaluation

- [ ] [C] Problem statement ≤150 từ (tiếng Anh) + tên ≤10 từ — **+1–2đ M1**
- [ ] [C] SDG mapping (đề xuất 3, 10, 11, 16) + giải thích liên kết — **+1đ M1**
- [ ] [C] Source verification: xác minh 11 nguồn (cơ quan ban hành, URL, hiệu
  lực) + gọi hotline xác minh, ghi log (`law_verification_log.md`) — đầu ra
  bắt buộc Gate B
- [ ] [C] Đánh dấu trạng thái nguồn active_verified/pending/expired trong
  `law_status.json` (human review bắt buộc — chỉ READY_FOR_HUMAN_REVIEW)
- [ ] [C] Claim check: README/MASTER/video/form — không claim quá bằng chứng
- [ ] [C] Evidence matrix đầy đủ mọi tiêu chí rubric (`docs/rubric_evidence_matrix.md`)
- [ ] [C] Ground truth R1–R4: false accept/reject phân tích; tách development/
  final test — ĐoD C
- [ ] [C] Accessibility report cho người cao tuổi: cỡ chữ, tốc độ TTS,
  số lần nhắc lại, tỷ lệ hiểu đúng và lỗi thao tác
- [ ] [C] Safety red-team pilot: câu hỏi khẩn cấp/hình sự/thiếu nguồn,
  kiểm tra refusal/chuyển tuyến và human oversight; tách khỏi synthetic
- [ ] [C] Consent templates pilot + thu âm + video (`consent_form_v1.md`) —
  giao P trước khi tuyển (ưu tiên sáng thứ 7 08/08)

### [P] Pilot, Presentation & Partnership

- [ ] [P] Tuyển 8–10 người (ưu tiên cao tuổi/rào cản số) + consent — **+1–2đ M1**
- [ ] [P] Pilot 3 task chuẩn + 1 tự do, log ẩn danh (task completion, time,
  satisfaction) — evidence M1 + M2 controlled test
- [ ] [P] Pilot local với người cao tuổi: consent riêng cho audio/video/transcript;
  log device/mode/task/time/success/satisfaction; mã participant không định danh
- [ ] [P] Thu ít nhất 3 testimony ngắn có consent, tập trung vào nghe, hiểu và
  hoàn thành bước tiếp theo; không gọi là adoption
- [ ] [P] Video 2 phút: người cao tuổi dùng bản local + tắt mạng + spoken citation
  + cảnh từ chối/chuyển tuyến + bảng pilot thật + phụ đề — **+1–2đ M1/M2**
- [ ] [P] Public self-serve walkthrough + feedback tự nguyện có consent (không gọi là
  partnership/traction nếu chưa có đối tác hoặc người dùng độc lập)
- [ ] [P] Pitch/slide đồng bộ với C; demo dự phòng bằng video nếu live lỗi

### [T+C+P] Gate D — Hồ sơ tổng hợp

- [ ] [C+P] Form nộp: tên, mô tả 150 từ, video link, dự án (đội ≤3, học sinh
  13-17 đang học THCS/THPT/CĐ nghề; consent phụ huynh/giám hộ — kiểm eligibility)
- [ ] [T+C+P] Backup + submission proof (screenshot, mã xác nhận) — ĐoD Gate D
- [ ] [T+C+P] Nhất quán: repo, README, video, form, evidence matrix

## 3. Mốc thời gian (hôm nay 08/08 → nộp 25/08)

| Deadline | Mốc | Chịu trách |
|---|---|---|
| 08–09/08 (T7+CN) | C: xác minh 11 nguồn+hotline, problem statement 150 từ + SDG, eval split + hard negatives, claim check, consent. P: tuyển 8–10 người + consent, lịch pilot + shot-list, email đối tác + GTM one-pager, demo script chốt | C, P |
| 10/08 | Nháp problem statement, SDG, GTM one-pager; checklist video | C |
| 12/08 | Public link chạy; pipeline ổn định trên link | T |
| 12/08 | Public link chạy; pipeline ổn định trên link | T |
| 15/08 | Source verification report; law_status human review xong | C (+T) |
| 18/08 | 1–2 user ngoài đội test qua public link; feedback | P+T |
| 20/08 | Pilot 8–10 người xong + log ẩn danh; consent đủ | P+C |
| 22/08 | Video 2 phút dựng xong (có consent); C duyệt claim | P+C |
| 23/08 | Form điền xong; evidence matrix chốt; claim check cuối | C+P |
| 24/08 | Dry-run nộp; backup; submission proof | T+C+P |
| 25/08 | **NỘP** | T+C+P |

## 4. Rủi ro & giảm thiểu

- Không có máy AI PC → mất 1–2đ M3; thay thế: chứng minh local CPU path
  (PhoWhisper int8) + OpenVINO plan; ghi rõ trong limitations.
- Không đủ 8–10 người pilot → mất evidence M1; giảm thiểu: ghi rõ giới hạn
  thực tế (ĐoD P cho phép), ưu tiên ít nhất 3–5 người + 2 người ngoài đội.
- Public link chậm/rớt → mất 2đ M2; giảm thiểu: chuẩn bị từ 12/08, fallback
  video demo có timestamp.
- Claim quá bằng chứng → mất uy tín + điểm C; claim check 23/08 bắt buộc.
