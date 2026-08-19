# Bản đồ tài liệu

Tài liệu trong repository được chia thành hai loại:

- **Hiện hành:** mô tả code, dữ liệu runtime, cách chạy và các ràng buộc đang áp dụng.
- **Lịch sử/tham chiếu:** snapshot, báo cáo, checklist hoặc quyết định theo một mốc thời gian. Các file này có nhãn ở đầu và không thay thế mã nguồn.

## Đọc theo nhu cầu

| Nhu cầu | Tài liệu |
| --- | --- |
| Hiểu nhanh dự án | [README](../README.md) · [MASTER](MASTER.md) |
| Cài và chạy | [Setup](setup.md) · [Architecture](architecture.md) |
| Dữ liệu và đánh giá | [Data card](data_card.md) · [Dataset card](evaluation_dataset_card.md) · [Protocol](evaluation_protocol.md) |
| An toàn và riêng tư | [Responsible AI](responsible_ai.md) · [Privacy](privacy_deletion_policy.md) · [Threat model](threat_model.md) · [Limitations](limitations.md) |
| Chuẩn bị vận hành | [Deployment strategy](deployment_strategy.md) · [Pilot protocol](pilot_protocol.md) · [Hardware benchmark](hardware_benchmark_plan.md) · [Gates](../gates/README.md) |

## Tài liệu lịch sử

`baseline_*`, `*_report`, `*_review`, `*_checklist`, `team_status.md`, `fit_assessment_aiif26.md`, `competition_aiif26.md` và tài liệu council/naming được giữ lại để truy vết. Đừng dùng ngày, quota, tiến độ hoặc số liệu trong các file này làm facts hiện tại nếu chưa kiểm tra lại.

## Quy ước cập nhật

1. Ưu tiên code, test, `.env.example`, `data/law_status.json` và artifact runtime làm nguồn sự thật.
2. Ghi rõ trạng thái: **hiện hành**, **bản nháp**, **kế hoạch**, hoặc **lịch sử**.
3. Không biến kết quả fixture/demo thành claim pilot/production.
4. Không đặt secret, PII hoặc số liên hệ chưa xác minh trong tài liệu.
5. Giữ liên kết tương đối, heading ngắn và bảng chỉ dùng khi thực sự giúp so sánh.
