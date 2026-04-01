---
layout: post
title: "Elements of a Proper Incident Report"
date: 2026-04-01
categories: [dfir-knowledge]
---

## Executive Summary

Executive Summary là phần đầu tiên của report, hướng tới nhiều nhóm người đọc khác nhau, kể cả stakeholder không có nền tảng kỹ thuật. Phần này cần đưa cho người đọc:

- bức tranh tổng quan ngắn gọn,
- các key findings,
- các hành động đã thực hiện ngay sau khi phát hiện,
- và mức độ ảnh hưởng tới stakeholder.
Vì nhiều stakeholder chỉ đọc Executive Summary, nên phần này phải được viết rõ ràng và đầy đủ nhất có thể. Dưới đây là các nội dung chính nên có trong Executive Summary:

## Technical Analysis

Phần này dùng để mô tả chi tiết về mặt kỹ thuật mọi việc đã diễn ra trong incident. Đây thường là phần dài nhất trong incident report. Các ý chính cần có gồm:

### Affected Systems & Data

Liệt kê tất cả hệ thống và data có khả năng bị truy cập hoặc chắc chắn đã bị compromise trong incident.

Nếu có data bị exfiltrated và xác định được con số, cố gắng nêu rõ dung lượng hoặc số lượng record bị ảnh hưởng.

### Evidence Sources & Analysis

Nêu rõ các nguồn evidence đã được xem xét, kết quả thu được và cách phân tích.

Ví dụ: nếu việc compromise được xác nhận từ web access log, nên đính kèm screenshot để làm tài liệu.

Cần đảm bảo evidence được giữ nguyên, đặc biệt nếu incident có khả năng liên quan đến điều tra hình sự. Thực hành tốt là hash file để có thể kiểm tra integrity về sau.

### Indicators of Compromise (IoCs)

IoC là thành phần quan trọng để hunting dấu hiệu compromise trong toàn bộ environment, hoặc thậm chí chia sẻ cho partner.

Dựa vào IoC, đôi khi có thể liên kết incident với một threat group cụ thể.

IoC có thể bao gồm:

- outbound traffic bất thường,
- process lạ đang chạy,
- scheduled task do attacker tạo ra,
### Root Cause Analysis

Mô tả phần phân tích root cause đã thực hiện và giải thích nguyên nhân gốc của security incident.

Trong đó cần chỉ rõ:

- lỗ hổng nào bị exploit,
- điểm nào trong hệ thống hoặc quy trình bị lỗi,
- vì sao attacker có thể thành công.
### Technical Timeline

Đây là phần rất quan trọng để hiểu được trình tự diễn biến của incident.

Timeline nên bao gồm các mốc chính như:

- Reconnaissance
- Initial Compromise
- C2 Communications
- Enumeration
- Lateral Movement
- Data Access & Exfiltration
- Malware Deployment or Activity (bao gồm Process Injection và Persistence)
- Containment times
- Eradication times
- Recovery times
Nhờ timeline, người đọc có thể thấy rõ chuyện gì xảy ra trước, sau, và mức độ phản ứng nhanh hay chậm.

### Nature of the Attack

Mô tả chi tiết loại attack và các tactics, techniques, procedures (TTPs) mà attacker đã sử dụng.

Phần này giúp kết nối incident với các pattern tấn công đã biết và hỗ trợ cho việc phòng thủ, detection và hunting về sau.

## **Impact Analysis**

Phần này dùng để đánh giá các tác động tiêu cực của incident lên data, hoạt động vận hành và uy tín của tổ chức. Mục tiêu là xác định và mô tả mức độ thiệt hại, bao gồm hệ thống, quy trình hoặc tập dữ liệu nào đã bị compromise.

Impact analysis cũng xem xét các hệ quả về mặt business, như: khả năng mất mát tài chính, nguy cơ bị xử phạt bởi cơ quan quản lý và mức độ ảnh hưởng tới hình ảnh, danh tiếng của tổ chức.

## Response and Recovery Analysis

Phần này mô tả cụ thể những gì đã làm để khống chế incident, xoá bỏ mối đe doạ và đưa hệ thống hoạt động bình thường trở lại. Nội dung nên theo trình tự thời gian, thể hiện rõ cách tổ chức giảm thiểu tác động và ngăn sự cố tương tự lặp lại.

Dưới đây là các phần thường có trong mục **Response and Recovery**:

---

### Immediate Response Actions

Revocation of Access

- **Identification of Compromised Accounts/Systems: **Mô tả chi tiết cách phát hiện tài khoản hoặc hệ thống bị compromise, kèm theo tool và phương pháp đã dùng.
- **Timeframe: **Nêu rõ thời điểm phát hiện truy cập trái phép và thời điểm thu hồi quyền truy cập, tốt nhất chính xác đến từng phút.
- **Method of Revocation: **Giải thích cách thực hiện về mặt kỹ thuật, ví dụ: disable tài khoản, thay đổi permission, chỉnh sửa rule trên firewall.
- **Impact: **Đánh giá việc thu hồi quyền truy cập ngay lập tức đã giúp đạt được điều gì, chẳng hạn như ngăn data bị exfiltrate thêm hoặc tránh hệ thống tiếp tục bị compromise.
---

Containment Strategy

- **Short-term Containment: **Các hành động nhanh để cô lập hệ thống bị ảnh hưởng khỏi network, tránh threat actor di chuyển sang hệ thống khác.
- **Long-term Containment: **Các biện pháp mang tính chiến lược hơn, ví dụ network segmentation hoặc triển khai mô hình zero trust để cô lập lâu dài các khu vực rủi ro.
- **Effectiveness: **Đánh giá mức độ hiệu quả của các biện pháp containment trong việc giới hạn phạm vi và tác động của incident.
---

### Eradication Measures

Malware Removal

- **Identification: **Quy trình phát hiện malware hoặc mã độc, bao gồm việc dùng EDR, phân tích forensic hoặc các kỹ thuật khác.
- **Removal Techniques: **Nêu rõ tool hoặc cách làm (tự động hoặc thủ công) để xoá bỏ malware.
- **Verification: **Các bước đảm bảo malware đã được xoá sạch, ví dụ kiểm tra checksum, dùng phân tích heuristic hoặc scan lại hệ thống.
System Patching

- **Vulnerability Identification: **Cách phát hiện ra lỗ hổng, và nếu có, ghi rõ các CVE liên quan.
- **Patch Management: **Mô tả quá trình triển khai patch: kiểm thử, rollout, và xác nhận patch đã áp dụng thành công.
- **Fallback Procedures: **Các bước rollback trong trường hợp patch gây lỗi hoặc làm hệ thống hoạt động không ổn định.
---

### Recovery Steps

Data Restoration

- **Backup Validation: **Cách kiểm tra backup trước khi restore để đảm bảo backup không lỗi hoặc không chứa mã độc.
- **Restoration Process: **Từng bước restore data, bao gồm cả việc giải mã nếu dữ liệu bị mã hoá.
- **Data Integrity Checks: **Cách kiểm tra tính toàn vẹn của dữ liệu sau khi restore.
System Validation

- **Security Measures: **Những việc đã làm để đảm bảo hệ thống đủ an toàn trước khi đưa vào vận hành lại, như cấu hình lại firewall, cập nhật IDS.
- **Operational Checks: **Các kiểm tra đảm bảo hệ thống hoạt động ổn định và đáp ứng yêu cầu trong môi trường production.
---

### Post-Incident Actions

Monitoring

- **Enhanced Monitoring Plans: **Kế hoạch tăng cường monitoring để phát hiện sớm các lỗ hổng tương tự hoặc pattern tấn công liên quan trong tương lai.
- **Tools and Technologies: **Những monitoring tool sẽ dùng, cách chúng được tích hợp với hệ thống hiện tại để có cái nhìn tổng thể.
### Lessons Learned

- **Gap Analysis: **Đánh giá các điểm yếu trong security controls hoặc quy trình, lý do chúng không phát huy hiệu quả.
- **Recommendations for Improvement: **Đề xuất các thay đổi cụ thể, có mức độ ưu tiên và timeline triển khai rõ ràng.
- **Future Strategy: **Các điều chỉnh dài hạn về policy, kiến trúc hệ thống hoặc đào tạo nhân sự nhằm giảm khả năng xảy ra incident tương tự.
## Diagrams

![image](/assets/images/dfir/31fbc35f-72fd-81e8-9868-fd272d4e6a0e.png)

- Incident Flowchart: Dùng flowchart để thể hiện tiến trình của attack, từ entry point ban đầu cho đến khi nó lan ra trong toàn bộ network.
- Affected Systems Map: Có thể dùng màu sắc hoặc ghi chú để thể hiện mức độ nghiêm trọng của từng trường hợp compromise.
- Attack Vector Diagram: Dùng mũi tên, node và ghi chú để thể hiện trực quan cách attacker di chuyển và các hoạt động exploit/post-exploitation khi đi xuyên qua defense.
Ví dụ, một diagram có thể thể hiện các attack vector như: phishing, vulnerability exploits, insider threat và open ports dẫn tới các điểm yếu trên endpoints và servers.

## Appendices

