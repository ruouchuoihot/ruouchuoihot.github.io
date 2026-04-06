---
title: "Web Investigation"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: medium
tags: [cyberdefenders, sql-injection, web-forensics, enumeration, webshell]
excerpt: "Phân tích chuỗi SQL injection, enum database và hành vi upload web shell trong challenge Web Investigation."
---

## Kịch bản (Scenario)

Kẻ tấn công lạm dụng một endpoint search bằng PHP đang dính lỗ hổng để enum backend database, mò thông tin các thư mục ẩn, đánh cắp credential và cuối cùng mớm một đoạn script PHP độc hại lên server.

Thực chất đây là một thước phim cô đọng minh hoạ quá trình bẻ khóa hệ thống web (full web compromise) từ A đến Z:

1. Dò ra lỗ hổng SQL injection.
2. Enum Schema và Table.
3. Cào thư mục ẩn.
4. Lạm dụng Crendential.
5. Ném Web shell.

## Những phát hiện chính (Key Findings)

- Attacker IP: `111.224.250.131`
- Origin city (Thành phố xuất phát): `Shijiazhuang` (Thạch Gia Trang)
- Nhắm vào script lỗi hổng: `search.php`
- Cú SQLi đầu tiên:
  `/search.php?search=book%20and%201=1;%20--%20-`
- Request dùng để enum dọn dẹp hệ cơ sở dữ liệu:
  `/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,schema_name)),0x7176706a71) FROM INFORMATION_SCHEMA.SCHEMATA-- -`
- Table chứa dữ liệu user của website: `customers`
- Thư mục ẩn bị attacker mò ra: `admin`
- Credential dùng để đăng nhập: `admin:admin123!`
- Malicious script được thảy lên: `NVri2vhp.php`

## Phân tích chuyên sâu (Analysis Walkthrough)

### 1. Chỉ mặt Attacker và Target

Từ ghi chú, xác định được IP của attacker:

- `111.224.250.131`

Check location của IP thì về thẳng:

- `Shijiazhuang`

![Traffic evidence showing the attacker's IP in the SQL injection activity](/assets/images/cyberdefenders/web-investigation/attacker-ip.png)

![AbuseIPDB-style lookup tying the source IP to Shijiazhuang](/assets/images/cyberdefenders/web-investigation/city-lookup.png)

### 2. Tìm trúng endpoint hớ hênh

File PHP có lỗ hổng:

- `search.php`

URI đầu tiên được sử dụng để khai thác:

- `/search.php?search=book%20and%201=1;%20--%20-`

### 3. Tái hiện giai đoạn Enumeration

Theo dõi các bước của attacker, ta phát hiện attacker enum schema database và xác định được bảng chứa thông tin user:

- `customers`

![Database enumeration through SQL injection against INFORMATION_SCHEMA](/assets/images/cyberdefenders/web-investigation/database-enum.png)

![Enumeration result exposing the customers table](/assets/images/cyberdefenders/web-investigation/customers-table.png)

### 4. Lần theo các vệt Post-Enumeration

Thư mục ẩn bị phát hiện:

- `admin`

Credential bị đánh cắp:

- `admin:admin123!`

![Captured admin credentials used to log in](/assets/images/cyberdefenders/web-investigation/admin-login-creds.png)

Malicious script được upload lên server:

- `NVri2vhp.php`

![Uploaded PHP web shell used for server-side control](/assets/images/cyberdefenders/web-investigation/web-shell-upload.png)

## Các gạch đầu dòng khi điều tra (Investigation Notes)

Case này là một ví dụ điển hình về Web Compromise Workflow:

1. Khai thác SQL injection để truy vấn database.
2. Enum table và column.
3. Brute force thư mục ẩn.
4. Sử dụng credential thu được để đăng nhập admin.
5. Upload web shell để duy trì quyền truy cập (persistence).

## Ma trận đáp án (Answer Matrix)

- Attacker IP: `111.224.250.131`
- City: `Shijiazhuang`
- Vulnerable script: `search.php`
- First SQLi URI: `/search.php?search=book%20and%201=1;%20--%20-`
- Database enumeration URI: `/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,schema_name)),0x7176706a71) FROM INFORMATION_SCHEMA.SCHEMATA-- -`
- User table: `customers`
- Hidden directory: `admin`
- Credentials: `admin:admin123!`
- Malicious script: `NVri2vhp.php`
