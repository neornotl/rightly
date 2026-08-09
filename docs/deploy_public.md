# Deploy public (F3) — 09/08/2026

Mục tiêu 12/08: **public link chính (Streamlit Cloud) + link backup (HF
Spaces)**. Chỉ còn việc nhấn nút khi: T xong key rotation (F4) + FAQ (F5) +
P xác minh SĐT (contacts.json verified=true) + C giao corpus bổ sung.

## 0. Trước khi bấm Deploy (1 lệnh)

```bash
python scripts/predeploy_check.py
```

Phải trả về 0 FAIL. FAIL = có secret trong repo / import lỗi / thiếu dữ liệu.

## 1. Streamlit Cloud (kênh chính)

1. Push repo lên GitHub (đã có: `neornotl/tieng-lang-v4`).
2. streamlit.io → New app → chọn repo, branch `master`, main file `app/ui.py`.
3. Settings → Secrets → dán nội dung theo `.streamlit/secrets.toml.example`
   (3 key Groq + 1 key Gemini + rate limit).
4. Deploy. Lưu URL chính thức.

## 2. HF Spaces (link backup — nếu Streamlit bị chặn/giới hạn)

1. huggingface.co → New Space → SDK: Streamlit, public.
2. Upload repo (hoặc git remote thứ 2), đặt main file `app/ui.py`.
3. Settings → Variables → dán cùng danh sách secret (tên file không quan trọng,
   đọc từ env; app merge tự động qua `_merge_streamlit_secrets`).
4. Nhấn Deploy. Lưu URL backup.

## 3. Checklist sau deploy (chạy với browser thật)

- [ ] Tải trang: title "Rightly - DEMO", không lỗi import.
- [ ] Hỏi "Thủ tục cấp giấy xác nhận hộ khẩu?" → trả lời có trích dẫn.
- [ ] Hỏi "Khám bệnh bằng bảo hiểm y tế cần mang gì?" → trả lời FAQ (không mất
  tiền API, có `faq_ms`).
- [ ] Nút "Gọi ngay" ẨN khi contacts chưa verified (cảnh báo hiện đúng).
- [ ] Sau 60+ câu hỏi nhanh → bị chặn rate limit (thử bằng incognito khác IP).
- [ ] Xóa 1 key Groq khỏi Secrets → rotate sang key 2 (xem log instance).
- [ ] Tắt toàn bộ Groq keys → fallback Gemini trả lời.
- [ ] Mock mode vẫn chạy nếu tắt hết secrets (APP_MODE=mock).

## 4. Chi phí & hạn mức (thật, trung thực)

- Groq free tier: ~1k request/ngày/model (bằng xoay 3 key = ~3k/ngày, đủ pilot).
- Gemini free tier: 15 RPM (fallback khẩn cấp, không phải kênh chính).
- FAQ (F5) chặn ~60-70% câu hỏi demo → giảm tiêu thụ API đáng kể khi demo.

## 5. Chưa làm / chưa thể làm từ máy này

- Không có tài khoản Streamlit Cloud/HF + token → việc bấm Deploy thuộc về T
  (2-3h, hoặc 30 phút nếu có sẵn tài khoản).
- Zalo OA (10-11/08) — kênh phụ, KHÔNG chặn mốc public link 12/08.
