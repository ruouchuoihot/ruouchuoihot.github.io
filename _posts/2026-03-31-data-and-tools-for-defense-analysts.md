---
title: "Data và Tools cho Defense Analyst trong Splunk"
date: 2026-03-31
category: siem
tags: [splunk, siem, blue-team, soc, threat-intelligence]
excerpt: "Tổng hợp các luồng data và mớ công cụ mà một defense analyst phải nhai hằng ngày khi làm việc với Splunk: auth, proxy, AV, firewall, endpoint, CTI và vọc metadata."
---


## Tầm nhìn của SOC về nguyên một stack

Có một ý cực kỳ tâm đắc trong note này: Một Defense Analyst không bao giờ coi Splunk là công cụ dùng một mình (isolated tool). Splunk luôn nằm lấn lướt trong một workflow SOC rộng lớn hơn, xoắn tít với SIEM, tự động hoá, telemetry và threat intelligence.

![SOC tool overview](/assets/images/splunk/defense-analyst-soc-overview.png)

![SOC stack and analyst workflow](/assets/images/splunk/defense-analyst-soc-stack.png)

Trong cấu trúc đồ sộ này:

- `Splunk Enterprise Security` đóng vai trò là quả tim SIEM
- `Splunk SOAR` phụ trách gánh bớt các thao tác phản hồi lặp đi lặp lại
- Dân Analyst đè các *detections*, *notable events* ra để nhào nặn ra context phục vụ investigate các hoạt động đáng ngờ.

## Tại sao mấy cái Notable Events lại quan trọng?

Có một câu vắn tắt trong note cực kỳ đáng giá:

> Cái hay của một notable event (sự kiện đáng lưu ý) là nó khoanh vùng thẳng mặt những log cho Analyst biết đâu là những mẩu data có tỉ lệ là mã độc cao nhất.

Đây chính là lý do notable event mang tính sống còn trên một hệ thống SOC thực tế. Nó chặt bớt thời gian ae phải rị mọ trong đống rác nhiễu (lower-priority noise).

## Nguồn Data cốt lõi cho nghề Defense Analyst

Giá trị nhất của note này là phân loại rõ ràng Analyst cần soi mờ mắt vào cái gì.

### Network Information (Thông tin Mạng)

Network data gỡ rối cho Analyst hiểu về giao tiếp, các luồng kết nối và khả năng kẻ địch bò trườn trong mạng nội bộ.

Hàng xịn bao gồm:

- NetFlow và flow logs
- Firewall events (Log tường lửa)
- IDS/IPS alerts
- Bản chụp gói tin (Packet capture) sau khi nổ ra sự cố
- DPI dùng để moi ruột gói tin real-time

Đây là huyết mạch để vẽ lại luồng traffic mờ ám hoặc chốt sổ xem có màn lateral movement (di chuyển ngang) xảy ra hay không.

### Authentication Information (Thông tin Xác thực)

Nếu không có Authentication data, việc điều tra đành chịu mù màu. Đây là gốc rễ của mọi thứ.

![Authentication and identity context](/assets/images/splunk/defense-analyst-authentication.png)

Hốt được mấy sources này là bao ngon:

- Active Directory
- LDAP
- RADIUS
- TACACS+
- Okta hoặc Azure AD
- VPN logs
- AWS CloudTrail

Luồng log này trả lời thẳng chóc:

- Ai đăng nhập (who authenticated)
- Làm trò ở đâu (from where)
- Can thiệp vô cái gì (to what)
- Đang gác quyền hay identity hão nào.

### Proxy và Gateway Information

Log lội từ Web proxies hay gateways đẻ ra hàng mớ bối cảnh:

- User lướt mấy website nào
- Bắt bài luồng traffic lặn sâu ngầm
- Lật tẩy mấy cái download bá dơ
- Hành vi xài web liên đới đến trò thả mã độc phía sau

Mớ data này xài xả láng khi moi móc vụ phishing, lôi cổ malware payload hay nhổ băng nhóm outbound traffic đen tối.

### AV và Endpoint Security Logs

Quả không ngoa, nhật ký Anti-virus (AV) và Endpoint Protection dính tới pháp y trực tiếp trên máy trạm.

![AV logs and endpoint detections](/assets/images/splunk/defense-analyst-av-logs.png)

Logs kiểu này quăng ra mặt:

- Signal khớp với malware signature
- Lịch sử quarantine (cách ly) hay remediation
- Điểm tên mấy file hoặc hash hắc ám
- Phác họa rành rành dòng thời gian máy nạn nhân bị lây nhiễm

### Firewall và Network Controls

Log tường lửa bơm thêm quyền cho Analyst để bắt quả tang:

- Traffic vọt qua một cách lố lăng
- Mấy luồng truy cập chéo vùng (zones) vô cớ
- Vài rục rịch giao thức sai lệch
- Lệnh denies dội liên hoàn từ một nguồn độc đắc
- Bằng chứng rành rành cho trò quét mạng và chuẩn bị bẻ khoá

### Endpoint Information

Ghi đè lên bằng endpoint log thì sẽ lòi ra:

- Failed logins ngập mặt
- Cố gắng leo quyền (Privilege escalation)
- Process lạ hoắc trồi lên
- Dấu hiệu bất thường chạm vào file hoặc system
- Nết lạm dụng dính dáng đến insider threat hay xé rào chính sách

### Server và Application Logs

Chính mấy ổ Server bự chảng nhả ra telemetry để confirm rốt cuộc vụ việc tiến triển thế nào:

- Luồng giao tiếp bốc mùi
- App thả error bất thường
- Đứt đoạn, đổi thay Service
- Thực thi Process
- Lật mặt account nhám nhúa
- Các hành động gác quyền

## Gắn Threat Intelligence thẳng vào Workflow

Note này còn nhắc đến trò chơi gắn `Cyber Threat Intelligence` (Tình báo mối đe dọa) vô guồng.

Có hai mặt trận đỉnh cao là:

- `Tactical intelligence` (Chiến thuật): IPs, URLs, hashes, signatures và đống IOCs nổ bùm bụp.
- `Operational intelligence` (Hoạt động): Điểm sơ sơ các thủ đoạn, ngón nghề và thói quen hành vi đặc sệt của attacker.

Operational intelligence cực kì ráo riết để:

- Threat hunting vọc vạch kiếm chuyện.
- Đong đếm hậu quả cái đợt compromise lan tới đâu.
- Bưng mớ lầy lội này map vô khung chuẩn của MITRE ATT&CK.

## Tại sao mớ này lại làm nên truyện trong Splunk?

Trớ trêu thay, gắp hết vào list tự học Splunk chỉ vì một chân lý đơn điệu:

- Splunk xịn cỡ nào cũng quy vào chất lượng data hút vào.
- Detections gõ SPL mỏi tay cũng vô dụng nếu rỗng context.
- Đời Analyst phải ôm cả telemetry lẫn rổ context bối cảnh thì mới investigate ra ngô ra khoai.

## Gói ghém lại (Practical Takeaway)

Chốt hạ một câu đâm thẳng ruột:

Làm Defense Analyst giỏi không phải cứ cắm mỏ search log là hay. Dân Analyst đỉnh phải biết:

- Source data nào moi giá trị
- Tool nào chạc thêm context ngon rinh
- Cách pivot bẻ lái nhảy từ cục telemetry này sang cục khác như múa
- Kết dính chằng chịt detections với identity, asset và đống intelligence context búa xua.

Đấy mới là tuyệt kỹ hô biến Splunk từ máy tìm kiếm cùi bắp thành nền tảng pháp y sừng sỏ.
