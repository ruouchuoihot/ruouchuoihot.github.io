---
layout: post
title: "The Incident Reporting Process"
date: 2026-04-01
categories: [dfir-knowledge]
---

## The Incident Reporting Process

Quy trình reporting là 1 khung gắn tất cả các phần việc liên quan đến security incident reporting lại với nhau. Nếu cơ chế reporting được thiết kế tốt, nó không chỉ giúp mọi người nhìn rõ hướng xử lý, mà còn tạo ra thông tin có thể dùng ngay để hành động. Phần này đi qua từng bước cần có trong quy trình đó.

---

### 1. Initial Detection & Acknowledgement

Trước khi một incident được báo cáo chính thức, nó phải được phát hiện và phải có người xác nhận đó là sự cố cần xử lý.

Nguồn phát hiện (detection vector) có thể khác nhau, ví dụ:

- Nhân viên hoặc người dùng tự nhận thấy dấu hiệu bất thường.
- Alert tự động do security tools trong hệ thống tạo ra.
- Đôi khi chính threat actor tạo ra tín hiệu rõ ràng, nhất là trong các vụ ransomware khi màn hình hiện thông báo đòi tiền chuộc.
---

### 2. Preliminary Analysis

Ở bước này, cần xác định phạm vi và hậu quả tiềm ẩn của security incident.

Dựa trên thông tin có được, incident được xếp loại theo hệ thống classification và mức độ severity đã thống nhất từ trước.

---

### 3. Incident Logging

Tất cả chi tiết, hành động và quan sát liên quan đến security incident cần được ghi lại đầy đủ trong một hệ thống dùng chung.

Một số nền tảng hay dùng cho mục đích này là **JIRA** và **TheHive Project**.

Nếu tổ chức chưa có hệ thống tương tự, có thể dùng giải pháp đơn giản hơn. Ngay cả việc ghi chép bằng bút giấy hoặc một file **spreadsheet** cũng tốt hơn là không log gì.

---

### 4. Notification of Relevant Parties

Cần nhanh chóng xác định stakeholder liên quan và chia việc thông báo thành hai nhóm chính.

### Internal Communications

Các bộ phận nội bộ liên quan như IT, legal, PR và executive team cần được thông báo.

Nếu incident có mức độ nghiêm trọng cao và ảnh hưởng rộng, có thể cần gửi thông báo tới toàn bộ tổ chức.

### External Communications

Tuỳ vào tính chất và mức độ ảnh hưởng của incident, có thể phải truyền thông ra bên ngoài.

Những đối tượng có thể cần được thông báo gồm:

- Khách hàng.
- Partner, vendor.
- Regulatory bodies.
- Thậm chí là công chúng nói chung.
---

### 5. Detailed Investigation & Reporting

Thời gian cho giai đoạn này có thể rất khác nhau: có vụ chỉ kéo dài vài ngày, nhưng cũng có vụ phải điều tra nhiều tháng, thậm chí lâu hơn.

Điểm quan trọng là phải có:

- Phân tích kỹ thuật chi tiết.
- Tổng hợp đầy đủ tất cả kết quả và phát hiện liên quan.
Cuộc điều tra chuyên sâu này là cơ sở để hiểu hết mức độ tác động của incident lên tổ chức.

---

### 6. Final Report Creation

Phần kết của công việc security analyst hoặc incident responder là tạo ra **final incident report**.

Tài liệu này cung cấp cho:

- Regulator.
- Insurer.
- Executive leadership.
một bức tranh chi tiết về:

- Incident đã xảy ra như thế nào.
- Nguồn gốc, nguyên nhân.
- Các remedial actions đã thực hiện.
---

### 7. Feedback Loop!

Sau khi xử lý xong incident, cần có bước nhìn lại để chuẩn bị tốt hơn cho những incident sau.

Việc này bao gồm:

- Xem lại toàn bộ diễn biến incident.
- Phân tích quy trình xử lý.
- Chỉ ra chỗ nào còn thiếu, yếu hoặc cần cải thiện.
---

## Conclusion

Quy trình reporting không phải chỉ là một thủ tục cho đủ quy trình. Nó là một tài sản mang tính chiến lược, giúp tổ chức tăng khả năng chống chịu trước security threat.

Nhờ việc ghi chép chặt chẽ, phân tích kỹ và rút kinh nghiệm sau mỗi incident, tổ chức có thể biến các sự cố thành cơ hội để củng cố security stance của mình.

