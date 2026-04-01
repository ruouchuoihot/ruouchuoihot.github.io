---
title: "WebStrike"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: easy
tags: [cyberdefenders, webshell, web-forensics, exfiltration, pcap]
excerpt: "Lần theo dấu vết web attack từ khâu upload web shell đến lúc exfiltration tẩu tán data trong lab WebStrike."
---

## Kịch bản (Scenario)

Bản PCAP bắt trọn khoảnh khắc một Web server đang bị dập tơi bời. Attacker ném lên một file web shell, dùng nó làm cửa hậu gõ lệnh, rồi ngoạm data nhạy cảm chuẩn bị mang tuồn (exfiltrate) ra ngoài.

Nhấn gọn nhưng cực kỳ thực dụng:

1. Tải mồi nhử độc hại (Malicious upload).
2. Chiếm quyền điều khiển thực thi qua đường file upload.
3. Thả các luồng request tương tác tiếp theo.
4. Đẩy ngược data tẩu tán.

## Những phát hiện chính (Key Findings)

### Profile Attacker

- Tọa độ xuất phát: `Tianjin` (Thiên Tân)
- User-Agent:
  `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`

![Geo lookup that maps the attacking IP to Tianjin](/assets/images/cyberdefenders/webstrike/origin-city.png)

![HTTP stream showing the attacker user-agent](/assets/images/cyberdefenders/webstrike/user-agent.png)

### Săm soi lại hoạt động Web Shell

- Tên file shell mớm lên: `image.jpg.php`
- Đỉnh điểm nằm ở thư mục: `/reviews/uploads`
- Port bị gắn họng hút do shell đẩy vào: `8080`

![Double-extension web shell upload used to bypass validation](/assets/images/cyberdefenders/webstrike/web-shell-upload.png)

![Execution path confirming the upload directory](/assets/images/cyberdefenders/webstrike/upload-directory.png)

Kẻ tấn công ban đầu vờ đặt cái tên payload rõ hiền, sau đó lắc lươn chuyển sang ngón nghề double-extension (tên có 2 đuôi) để đâm lủng cái hàng rào validation.

### Đánh cắp dữ liệu

- File nằm trong danh sách bế đi: `passwd`

![Traffic showing the attacker targeting passwd for exfiltration](/assets/images/cyberdefenders/webstrike/passwd-exfil.png)

## Phân tích chuyên sâu (Analysis Walkthrough)

### 1. Phác thảo Attacker Profile

Chỉ cần soi sơ luồng HTTP stream là lòi ra User-agent và lần theo IP là ra cái nguồn gốc địa lý dính đến kẻ tấn công.

### 2. Focus vào luồng thư mục Uploads

Lọc thẳng request `POST`, soi thật nhanh hành vi upload là thấy cấn ngay. Lão này định dùng loại file phổ thông nhưng gặp khó nên mới dùng chiêu ném `image.jpg.php` để luồn qua khe giới hạn filter.

### 3. Định hình lại Excecution Path

Khi soi cái đường dẫn `/reviews/uploads`, ta biết tỏng đây là cái kho cất đồ upload mà app chỉ định sẵn. Nước sau đó, attacker cứ rình chọt vào đây gõ tới.

### 4. Tracking Command và hành vi Exfiltration

Traffic dính dáng đến file shell cho thấy attacker cắm vòi hút vào port `8080` và nỗ lực cấu trúc file `passwd`, khẳng định 100% đây là chuỗi "hậu upload" chứ không phải màn kịch lỗi upload.

## Các lệnh rà soát khi điều tra (Investigation Notes)

Nhanh gọn lẹ để triệt phá cái case này:

1. Filter bằng `POST` để túm luồng upload ảnh/file.
2. Dò theo mạch Request & Response cho bằng được cái shell.
3. Check coi có cha nào command liên đới nổ từ C2 server thông diễn qua con shell hay không.
4. Review toàn cảnh Outbound traffic coi có file nào bị bế đi lọt đường chưa.

## Ma trận đáp án (Answer Matrix)

- Origin city: `Tianjin`
- User-Agent: `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`
- Web shell: `image.jpg.php`
- Upload directory: `/reviews/uploads`
- Web shell port: `8080`
- Exfiltrated file target: `passwd`

## Ghi chú

Bản writeup này hiện đã áp dụng cấu trúc phân tích đầy đủ và đồng bộ ảnh tĩnh về cục máy local block.
