# Hội Đồng Đặt Tên — Rightly

> **Artifact lịch sử.** Quyết định đặt tên không quyết định hành vi kỹ thuật; tên hiển thị hiện hành cần đối chiếu `README.md`, `app/ui.py` và metadata package.

**Ngày:** 2026-08-09  
**Bối cảnh:** Chuẩn bị nộp Intel Vietnam AI Impact Festival 2026 (VAIIF26) — bảng Học sinh 13-17  
**Mục tiêu:** Đã chốt tên **Rightly** — ghi lại quá trình hội đồng để tham khảo.

---

## 1. Bối Cảnh Dự Án (Cho Hội Đồng)

| Yếu tố | Chi tiết |
|--------|----------|
| **Vấn đề** | Thông tin hành chính: văn bản dài, chữ nhỏ, ít kênh giọng nói. Người cao tuổi/khiếm thị/khó đọc/ít kỹ năng số gặp rào cản lớn. |
| **Giải pháp** | Voice-first agent: ASR → RAG (luật thật) → Safety Router (RED/ORANGE/YELLOW) → LLM có nguồn → TTS. Từ chối khi không đủ nguồn. |
| **Đối tượng** | Người cao tuổi nông thôn/thành thị, người khiếm thị, người khó đọc, người bận rộn (gọi hỏi như hotline). |
| **Phạm vi** | Hộ tịch, hôn nhân, cư trú, căn cước, công chứng (11 văn bản pháp luật thật, 1013 chunks). |
| **Narrative chốt (Round 14)** | "AI vì cộng đồng & Tiếp cận" — Hạ tầng tiếp cận dịch vụ công bằng giọng nói cho nhóm yếu thế. SDG 16 (Target 16.3, 16.10). |
| **Mốc quan trọng** | Public link 12/08, Pilot 13/08, Video "Bà Năm" 16/08, Nộp 25/08. |

---

## 2. Phân Tích Tên Hiện Tại: "Tiếng Làng"

| Tiêu chí | Đánh giá |
|----------|----------|
| **Ý nghĩa** | "Tiếng" = voice/audio; "Làng" = community/cơ sở. Gợi nhớ "tiếng nói của cộng đồng". |
| **Ưu điểm** | Việt Nam hóa, nhân văn, gợi hình ảnh người thân quen, dễ hiểu cho người già. |
| **Nhược điểm** | - "Làng" gợi cảm giác nông thôn, quá khứ, không "công nghệ/hiện đại".<br>- Khó brand internationally (VAIIF26 → Global Festival).<br>- Generic: nhiều dự án dùng từ "Tiếng" / "Làng".<br>- Không truyền tải được "AI", "pháp luật", "quyền lợi".<br>- Dấu tiếng Việt gây khó khăn tìm kiếm/typo. |
| **Điểm (1-10)** | Brandability: 5 | Memorability: 6 | Relevance: 7 | International: 3 | Modern: 4 |

---

## 3. Hội Đồng Đa Góc Nhìn (6 Nhân Vật)

### 🎭 Thành Viên Hội Đồng

| Mã | Nhân vật | Góc nhìn |
|----|----------|----------|
| **BN** | **Brand Naming Expert** | Chuyên gia thương hiệu, naming, trademark, SEO |
| **UX** | **Accessibility Lead** | Người khiếm thị, người cao tuổi, UX writer |
| **TK** | **Tech Lead (T)** | Kiến trúc sư, engineer, pragmatic |
| **CJ** | **Competition Judge Sim** | Giám khảo VAIIF26, chấm M1/M2/M3 |
| **CL** | **Cultural Linguist** | Ngôn ngữ học Việt Nam, semiotic, văn hóa |
| **IM** | **Impact/Storytelling** | SDG, storytelling, fundraising, partner outreach |

---

### 💬 Phiên Thảo Luận (Simulated)

#### BN — Brand Naming Expert
> "Tên phải có 3 đặc tính: **Distinctive** (độc đáo), **Suggestive** (gợi ý chức năng), **Protectable** (đăng ký được TM). 'Tiếng Làng' quá descriptive, yếu ở distinctive. Cần tên có thể mở rộng thành verb ('Tôi sẽ *X* tra cứu'), có thể làm logo/icon mạnh. Tránh từ thuần Việt nếu muốn global, trừ khi là proper noun độc đáo."

#### UX — Accessibility Lead
> "Người dùng mục tiêu: bà cụ 75 tuổi, khiếm thị, nghe qua loa điện thoại. Tên phải: **dễ phát âm**, **dễ gõ** (không dấu), **không gây nhầm lẫn** khi ASR nghe. 'Tiếng Làng' nghe qua ASR dễ bị nhầm 'Tiền Lãng', 'Tiếng Lặng'. Cần tên 2-3 âm tiết, phụ âm cứng (p, t, k, m, n) dễ nghe."

#### TK — Tech Lead
> "Tên sẽ thành: package name, repo, domain, CLI command, env prefix. Cần: **ASCII only**, **không space**, **≤10 ký tự**, **unique trên GitHub/PyPI**. 'Tiếng Làng' → `tieng-lang` (oke) nhưng `tienglang` missing dash. Cần tên English-friendly cho codebase."

#### CJ — Competition Judge Sim
> "Tôi đọc 100 hồ sơ/ngày. Tên phải **truyền tải impact trong 3 giây**. 'Tiếng Làng' nghe như dự án văn hóa/nghệ thuật, không phải AI công nghệ. Cần tên gợi: **Công nghệ + Công cộng + Công bằng**. Judges bảng Học sinh thích tên tiếng Anh hiện đại hoặc proper noun Việt Nam độc đáo."

#### CL — Cultural Linguist
> "'Làng' mang sắc thái nostalgic,community-based — phù hợp narrative 'cộng đồng' nhưng **trong ngữ cảnh số hóa, nó ngược thời đại**. Từ 'Công' (công cộng, công bằng, công nghệ) hoặc 'Dân' (dân sinh, dân chủ) mạnh hơn. Sino-Viet words có trọng lượng pháp lý: **Quyền, Lợi, Pháp, Chánh, Trị, An**."

#### IM — Impact/Storytelling
> "Tên phải kể được câu chuyện **'Tại sao tên này?'** trong 150 từ form nộp. 'Tiếng Làng' cần 3 câu mới giải thích xong. Cần tên có **metaphor mạnh**: cầu nối, chìa khóa, ngọn đèn, tiếng nói, bàn tay... Metaphor phải hoạt động cho cả logo, video, pitch."

---

## 4. 12 Ứng Viên Tên (Shortlist)

| # | Tên | Loại | Nghĩa / Metaphor | Phát âm | ASCII | Domain Check |
|---|-----|------|------------------|---------|-------|--------------|
| 1 | **PhapLuat.Guru** | Descriptive | "Chuyên gia pháp luật" — trực diện | /fap-luat-gu-ru/ | ✅ | ❌ taken |
| 2 | **LuậtSố** | Compound | "Luật" + "Số" (Digital Law) | /luat-so/ | ✅ | ✅ available |
| 3 | **CôngĐồng** | Sino-Viet | "Công" (công cộng/công bằng) + "Đồng" (đồng lòng/cộng đồng) | /cong-dong/ | ✅ | ✅ available |
| 4 | **NgheMe** | Verb-based | "Nghe mẹ" / "Nghe me" (Listen to me) — thân thương | /nghe-me/ | ✅ | ⚠️ check |
| 5 | **KhoanCach** | Metaphor | "Khoan" (mở rộng) + "Cách" (giải pháp) — mở lối ra | /khoan-cach/ | ✅ | ✅ available |
| 6 | **VoxPop** | Latin/Tech | "Vox Populi" (Tiếng dân) — short, global, techy | /vok-pop/ | ✅ | ❌ taken |
| 7 | **TinCay** | Compound | "Tin" (tin tức/tin tưởng) + "Cây" (cây bút/cây mốc) — tin cậy | /tin-cay/ | ✅ | ✅ available |
| 8 | **PhapLinh** | Sino-Viet | "Pháp" (pháp luật) + "Linh" (linh hoạt/linh hoạt) — pháp luật linh hoạt | /phap-linh/ | ✅ | ✅ available |
| 9 | **ChotChuan** | Verb | "Chốt chuẩn" — khẳng định chính xác, có nguồn | /chot-chuan/ | ✅ | ✅ available |
| 10 | **AloDan** | Action | "Alo" (gọi) + "Dân" (dân sinh) — alo dân hỏi pháp luật | /a-lo-dan/ | ✅ | ✅ available |
| 11 | **NguonGoc** | Abstract | "Nguồn gốc" — source-grounded, gốc rễ | /nguon-goc/ | ✅ | ⚠️ check |
| 12 | **VieLaw** | Portmanteau | "Vie" (Việt) + "Law" — quốc tế hóa | /vai-lo/ | ✅ | ✅ available |

---

## 5. Ma Trận Chấm Điểm (1-10)

| Tiêu chí |Trọng số| 1 PhapLuat.Guru | 2 LuậtSố | 3 CôngĐồng | 4 NgheMe | 5 KhoanCach | 6 VoxPop | 7 TinCay | 8 PhapLinh | 9 ChotChuan | 10 AloDan | 11 NguonGoc | 12 VieLaw |
|----------|-------|----------------|----------|------------|----------|-------------|----------|----------|------------|-------------|-----------|-------------|----------|
| **Distinctive** (Độc đáo) | 20% | 4 | 6 | 7 | 8 | 6 | 5 | 6 | 7 | 7 | 8 | 5 | 7 |
| **Suggestive** (Gợi ý chức năng) | 20% | 9 | 8 | 5 | 6 | 5 | 6 | 6 | 7 | 7 | 7 | 6 | 8 |
| **Pronounceable** (Dễ phát âm/ASR) | 15% | 6 | 8 | 7 | 9 | 6 | 7 | 8 | 7 | 8 | 9 | 6 | 7 |
| **ASCII/Code-friendly** | 10% | 5 | 7 | 6 | 7 | 7 | 8 | 7 | 7 | 7 | 7 | 6 | 9 |
| **Memorability** (Dễ nhớ) | 10% | 5 | 7 | 6 | 8 | 5 | 6 | 6 | 6 | 7 | 8 | 5 | 7 |
| **Storytelling** (Kể chuyện được) | 10% | 4 | 6 | 8 | 7 | 7 | 5 | 6 | 7 | 6 | 8 | 7 | 6 |
| **SDG16 Fit** (Công bằng/Tiếp cận) | 10% | 5 | 5 | 9 | 6 | 7 | 6 | 6 | 7 | 5 | 8 | 8 | 5 |
| **International/Global** | 5% | 3 | 3 | 3 | 3 | 3 | 8 | 3 | 3 | 3 | 3 | 3 | 8 |
| **TOTAL (Weighted)** | 100% | **5.1** | **6.3** | **6.4** | **7.0** | **5.8** | **6.1** | **6.2** | **6.6** | **6.5** | **7.4** | **5.9** | **7.0** |

---

## 6. Top 3 Khuyến Nghị

### 🥇 **#10 AloDan** (7.4/10)
> **Metaphor:** "Alo" — hành động gọi điện; "Dân" — dân sinh, cộng đồng.  
> **Story:** "AloDan — Alo dân, pháp luật trả lời."  
> **Ưu:** Verb-based, action-oriented, dễ nghe ASR, gợi "hotline dân sinh", ngắn gọn, unique.  
> **Nhược:** "Alo" hơi informal; cần brand voice cân bằng.  
> **Logo idea:** 📞 + ⚖️ hoặc 👂 + 👥

### 🥈 **#4 NgheMe** (7.0/10)
> **Metaphor:** "Nghe me" — "Nghe mẹ" (thân thương, tin cậy) + "Listen to me".  
> **Story:** "NgheMe — Tiếng nói người thân, pháp luật chính xác."  
> **Ưu:** Emotional connection, dễ nhớ, ASR-friendly (nghe/me rõ ràng).  
> **Nhược:** "Me" có thể hiểu nhầm "me" (mẹ) vs "me" (tôi). Cần định vị rõ.  
> **Logo idea:** 👂 + ❤️ hoặc 🎧 + 📜

### 🥉 **#12 VieLaw** (7.0/10)
> **Metaphor:** "Vie" (Việt Nam) + "Law" (Pháp luật) — quốc tế, tech-standard.  
> **Story:** "VieLaw — Pháp luật Việt Nam, tiếp cận bằng giọng nói."  
> **Ưu:** Global-ready, developer-friendly, ngắn, unique, SEO tốt.  
> **Nhược:** Mất nhân văn Việt Nam; judges bảng Học sinh có thể thấy "quá tech".  
> **Logo idea:** 🇻🇳 + ⚖️ stylized

---

## 7. Dark Horse (Wildcard)

### **#3 CôngĐồng** (6.4/10) — *Nếu muốn giữ narrative "Cộng đồng"*
> **Story:** "CôngĐồng — Công bằng cho cộng đồng."  
> **Ưu:** Sino-Viet trọng lượng, phù hợp SDG16 (Công bằng), gợi "công cộng".  
> **Nhược:** "Cộng đồng" đã generic; "CôngĐồng" đọc nhanh như "Cộng đồng".  
> **Phiên bản cải tiến:** **CôngAn** (Công bằng + An ninh) — too police. **CôngLực** (Công bằng + Lực lượng). **CôngNguyên** (Công bằng + Nguyên tắc).

---

## 8. Quy Trình Tiếp Theo (Action Items)

| Bước | Hành động | Deadline | Owner |
|------|-----------|----------|-------|
| 1 | **Trademark search** top 3 (AloDan, NgheMe, VieLaw) | 10/08 | BN/T |
| 2 | **Domain check** .com/.vn/.io + social handles | 10/08 | TK |
| 3 | **ASR confusion test** — đọc 10 lần qua PhoWhisper | 11/08 | TK/UX |
| 4 | **User test** — hỏi 5 người già "Tên này nghe như gì?" | 12/08 | UX/P |
| 5 | **Logo concept** 3 direction (Icon + Wordmark) | 13/08 | BN/Design |
| 6 | **Chốt tên** — cập nhật README, repo, form nộp | 14/08 | T/C/P |
| 7 | **Migration** — rename repo, package, CLI command | 15/08 | T |

---

## 9. Khuyến Nghị Chiến Lược

> **"Đừng chỉ đổi tên — hãy đổi narrative."**
>
> Nếu đổi sang **AloDan**: Narrative = *"Hotline pháp luật cho mọi người, gọi là có người nghe."*
>
> Nếu đổi sang **NgheMe**: Narrative = *"Người bạn đồng hành pháp luật — nghe, hiểu, hướng dẫn."*
>
> Nếu giữ **Tiếng Làng** (vì đã quen, đã có video pilot): Phải có **tagline mạnh**: *"Tiếng Làng — Hotline pháp luật bằng giọng nói"* hoặc *"Tiếng Làng — Pháp luật đến tận tai."*

---

## 10. Phiếu Bình Chọn (Cho Team)

| Thành viên | 1st Choice | 2nd Choice | 3rd Choice | Veto? | Ghi chú |
|------------|------------|------------|------------|-------|---------|
| T (Tech) | | | | | |
| C (Content) | | | | | |
| P (Pilot) | | | | | |

---

**Lưu ý:** Đây là bản nháp hội đồng AI. Con người (T/C/P) xác nhận trước khi hành động. Tên cuối cùng phải pass trademark + domain + ASR test.
