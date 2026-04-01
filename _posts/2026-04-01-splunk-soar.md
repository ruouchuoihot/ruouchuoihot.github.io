---
layout: post
title: "Splunk SOAR"
date: 2026-04-01
categories: [tools]
tags: [splunk]
---

## Splunk SOAR là gì?

![image](/assets/images/splunk/soar_1.png)

Splunk SOAR kéo dữ liệu từ các hệ thống khác như Splunk Enterprise Security (ES) hay Search Head (SH) để giám sát các luồng network nhằm phát hiện:
- Security incidents: Các lỗ hổng, hành vi truy cập trái phép, hoặc mã độc.
- Vulnerabilities: Các điểm yếu cấu hình có khả năng leo thang thành incident.

Dữ liệu đưa vào Splunk SOAR sẽ được lưu trữ dưới dạng Database chuyên dụng và hiển thị lên thành các Event. 

Mục tiêu cốt lõi của SOAR là giúp anh em phân tích chuyên sâu vào từng event để hoạch định phương án ứng phó (Response Plan) một cách rõ ràng:
- Máy trạm (endpoint) hay server nào đang bị ảnh hưởng?
- Bản chất của mối đe dọa (threat) là gì?
- Mối đe dọa này xuất phát từ đâu?
- Mức độ nghiêm trọng (severity) ra sao?

Từ những phân tích này, hệ thống sẽ đưa ra các quyết định hành động (Response decision).

![image](/assets/images/splunk/soar_2.png)

Sau khi chốt phương án, SOAR sẽ bắt đầu tự động hoá các luồng "Take action" (như Kill process, xóa file độc hại, hoặc cô lập host...).

![image](/assets/images/splunk/soar_3.png)
