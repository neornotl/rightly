# Kho văn bản pháp luật

*English below.*

Thư mục này là kho văn bản pháp luật nguồn của dự án Rightly. Các tệp văn bản thô được tổ chức theo loại văn bản để phục vụ tra cứu, xây dựng corpus và đối chiếu căn cứ pháp lý.

## Cấu trúc

- [`laws-n-codes`](laws-n-codes/README.md): Luật, bộ luật và một số văn bản hợp nhất.
- [`decrees-n-decisions`](decrees-n-decisions/README.md): Nghị định và quyết định.
- [`circulars`](circulars/README.md): Thông tư và hướng dẫn chuyên ngành.
- [`ordinances-n-resolutions`](ordinances-n-resolutions/README.md): Pháp lệnh và nghị quyết.
- [`dispatches-n-guidelines`](dispatches-n-guidelines/README.md): Công văn và hướng dẫn triển khai.
- [`archived`](archived/README.md): Văn bản lịch sử, hết hiệu lực hoặc bị thay thế; chỉ dùng để tham khảo.

Một số nhóm có thư mục `en/` lưu bản tiếng Anh chọn lọc. Bản dịch dùng để hỗ trợ đọc hiểu và đối chiếu thuật ngữ; văn bản tiếng Việt là nguồn ưu tiên khi cần xác định nội dung pháp lý.

## Nguyên tắc sử dụng

- Corpus này là nguồn thô, không phải tự nó là danh mục hiệu lực pháp lý đầy đủ.
- Không suy ra hiệu lực chỉ từ tên tệp, năm ban hành hoặc việc văn bản có mặt trong corpus.
- Trước khi trích dẫn, kiểm tra số hiệu, cơ quan ban hành, điều khoản hiệu lực, sửa đổi/thay thế và phạm vi áp dụng trong danh mục hiệu lực pháp lý của dự án.
- Chỉ trích điều, khoản, điểm trực tiếp liên quan đến câu hỏi; không ghép quy định từ các văn bản hoặc thời điểm khác nhau.
- Không dùng tài liệu trong `archived/` làm nguồn trích dẫn chính cho quy định hiện hành.

## Danh mục và kiểm tra trạng thái

- [Danh mục nguồn](../data/source_registry.csv): số hiệu, cơ quan ban hành, ngày hiệu lực, URL nguồn và trạng thái đã kiểm chứng.
- [Danh mục hiệu lực pháp lý](../data/law_status.json): nguồn dùng để kiểm tra trích dẫn, ngày hết hiệu lực và văn bản thay thế.
- [Báo cáo đối chiếu tệp nguồn](../data/rightly_source_file_audit.csv): kết quả đối chiếu metadata với các tệp nguồn có trong dự án.
- [README dự án](../README.md): mục đích, kiến trúc và hướng dẫn vận hành Rightly.

---

# Legal corpus — legal source documents

This directory is Rightly's source collection of legal documents. Raw text files are organized by document type for research, corpus construction, and verification of legal authority.

## Structure

- [`laws-n-codes`](laws-n-codes/README.md): Laws, codes, and some consolidated documents.
- [`decrees-n-decisions`](decrees-n-decisions/README.md): Decrees and decisions.
- [`circulars`](circulars/README.md): Circulars and sector-specific implementation guidance.
- [`ordinances-n-resolutions`](ordinances-n-resolutions/README.md): Ordinances and resolutions.
- [`dispatches-n-guidelines`](dispatches-n-guidelines/README.md): Official dispatches and implementation guidance.
- [`archived`](archived/README.md): Historical, expired, or superseded documents for reference only.

Some groups include an `en/` directory with selected English versions. Translations support comprehension and terminology comparison; Vietnamese texts remain the preferred source when determining legal content.

## Usage principles

- This corpus is a raw source collection, not by itself a complete legal-validity registry.
- Do not infer validity solely from a filename, enactment year, or a document's presence in the corpus.
- Before citing a text, verify its number, issuing authority, effectiveness clause, amendments or replacement, and scope in the project's legal-status registry.
- Cite only the article, clause, or point directly applicable to the question; do not combine rules from different documents or time periods.
- Do not use material in `archived/` as the primary citation for current-law guidance.

## Catalogue and status checks

- [Source catalogue](../data/source_registry.csv): document numbers, issuing bodies, effective dates, source URLs, and verified status.
- [Legal-status registry](../data/law_status.json): the source used to check citations, expiry dates, and replacement documents.
- [Source-file audit](../data/rightly_source_file_audit.csv): metadata-to-source-file matching results within the project.
- [Project README](../README.md): Rightly's purpose, architecture, and operating guidance.
