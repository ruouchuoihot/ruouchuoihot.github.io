---
layout: post
title: "Splunk Security Essentials (SSE)"
date: 2026-04-01
categories: [tools]
tags: [splunk]
---

## SSE là gì?

Splunk Security Essentials (SSE) là một ứng dụng của Splunk, đóng vai trò như một kho tàng "chính hãng" chứa các quy tắc phát hiện bảo mật (security detections) và gợi ý đưa dữ liệu vào hệ thống (data onboarding recommendations). 

SSE đóng vai trò như chiếc la bàn để doanh nghiệp biết mình đang đi đúng hướng trên hành trình bảo mật hay không. Nó là một bách khoa toàn thư cho Splunk Cloud, Splunk Enterprise Security, SOAR và User Behavior Analytics (UBA). Ngoài ra, SSE còn đưa ra các khuyến nghị vá lỗ hổng, bổ sung context cho các event, và tự động mapping dữ liệu/luồng phát hiện vào các framework chuẩn ngành như MITRE ATT&CK hay Cyber Kill Chain.

## The Security Data Journey

SSE định hình một lộ trình bảo mật (Security Roadmap). Từng chặng (stage) sẽ có các yêu cầu khác nhau, từ việc thu thập data cơ bản ở Stage 1 cho đến dùng Machine Learning phức tạp ở Stage 6.

Với các content tương ứng cho từng stage, tổ chức có thể đo lường mức độ trưởng thành của hệ thống Splunk và tập trung vào những thứ vừa sức.

![image](/assets/images/splunk/sse_1.png)

Nếu anh em bấm vào một Stage bất kỳ trong **Security Data Journey**, hệ thống sẽ sổ ra mô tả chi tiết: cột mốc, khó khăn, và các Use Case phù hợp nhất. Khi cuộn xuống cuối màn hình, hệ thống sẽ chốt hạ những "Data Source" nào bắt buộc phải có cho Stage này.

![image](/assets/images/splunk/sse_2.png)

## Security Content

Đây là thư viện tổng hợp các Use Case liên quan đến Splunk Cloud, Splunk SIEM & SOAR để tăng cường sức mạnh điều tra (investigations). SSE chứa hơn 1000 Use Cases và thậm chí còn tự gợi ý Use Case dựa trên những dữ liệu anh em đang có sẵn. Lưu ý: anh em cần làm "Gap assessment" cẩn thận để đảm bảo hệ thống đang nhận đủ và đúng nguồn log trước khi triển khai một Use Case nào đó.

![image](/assets/images/splunk/sse_3.png)

**Cách tìm kiếm:** Mở SSE Home, chọn **Find Content**.
![image](/assets/images/splunk/sse_4.png)

Chọn loại Content (VD: **Security Detection Basics** -> **Security Monitoring**).
![image](/assets/images/splunk/sse_5.png)

Hệ thống sẽ filter từ 1398 content xuống còn 13 content đặc thù cho Security Monitoring ở Stage 1. Mọi thứ trở nên cực kỳ tinh gọn để nghiên cứu sâu.
![image](/assets/images/splunk/sse_6.png)

Anh em hoàn toàn có thể tìm theo **Keywords** (VD: gõ *endpoint* để tìm đúng 1 Use Case cần thiết).
![image](/assets/images/splunk/sse_7.png)

Filter theo **Journey** (lọc từ Stage 1-3).
![image](/assets/images/splunk/sse_8.png)

Filter theo **Category** (VD: chọn *Account Compromise* hoặc *Cloud Security*).
![image](/assets/images/splunk/sse_9.png)

Filter theo **Data Source** (rất quan trọng để lọc theo log AWS hay Authentication).
![image](/assets/images/splunk/sse_10.png)

Filter theo **Featured** (chỉ lấy những Use Case xịn xò do chính các chuyên gia Splunk khuyên dùng).
![image](/assets/images/splunk/sse_11.png)

Tất cả các bộ filter này đều có thể Edit và lưu lại tùy ý.
![image](/assets/images/splunk/sse_12.png)

## Bookmarking Security Content

Bookmark cực kỳ hữu dụng để đánh dấu quy trình điều tra hoặc đưa vào danh sách chờ triển khai.
![image](/assets/images/splunk/sse_13.png)

## Overview Dashboard

Dashboard này phủ trọn bức tranh dữ liệu đang được cấu hình. Anh em dùng nó để soi số lượng Data Sources, đếm đống Use Cases, hoặc nhìn xem log của mình đang map vào MITRE ATT&CK tactics ở mức độ nào. Tick vào ô **Only Bookmarked** để thu hẹp tầm nhìn.
![image](/assets/images/splunk/sse_14.png)

Sơ đồ **Data Source > Splunk App** biểu diễn mối quan hệ giữa dòng chảy dữ liệu bên trái và đích đến bên phải.
![image](/assets/images/splunk/sse_15.png)

Bảng mapping tổng thể từ Data Journey sang Apps và Use Cases.
![image](/assets/images/splunk/sse_16.png)

## Browsing Content by Framework

Giao diện để duyệt qua toàn bộ ma trận Security Content.
![image](/assets/images/splunk/sse_17.png)
