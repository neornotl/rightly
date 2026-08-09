# Question Source Catalog — Tiếng Làng v4.0

Generated: 2026-08-09 · For 10k Benchmark Generation (Phase B)

---

## Source Records

### SRC_001 — Cổng Dịch vụ công Quốc gia
- **source_name**: Cổng Dịch vụ công Quốc gia
- **official_owner**: Bộ Nội vụ / Chính phủ Việt Nam
- **base_url**: https://dichvucong.gov.vn
- **content_type**: FAQ theo nhóm sự kiện, chi tiết thủ tục hành chính, phản ánh/kiến nghị công khai
- **public_access**: true
- **personal_data_risk**: low (FAQ công khai, không dữ liệu cá nhân)
- **terms_or_license_note**: Cần xem điều khoản sử dụng tại trang; thường cho phép truy cập công khai thông tin thủ tục
- **automated_access_status**: robots.txt tồn tại, không chặn crawl công khai; cần delay + cache
- **allowed_use**: seed_only
- **human_reviewer**: C
- **review_date**: 2026-08-09
- **notes**: Chỉ lấy phần câu hỏi FAQ đã khử PII; không crawl hàng loạt; dùng làm seed để tạo paraphrase

### SRC_002 — Giải đáp Chính sách Online (Cổng Thông tin điện tử Chính phủ)
- **source_name**: Giải đáp Chính sách Online
- **official_owner**: Chính phủ Việt Nam / Bộ Thông tin và Truyền thông
- **base_url**: https://chinhphu.vn/giai-dap-chinh-sach-online
- **content_type**: Danh sách câu hỏi công khai theo lĩnh vực (hành chính, xã hội, kinh tế)
- **public_access**: true
- **personal_data_risk**: low (chỉ tiêu đề/câu hỏi tổng quát)
- **terms_or_license_note**: Nội dung chính sách công khai; câu trả lời chính thức dùng để xác định topic/source candidate, KHÔNG sao chép làm gold answer
- **automated_access_status**: robots.txt cho phép; cần respect rate limit
- **allowed_use**: seed_only
- **human_reviewer**: C
- **review_date**: 2026-08-09
- **notes**: Dùng câu hỏi để map topic; câu trả lời chỉ tham chiếu nguồn pháp lý, không làm gold

### SRC_003 — Bảo hiểm xã hội Việt Nam
- **source_name**: Bảo hiểm xã hội Việt Nam
- **official_owner**: Bảo hiểm xã hội Việt Nam
- **base_url**: https://baohiemxahoi.gov.vn
- **content_type**: Hỏi đáp BHXH, BHYT, BHTN, dịch vụ công
- **public_access**: true (phần công khai)
- **personal_data_risk**: **HIGH** (có thể chứa số BHXH, tên, email, quá trình đóng, dữ liệu cá nhân)
- **terms_or_license_note**: Cần kiểm tra kỹ điều khoản; phần tra cứu cá nhân KHÔNG được dùng
- **automated_access_status**: Có thể có anti-bot, CAPTCHA cho tra cứu cá nhân; phần FAQ công khai có thể truy cập
- **allowed_use**: metadata_only
- **human_reviewer**: C
- **review_date**: 2026-08-09
- **notes**: CHỈ lấy tiêu đề/câu hỏi tổng quát từ FAQ công khai; TUYỆT ĐỐI KHÔNG crawl phần tra cứu cá nhân; không lưu số BHXH, tên, email

### SRC_004 — Bộ Tư pháp & Cục Hành chính tư pháp
- **source_name**: Bộ Tư pháp / Cục Hành chính tư pháp
- **official_owner**: Bộ Tư pháp Việt Nam
- **base_url**: https://mot.gov.vn, https://moc.gov.vn
- **content_type**: Danh sách thủ tục, FAQ/hỏi đáp công khai (hộ tịch, chứng thực, trợ giúp pháp lý)
- **public_access**: true
- **personal_data_risk**: low (thủ tục chung, không dữ liệu cá nhân)
- **terms_or_license_note**: Cần kiểm tra; thông tin thủ tục hành chính thường công khai
- **automated_access_status**: robots.txt tồn tại; cần delay
- **allowed_use**: seed_only
- **human_reviewer**: C
- **review_date**: 2026-08-09
- **notes**: Phù hợp chủ đề hộ tịch, chứng thực - overlap tốt với corpus hiện tại

### SRC_005 — Pilot Questions (Có Consent)
- **source_name**: Pilot Questions (Người dùng thật)
- **official_owner**: Đội ngũ Tiếng Làng
- **base_url**: N/A (private, không public)
- **content_type**: Câu hỏi từ pilot 8-10 người có consent
- **public_access**: false
- **personal_data_risk**: medium (cần consent + scrub trước khi dùng)
- **terms_or_license_note**: Chỉ dùng khi có consent ký tên; lưu ngoài Git; repo chỉ chứa bản ẩn danh
- **automated_access_status**: N/A
- **allowed_use**: ingest_allowed (chỉ bản redacted)
- **human_reviewer**: P + C
- **review_date**: pending (chưa có pilot)
- **notes**: Placeholder 200 câu; chỉ điền khi đã có consent form signed

### SRC_006 — Search Logs Prototype (Có Consent)
- **source_name**: Search Logs Prototype
- **official_owner**: Đội ngũ Tiếng Làng
- **base_url**: N/A (private)
- **content_type**: Transcript đã scrub từ phiên demo/mock
- **public_access**: false
- **personal_data_risk**: low (đã scrub heuristic, ẩn danh session ID)
- **terms_or_license_note**: Chỉ dùng nếu user đã consent `SAVE_TRANSCRIPTS=true`
- **automated_access_status**: N/A
- **allowed_use**: ingest_allowed (chỉ bản đã scrub)
- **human_reviewer**: T + C
- **review_date**: pending
- **notes**: Không lưu raw transcript mặc định; chỉ xuất câu đã scrub + participant ID ẩn danh

### SRC_007 — Corpus Pháp luật Thật (Real Corpus)
- **source_name**: Corpus Pháp luật Thật (11 văn bản từ vanban.chinhphu.vn)
- **official_owner**: Chính phủ / Quốc hội Việt Nam
- **base_url**: https://vanban.chinhphu.vn
- **content_type**: Văn bản pháp luật gốc (Luật, Nghị định) — đã crawl, OCR, chunk
- **public_access**: true (văn bản chính quy)
- **personal_data_risk**: none (văn bản luật công khai)
- **terms_or_license_note**: Văn bản pháp luật công khai, không bản quyền; tuy nhiên cần ghi nguồn chính xác
- **automated_access_status**: Đã crawl xong (11 docs, 1013 chunks); crawl có delay, cache, respect robots
- **allowed_use**: ingest_allowed (đã ingest vào `data/chunks/real_chunks.jsonl`)
- **human_reviewer**: C
- **review_date**: 2026-08-07
- **notes**: **Chưa có status `active_verified`** — C cần review 11 nguồn trong `data/law_status.json` trước khi benchmark

---

## Nguồn KHÔNG DUYỆT (Blocked / Not Allowed)

| Nguồn | Lý do |
|-------|-------|
| Blog luật SEO, Q&A không rõ nguồn | Không xác minh được tính chính xác, rủi ro hallucination source |
| Facebook/Zalo/TikTok/YouTube comments | Điều khoản không cho phép crawl; dữ liệu không có provenance |
| Diễn đàn pháp luật có điều khoản cấm | Vi phạm terms of service |
| Câu do LLM tạo không có seed/provenance | Không có nguồn gốc, không thể verify |

---

## Summary Statistics

| Allowed Use | Count | Sources |
|-------------|-------|---------|
| `seed_only` | 3 | SRC_001, SRC_002, SRC_004 |
| `metadata_only` | 1 | SRC_003 |
| `ingest_allowed` | 3 | SRC_005, SRC_006, SRC_007 |
| `blocked` | 4+ | Blog SEO, Social media, Forums, LLM-generated |

---

## Next Steps (Phase C)

1. **C review SRC_007**: Xác minh 11 nguồn trong `data/law_status.json` → cập nhật status `active_verified`
2. **C/P chuẩn bị consent form** cho SRC_005 (pilot) — theo `deliverables/C/consent_form_v1.md`
3. **T tạo taxonomy & schema** (Phase C) dựa trên các topic từ corpus thật
4. **Không crawl thêm** cho đến khi C duyệt source catalog này