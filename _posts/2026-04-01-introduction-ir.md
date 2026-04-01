---
layout: post
title: "Introduction (Incident Reporting)"
date: 2026-04-01
categories: [dfir]
tags: [dfir]
---

## Introduction to Security Incident Reporting

Trong bối cảnh hiện nay, chuyện xảy ra security incident gần như là chắc chắn. Câu hỏi chính là nó sẽ xảy ra lúc nào. 

Công nghệ giúp tăng hiệu quả làm việc, mang lại doanh thu và sản lượng tốt hơn. Nhưng đi cùng với đó là rủi ro bảo mật cũng tăng. Các hệ thống này trở thành mục tiêu tấn công của nhiều nhóm khác nhau, bao gồm cả nhóm được nhà nước tài trợ và nhóm độc lập. Vì vậy, một cơ chế Security incident reporting rõ ràng và thống nhất là rất quan trọng để tổ chức sẵn sàng đối phó với các mối đe doạ.

Security incident reporting kết nối giai đoạn phát hiện sự cố với giai đoạn xử lý. Nó giúp lưu lại các incident đã xảy ra, rút kinh nghiệm từ các sai sót trước đó. Thông tin này có thể đưa vào kế hoạch phòng ngừa và giảm thiểu rủi ro trong tương lai. Với một môi trường đe doạ thay đổi liên tục, một incident reporting framework đầy đủ và được áp dụng nhất quán là điều cần thiết để tổ chức và nhân viên không bị động khi có sự cố.

Ngoài việc hỗ trợ xử lý kỹ thuật, một reporting process rõ ràng còn phục vụ các nhu cầu nội bộ khác. Bộ phận pháp chế dùng incident report để kiểm tra tuân thủ quy định. Ban lãnh đạo dùng nó để đánh giá rủi ro. CFO dựa vào đó để xem xét tác động tài chính. Một incident report được viết mạch lạc sẽ giúp tất cả các bên liên quan nắm được tình hình chung.

Incident report hiệu quả cần đủ chi tiết nhưng vẫn dễ đọc. Người có nền tảng kỹ thuật và người không chuyên đều cần hiểu được nội dung chính. Mục tiêu của module này là giúp bạn nắm rõ những điểm quan trọng khi thực hiện incident reporting.

---

## Incident Identification and Categorisation

Có rất nhiều loại cyber security threat có thể ảnh hưởng tới cá nhân hoặc tổ chức. Vì vậy, cần một cách làm có hệ thống để nhận diện và phân loại security incident. Làm tốt phần này giúp phân bổ nguồn lực nhanh hơn và xử lý sự cố kịp thời. Nói ngắn gọn, phản ứng ban đầu có hiệu quả hay không phụ thuộc nhiều vào việc bạn có nhận ra và phân loại được incident đủ nhanh hay không.

### Identifying Security Incidents

Security incident có thể xuất phát từ nhiều nguồn khác nhau. Thường nó được thấy dưới dạng cảnh báo, dấu hiệu bất thường hoặc các thay đổi so với baseline của hệ thống. Ba nhóm nguồn chính thường gặp là:

### Categorising Security Incidents

Khi đã xác định có incident, bước tiếp theo là phân loại. Việc phân loại hỗ trợ:

- Ưu tiên thứ tự xử lý.
- Phân công đúng team và đúng nguồn lực.
- Truyền đạt và báo cáo lại cho stakeholder một cách rõ ràng.
**Ví dụ về loại incident:**

- **Malware**: Phần mềm độc hại như virus, worm, ransomware.
- **Phishing**: Hành vi lừa đảo để lấy thông tin nhạy cảm, chủ yếu qua email.
- **DDoS Attacks**: Cố ý gửi lượng lớn traffic để làm gián đoạn hoặc ngừng hoạt động hệ thống, dịch vụ hoặc mạng.
- **Unauthorised Access**: Đối tượng không được cấp quyền nhưng vẫn truy cập được hệ thống hoặc dữ liệu.
- **Data Leakage**: Dữ liệu mật bị lộ ra ngoài, có thể trong nội bộ hoặc ra ngoài tổ chức.
- **Physical Breach**: Truy cập trái phép vào khu vực vật lý được bảo vệ, ví dụ phòng server.
**Incident Severity Levels:**

- **Critical (P1)**: Đe doạ trực tiếp tới chức năng kinh doanh quan trọng hoặc dữ liệu nhạy cảm. Cần xử lý ngay.
- **High (P2)**: Có rủi ro đáng kể với hoạt động kinh doanh nhưng chưa gây gián đoạn tức thì. Cần ưu tiên xử lý.
- **Medium (P3)**: Chưa gây ảnh hưởng trực tiếp ngay lập tức tới hoạt động kinh doanh, nhưng vẫn cần xử lý trong thời gian hợp lý.
- **Low (P4)**: Sự cố mức thấp hoặc các bất thường có thể xử lý trong quy trình vận hành thông thường.
Trong thực tế, một incident có thể thuộc nhiều nhóm khác nhau. Mức độ nghiêm trọng cũng có thể thay đổi khi có thêm thông tin trong quá trình phân tích. Vì vậy, cách tiếp cận cần vừa có cấu trúc rõ ràng, vừa đủ linh hoạt để điều chỉnh khi hiểu rõ hơn về incident.

