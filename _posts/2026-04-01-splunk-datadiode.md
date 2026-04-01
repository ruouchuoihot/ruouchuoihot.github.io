---
layout: post
title: "Splunk datadiode"
date: 2026-04-01
categories: [tools]
tags: [splunk]
---

# 🛡️ Sơ lược về Data Diode

## 📌 Data Diode là gì?

**Data Diode** là một giải pháp an ninh mạng đảm bảo trao đổi thông tin **một chiều**. Có thể hiểu đơn giản, **Data Diode** tạo ra một luồng mạng chỉ cho phép dữ liệu đi **từ mạng nguồn sang mạng đích**, nhưng **không cho chiều ngược lại**.

Việc này giúp:

- Đảm bảo **tính toàn vẹn** của hệ thống bằng cách ngăn chặn xâm nhập.
- Bảo vệ **thông tin nhạy cảm**, đặc biệt trong môi trường phân tách mạng tin cậy/không tin cậy (Trust/Untrust).
![image](/assets/images/splunk/20dbc35f-72fd-80c7-9ad0-fc83ec18a46c.png)

---

## ⚙️ Cơ chế hoạt động của Data Diode

**Owl Data Diode** là một thiết bị phần cứng gồm:

- **Hai đầu riêng biệt**: một đầu **chỉ gửi**, một đầu **chỉ nhận**.
- Điều này khiến cho dữ liệu **chỉ có thể truyền một chiều**, khiến việc tấn công từ xa gần như **bất khả thi**.
### 🎯 Vấn đề giao tiếp hai chiều

Do các giao thức như TCP yêu cầu bắt tay hai chiều, Owl sử dụng cơ chế:

- **Proxy gửi (Sender Proxy)**: tương tác với mạng nguồn.
- **Proxy nhận (Receiver Proxy)**: tương tác với mạng đích.
- Data diode sẽ chuyển đổi các giao thức **hai chiều thành một chiều**, giúp quá trình giao tiếp liền mạch.
---

# 🧩 Data Diode trong môi trường Splunk Cluster

## 📍 Tổng quan triển khai

Trong môi trường **Splunk Cluster**, Data Diode cũng được triển khai để truyền tải dữ liệu một chiều từ:

- **Mạng tin cậy (High Security Site)** đến
- **Mạng không tin cậy (Low Security Site)**
![image](/assets/images/splunk/20dbc35f-72fd-8067-b7f1-c7129b42d5c1.png)

Bằng cách sử dụng Data Diode Add-on, Add-on ở phía Heavy Forwarder sender sẽ add them các trường metadata trong event và sau đó được gửi đến data diode, data diode lúc này sẽ gửi data đến receiver add-on và add-on sẽ gỡ bỏ những trường data này để hoàn trả các log về ban đầu.

![image](/assets/images/splunk/20dbc35f-72fd-80df-a0ef-fe4d4d8d7247.png)

### ✅ Add-on sử dụng:

- **Owl Diode Sender Add-on** (trên máy gửi)
- **Owl Diode Receiver Add-on** (trên máy nhận)
---

## 🧱 Chi tiết cấu hình

### 🟩 Owl Diode Sender Add-on

- Cài đặt trên **Heavy Forwarder Sender**
- Trích xuất metadata như: `source`, `sourcetype`, `host`, `_time`, `index`, ...
- Sử dụng:
**Cách cấu hình:**

```plain text
# outputs.conf
[indexAndForward]
disabled = false
index = false

[tcpout:diode-syslog-udp]
server = 10.11.13.60:7500
```

```plain text
# props.conf
[<sourcetype>]
TRANSFORMS-diode-2 = send-to-syslog-udp
```

---

### 🟦 Owl Diode Receiver Add-on

- Cài đặt trên **Heavy Forwarder Receiver**
- Nhận dữ liệu, gỡ header metadata → khôi phục log về trạng thái ban đầu
- Sử dụng:
**Cách cấu hình:**

```plain text
# inputs.conf
[udp://7500]
sourcetype = diode-syslog

# hoặc với TCP
[tcp://7500]
sourcetype = diode-syslog
```

```plain text
# transforms.conf
[extract_metadata]
REGEX = ...
FORMAT = ...

[rewrite_raw]
REGEX = ...
FORMAT = ...
```

---

## 🏗️ Mô hình triển khai

---

## 🔄 Cấu hình đẩy dữ liệu từ HF Receiver đến Indexer

```plain text
# outputs.conf tại Heavy Forwarder Receiver
[tcpout:indexers]
server = indexer1:9997, indexer2:9997
indexAndForward = false
```

---

## 📊 Kiểm tra dữ liệu trên Indexer

- Vào **Splunk Web**
- Truy cập `Settings → Indexes`
- Kiểm tra logs được gửi lên có khớp với dữ liệu gốc không.
