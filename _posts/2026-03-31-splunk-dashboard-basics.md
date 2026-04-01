---
title: "Splunk Dashboard Basics"
date: 2026-03-31
category: siem
tags: [splunk, dashboard, siem, blue-team]
excerpt: "Ghi chú ngắn gọn về dashboard framework trong Splunk và tại sao dashboard vẫn cứ là chân ái đối với quy trình workflow của Analyst."
---

Lượm lặt chút ít từ file ghi chú `Splunk Dashboard` cũ của tôi thì gom nhanh tóm gọn lại như thế này.

## Tại sao Dashboard vẫn nắm đằng cán ngọn?

Xin đính chính Dashboard không sinh ra để gạch tên chuyện Investigation (điều tra sâu), nhưng giá trị trị liên thành của nó nằm ở việc cài cắm những thứ sau:

- Summarize (gom gọn) luôn bộ mặt của tập dataset với tốc độ bạt xẹt.
- Trồi lên luôn các chỉ báo (anomalies) gai góc gọi mời click vô săm soi.
- Nắn dòng cho dân Analyst lướt lẹ ra cái trend mà không điên đầu hì hục gõ lại mớ SPL search bùng boong.
- Chi viện đắc lực cho các mặt trận view dập khuôn làm SOC hằng ngày cho khâu triage và report.

## Ghi tạc đôi chút Dashboard Framework Note

Ngẫm lại note gốc lòi ra vài gạch đầu dòng căn bản thôi:

- Đời không thiếu gì cách xào nấu visualizations với dashboard trong Splunk.
- Kiểu `Classic Splunk Dashboard` cổ lổ sỉ thì đổ cái rộp bằng mớ XML.
- Nhai XML làm dashboard thì cũng ngon, có điều cái layer giao diện (UI) bị còng tay hạn hẹp hơn ba cái chuẩn nhúng kéo thả sau này.

Nói cho vuông thì dù note này nó cỏn con nhưng thiết kế tồi một quả Dashboard thì coi như chặn họng cả lũ Analyst biến từ màn vọc visibility sang action tác chiến thực tiễn.

## Gút lại thì xây Dashboard cần lưu tâm điều gì?

Nếu sau rảnh rang kéo giãn cái chủ đề này bự lên nữa, tui sẽ rờ gáy mấy cái này:

- Thứ gì biến dashboard trở thành miếng võ có giá trị trong mắt ông cố SOC Analyst.
- Khi nào dùng Dashboard đắp vào và khi nào ốp luôn SPL chọc thẳng mạch máu.
- Design panel kiểu gì cho nó chống cự điều tra, bớt ảo mộng ba trò màu mè vanity metrics dỏm móc lỗ.
- Cấu trúc xích chó giữa Dashboard với Enterprise Security (ES), đám notable events lộn nhộn với mấy cái rạch ròi security domains.

Tạm thì cứ lưu note này đính một trạm thu phí mỏng trên hành trình tu luyện công lực cày Splunk.
