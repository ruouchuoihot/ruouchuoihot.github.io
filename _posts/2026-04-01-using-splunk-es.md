---
layout: post
title: "Using Splunk ES"
date: 2026-04-01
categories: [tools]
tags: [splunk]
---

## Risk Framework

![image](/assets/images/splunk/uses_1.png)

Risk notables (Sự kiện đáng chú ý dựa trên rủi ro):
- **ATT&CK Tactic Threshold Exceeded for Object Over Previous 7 days**: Notable này sẽ nổ khi số lượng kỹ thuật MITRE ATT&CK bị kích hoạt vượt quá 3 lần trong vòng 7 ngày.
- **Risk Threshold Exceeded for Object Over 24 Hour Period**: Notable sẽ nổ khi Risk Score (điểm rủi ro) vượt mốc 100 trong vòng 24 giờ.

![image](/assets/images/splunk/uses_2.png)

## Security Domain

Khung phân nhóm bảo mật (Security Domain) trong Splunk ES tập trung vào các luồng sự kiện chính:

**Access (Truy cập):** Các nỗ lực xác thực và sự kiện kiểm soát truy cập (login, access allowed, ...). Dashboard cung cấp công cụ để research sâu vào:
- Brute force (Dò mật khẩu)
- Privileged account (Tài khoản đặc quyền)
- Access by rare or new accounts (Truy cập từ tài khoản hiếm/mới)
- Access by expired or disabled accounts (Truy cập từ tài khoản đã hết hạn/bị vô hiệu)
- Access by unusual app (ssh, ...)

![image](/assets/images/splunk/uses_3.png)

**Endpoint:** Lây nhiễm mã độc, cấu hình hệ thống, trạng thái (CPU, port, uptime...), tình trạng bản vá và đồng bộ thời gian.

**Network:** Lưu lượng mạng, Firewall, Router, IDS/IPS, Host...

**Identity:** Thu thập và kiểm tra dữ liệu về danh tính và tài sản (asset).
