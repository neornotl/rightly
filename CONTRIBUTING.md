# Contributing

Cảm ơn bạn quan tâm đóng góp cho **Rightly**. Đọc kỹ mục này trước khi
gửi thay đổi — repo là dự án có vai trò rõ ràng ([T]/[C]/[P], xem
`docs/team_status.md` và `QUESTS.md`).

## Vai trò và ai được làm gì

| Vai trò | Trách nhiệm |
|---|---|
| [T] Technical | Code, pipeline, eval, deploy, hỗ trợ kỹ thuật |
| [C] Content & Compliance | Văn bản pháp luật, label, responsible AI, consent, claim check |
| [P] Pilot & Partnership | Pilot, video, đối tác, GTM, pitch |

- OpenCode (công tác viên của T) không làm thay C/P. C/P tự chạy nhiệm vụ,
  nhờ T khi cần kỹ thuật.
- Thay đổi liên quan hiệu lực văn bản pháp luật, consent, claim, GTM **bắt
  buộc có xác nhận con người** — chỉ đạt trạng thái READY_FOR_HUMAN_REVIEW,
  không tự DONE.

## Luồng đóng góp

1. Xem `QUESTS.md` + `docs/submission_checklist.md` chọn quest chưa có ai làm.
2. Nhánh mới: `git checkout -b quest/<tên-quest>`.
3. Code theo chuẩn:
   - `ruff check .` sạch.
   - `python -m pytest tests/ -q` — toàn bộ test xanh (hiện 74+).
   - `python scripts/preflight.py` — 9/9.
   - Không thêm secret; giữ `.env`/`data/private_cache/` ngoài git.
4. Cập nhật tài liệu tương ứng (MASTER, team_status, data card nếu đụng dữ liệu).
5. Commit ngắn gọn theo phong cách repo, push, mở PR lên `master`.

## Quy tắc dữ liệu & riêng tư

- Không commit SĐT cá nhân mới, audio raw, ảnh người tham gia pilot.
- Thêm dữ liệu văn bản luật: đi kèm `data/law_status.json` cập nhật + ghi
  nguồn chính thức.
- Không dùng dữ liệu hư cấu làm bằng chứng pilot; mọi kết quả demo ghi rõ
  "SYNTHETIC DEMO".

## Hội đồng AI pool

Quyết định lớn (điểm hướng, kiến trúc, nội dung nhạy cảm) được đưa ra hội
đồng 6 thành viên (5 mô hình + OpenCode). Kết quả lưu tại `debate_output/`.
