---
title: "WebStrike"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: easy
tags: [cyberdefenders, webshell, web-forensics, exfiltration, pcap]
excerpt: "Phân tích dấu vết web attack từ khâu upload web shell đến exfiltration data trong lab WebStrike."
---

## Kịch bản (Scenario)

Bản PCAP ghi lại toàn bộ quá trình một Web server bị tấn công. Attacker upload một file web shell, dùng nó làm backdoor để thực thi command, sau đó exfiltrate data nhạy cảm ra ngoài.

Tóm lại chuỗi tấn công gồm:

1. Upload file độc hại (Malicious upload).
2. Chiếm quyền thực thi qua đường file upload.
3. Gửi các request tương tác tiếp theo.
4. Exfiltrate data ra ngoài.

## Những phát hiện chính (Key Findings)

### Profile Attacker

- Vị trí địa lý: `Tianjin` (Thiên Tân)
- User-Agent:
  `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`

![Geo lookup that maps the attacking IP to Tianjin](/assets/images/cyberdefenders/webstrike/origin-city.png)

![HTTP stream showing the attacker user-agent](/assets/images/cyberdefenders/webstrike/user-agent.png)

### Phân tích Web Shell

- Tên file shell được upload: `image.jpg.php`
- Thư mục chứa shell: `/reviews/uploads`
- Port mà shell sử dụng: `8080`

![Double-extension web shell upload used to bypass validation](/assets/images/cyberdefenders/webstrike/web-shell-upload.png)

![Execution path confirming the upload directory](/assets/images/cyberdefenders/webstrike/upload-directory.png)

Attacker sử dụng kỹ thuật double-extension (đặt tên file có 2 phần mở rộng) để bypass cơ chế validation của server.

### Exfiltration

- File bị nhắm tới: `passwd`

![Traffic showing the attacker targeting passwd for exfiltration](/assets/images/cyberdefenders/webstrike/passwd-exfil.png)

## Phân tích chuyên sâu (Analysis Walkthrough)

### 1. Xác định Attacker Profile

Kiểm tra HTTP stream để lấy User-Agent, sau đó tra IP để xác định vị trí địa lý của attacker.

### 2. Phân tích luồng Upload

Filter request `POST` để tìm hành vi upload. Attacker ban đầu thử upload file thông thường nhưng bị chặn, sau đó chuyển sang kỹ thuật double-extension với file `image.jpg.php` để vượt qua filter.

### 3. Xác định Execution Path

Thư mục `/reviews/uploads` là nơi ứng dụng lưu file upload. Attacker truy cập shell từ thư mục này để thực thi command.

### 4. Tracking Command và Exfiltration

Traffic liên quan đến web shell cho thấy attacker kết nối qua port `8080` và truy cập file `passwd`, xác nhận đây là chuỗi hành vi post-exploitation chứ không phải lỗi upload thông thường.

## Ghi chú điều tra (Investigation Notes)

Các bước chính để phân tích case này:

1. Filter `POST` request để xác định luồng upload.
2. Theo dõi Request & Response liên quan đến web shell.
3. Kiểm tra xem có command nào được thực thi thông qua shell không.
4. Review outbound traffic để xác định file bị exfiltrate.

## Ma trận đáp án (Answer Matrix)

- Origin city: `Tianjin`
- User-Agent: `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`
- Web shell: `image.jpg.php`
- Upload directory: `/reviews/uploads`
- Web shell port: `8080`
- Exfiltrated file target: `passwd`
