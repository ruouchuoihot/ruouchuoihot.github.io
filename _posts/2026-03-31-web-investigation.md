---
title: "Web Investigation"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: medium
tags: [cyberdefenders, sql-injection, web-forensics, enumeration, webshell]
excerpt: "Phân tích chuỗi SQL injection, enum dataabase và hành vi upload web shell trong challenge Web Investigation."
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
- Credential dùng để log in hốt ổ: `admin:admin123!`
- Malicious script được thảy lên: `NVri2vhp.php`

## Phân tích chuyên sâu (Analysis Walkthrough)

### 1. Chỉ mặt Attacker và Target

Từ note ghi chú, bới ra IP của khứa attacker:

- `111.224.250.131`

Check location của IP thì về thẳng:

- `Shijiazhuang`

![Traffic evidence showing the attacker's IP in the SQL injection activity](/assets/images/cyberdefenders/web-investigation/attacker-ip.png)

![AbuseIPDB-style lookup tying the source IP to Shijiazhuang](/assets/images/cyberdefenders/web-investigation/city-lookup.png)

### 2. Tìm trúng endpoint hớ hênh

Cái phễu PHP thủng là file:

- `search.php`

Và URI đầu tiên thả chui vô là:

- `/search.php?search=book%20and%201=1;%20--%20-`

### 3. Tái hiện giai đoạn Enumeration

Lần mò đường mòn mà attacker đi qua, ta phát hiện nó chọc vào schema và chốt được bảng chứa user:

- `customers`

![Database enumeration through SQL injection against INFORMATION_SCHEMA](/assets/images/cyberdefenders/web-investigation/database-enum.png)

![Enumeration result exposing the customers table](/assets/images/cyberdefenders/web-investigation/customers-table.png)

### 4. Lần theo các vệt Post-Enumeration

Thư mục ẩn lõi thòi lòi ra là:

- `admin`

Thông tin đăng nhập bị bợ đi:

- `admin:admin123!`

![Captured admin credentials used to log in](/assets/images/cyberdefenders/web-investigation/admin-login-creds.png)

Mã độc thảy ngược lại server:

- `NVri2vhp.php`

![Uploaded PHP web shell used for server-side control](/assets/images/cyberdefenders/web-investigation/web-shell-upload.png)

## Các gạch đầu dòng khi điều tra (Investigation Notes)

Case này giống y chang một cuốn SGK mẫu về Web Compromise Workflow:

1. Test chọc SQL injection hòng moi Database.
2. Truy xuất thẳng vô Table và Column.
3. Quất Brute forcing băm thư mục.
4. Xài cặp Credential đi loot đồ Admin.
5. Quăng quả Web Shell để đóng chốt cắm cờ nằm lì bên trong.

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
