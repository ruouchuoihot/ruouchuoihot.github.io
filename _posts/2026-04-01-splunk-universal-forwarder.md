---
layout: post
title: "Splunk universal forwarder"
date: 2026-04-01
categories: [tools]
tags: [splunk]
---

## SPLUNK UNIVERSAL FORWARDER LINUX

**Splunk Universal Forwarder (UF)** là phương thức thu thập log dành cho các thiết bị được Splunk hỗ trợ như các máy **Windows**, **Linux**,...

- Thông thường, người dùng **không nên chạy Splunk UF dưới quyền root**, mà nên **tạo user riêng**, ví dụ: `splunkfwd`.
- Tuy nhiên, một số log cần quyền truy cập cao hơn, nên **cân nhắc kỹ trước khi cấu hình** Splunk UF phù hợp với hệ thống của bạn.
### Triển khai nhiều Splunk UF

- Khi có **nhiều Splunk UF** được cài đặt trên nhiều máy, bạn có thể sử dụng **Deployment Server** để:
---

### Cài đặt Splunk UF bằng file `.tgz`

1. **Tải gói cài đặt**
1. **Giải nén file **`.tgz`** vào **`/opt`
1. **Tạo user và phân quyền**
1. **Khởi động Splunk UF**
1. **Thiết lập chạy Splunk UF khi hệ điều hành khởi động**
---

### Cấu hình kết nối đến Deployment Server

Giả sử Heavy Forwarder tại Kafi làm **deployment server**, sử dụng port **8089 (management)**:

```shell
/opt/splunkforwarder/bin/splunk set deploy-poll <heavyforwarder.fqdn>:808
```

---

### Cấu hình đẩy log đến Heavy Forwarder

Giả sử Heavy Forwarder tại Kafi lắng nghe trên port **9997/TCP**:

```shell
/opt/splunkforwarder/bin/splunk add forward-server <heavyforwarder.fqdn>:999
```

---

### Khởi động lại Splunk UF

```shell
/opt/splunkforwarder/bin/splunk restart
```

---

### Kiểm tra kết nối

Truy cập Splunk Web tại Heavy Forwarder:

- Vào: `Settings → Forwarder Management`
- Kiểm tra xem **agent vừa cài đặt** đã hiển thị trong danh sách chưa.
## SPLUNK UNIVERSAL FORWARDER WINDOWS

Bước 1: Chọn Check this box to accept the License Agreement và chọn An on-premises Splunk Enterprise instances.
Bước 2: Chọn Customize Options để kiểm tra các cấu hình bao gồm:

- Đường dẫn thư mục sẽ chứa Splunk UF: C:\Program Files\SplunkUniversalForwarder\
- Cấu hình SSL certificate: Splunk UF sử dụng SSL certificate để mã hoá data trước khi gửi đến Receiver. Theo mặc định sẽ sử dụng selft-signed cert của Splunk.
![image](/assets/images/splunk/20dbc35f-72fd-802c-8a3e-d6557d041739.png)

- Chọn user context để chạy process Splunk UF: bao gồm 3 lựa chọn là Local System, Domain Account và Virtual Account.
• Local System: Splunk UF chạy dưới quyền Administrator với đầy đủ đặc quyền.
• Domain Account: Splunk UF chạy dưới quyền của domain account được cấu hình.
• Virtual Account: Splunk UF sử dụng một virtual account là splunkfwd có đặc quyền truy cập ít nhất, chỉ cung cấp các khả năng
cần thiết để chạy tiến trình.
- Cấu hình các đặc quyền cho phép Splunk UF thu thập các loại log:
• SeBackupPrivilege: cấp quyền ĐỌC (không phải VIẾT) cho người dùng có đặc quyền thấp nhất đối với các tệp
• SeSecurityPrivilege: cho phép user ảo thu thập Windows Event Logs
• SeImpersonatePrivilege: kiểm tra để kích hoạt khả năng thêm user có đặc quyền tối thiểu sau khi cài Splunk UF.
• Performance Monitor Users: Kiểm tra đầu vào WMI/perfmon để thu thập dữ liệu về performance.
![image](/assets/images/splunk/20dbc35f-72fd-801c-b9d6-d58ef81abba8.png)

- Cấu hình các loại log sẽ thu thập: phần này có thể bỏ trống và cấu hình trên file inputs.conf sau.
- Tạo tài khoản admin cho Splunk UF: nhập username và password.
![image](/assets/images/splunk/20dbc35f-72fd-806d-8aa2-f8cb469d3722.png)

Bước 3: Cấu hình Deployment Server
Bước 4: Cấu hình Receiver Indexer (nơi log được gửi đến)

![image](/assets/images/splunk/20dbc35f-72fd-8009-9dda-f6b3fa6dd48f.png)

## Cấu hình Avanced Audit Policy Configuration cho Windows

Theo mặc định, Windows Event Logs không ghi nhật ký toàn bộ các sự kiện trên Windows mà cần phải cấu hình cho phép ghi thêm các sự kiện khác. Để cấu hình, cần truy cập vào Local Security Policy, trong phần Advanced Audit Policy Configuration, turn on các sự kiện muốn ghi nhật ký.

![image](/assets/images/splunk/20dbc35f-72fd-80be-bece-dbd115a0e4f7.png)

## Cài đặt Sysmon

Truy cập vào trang chính thức của Microsoft để tải gói cài đặt Sysmon.
Theo mặc định, Sysmon sẽ thu thập toàn bộ log nhưng điều này có thể dẫn đến một khối lượng log khổng lồ, do đó để giảm thiểu khối lượng mà đảm bảo việc các sự kiện liên quan đến bảo mật không bị bỏ qua, cần sử dụng một file config .xml để exclude các trường hợp có thể coi là false positives. Splunk khuyến nghị sử dụng file .xml [Github ](https://github.com/SwiftOnSecurity/sysmon-config/blob/master/sysmonconfig-export.xml)sau như một điểm khởi đầu cho các tuning Sysmon logging về sau. Sau khi có file Sysmon.xml, chạy command sau để cài đặt:

```powershell
Sysmon.exe -i Sysmon.xml -accepteula.
```

## Cấu hình PowerShell và Command Line logging

PowerShell hỗ trợ các loại log như sau:

- Module Logging: ghi lại chi tiết pipeline execution dưới dạng sự kiện, đặc biệt tập trung vào các mô-đun. Tính năng này ghi lại thông
tin chi tiết về các command từ các mô-đun PowerShell cụ thể.
- Script Block Logging: ghi lại nội dung của tất cả các script block được xử lý bởi công cụ PowerShell.
- Transcription: ghi lại input và output của PowerShell session cũng như các thông báo lỗi.
Để cấu hình cho phép Windows ghi các loại PowerShell log như trên và Command Line log, cần cấu hình GPO trên Windows Active Directory hoặc thay đổi trực tiếp trên registry. File enable_logging.ps1 được tạo để tự động thực hiện việc thay đổi GPO phục vụ cho việc logging PowerShell và Command Line được xây dựng theo tài liệu của Microsoft và Splunk.
Scipts này cũng bao gồm việc chỉ cấp quyền truy cập thư mục C:\pstrans (nơi lưu trữ log PowerShell) cho user System và Administrators.
## Cài đặt các Add-on cần thiết

Các Add-on cần thiết bao gồm:

- Splunk Add-on for Microsoft Windows: [https://splunkbase.splunk.com/app/742](https://splunkbase.splunk.com/app/742)
- Splunk Add-on for Sysmon: [https://splunkbase.splunk.com/app/5709](https://splunkbase.splunk.com/app/5709)
- Splunk Add-on for Microsoft Security: [https://splunkbase.splunk.com/app/6207](https://splunkbase.splunk.com/app/6207)
Sau khi tải xuống, extract các file zip và đưa các thư mục này vào folder C:\Program Files\SplunkUniversalForwarder\etc\apps

![image](/assets/images/splunk/20dbc35f-72fd-8098-b450-cd58804c4613.png)

## Cấu hình thu thập Sysmon logs trên Splunk UF

Tạo file C:\Program Files\SplunkUniversalForwarder\etc\system\local\inputs.conf và thêm các dòng sau:

![image](/assets/images/splunk/20dbc35f-72fd-80aa-bc22-ca3c09dbe8db.png)

## Cấu hình thu thập Windows Event Logs trên Splunk UF

Sao chép file C:\Program Files\SplunkUniversalForwarder\etc\apps\Splunk_TA_windows\default\inputs.conf vào thư mục C:\ProgramFiles\SplunkUniversalForwarder\etc\apps\Splunk_TA_windows\local, sau đó đổi disabled = 0

