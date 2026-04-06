---
title: "PoisonedCredentials"
date: 2026-03-31
ctf: "CyberDefenders"
category: threat-hunting
difficulty: easy
tags: [cyberdefenders, llmnr, nbt-ns, credential-theft, smb]
excerpt: "Điều tra kỹ thuật poisoning qua LLMNR/NBT-NS để lần ra rogue host, tài khoản bị lộ và máy tính mục tiêu."
---

## Kịch bản (Scenario)

Challenge này tập trung vào kẽ hở của cơ chế phân giải tên miền nội bộ (local name resolution) trong môi trường Windows. Một cỗ máy giả mạo (rogue machine) đứng ra phản hồi các request giả (poisoned traffic), thu thập thông tin đăng nhập (authentication attempts), rồi lấy chính cái access đó quay ra quật lại một host nội bộ khác.

## Kiến thức cốt lõi (Core Concepts)

- `LLMNR` và `NBT-NS` là các giao thức phân giải tên nội bộ.
- Nhược điểm chí mạng là chúng không có bảo mật xác thực chặt chẽ cho các response.
- Attacker hoàn toàn có thể lắng nghe/đánh lừa (poison) các request này để bế luôn credential (hash) hoặc relay quyền đăng nhập.

![LLMNR and NBT-NS poisoning flow](/assets/images/cyberdefenders/poisonedcredentials/poisoning-diagram.png)

Đây là lý do anh em làm SOC phải coi chừng cái case này: Nó bắt nguồn từ những mẩu traffic nhiễu thoạt nhìn rất bình thường nhưng lại đẻ ra lỗ hổng credential theft.

## Những phát hiện chính (Key Findings)

- Hostname bị gõ nhầm: `fileshaare`
- Rogue machine IP: `192.168.232.215`
- Máy nạn nhân thứ 2 bị dính poison: `192.168.232.176`
- User bị hack: `janesmith`
- Host bị mò vào qua SMB: `AccountingPC`

## Phân tích chuyên sâu (Analysis Walkthrough)

### 1. Dò tìm cú gõ phím lỗi

Từ log, anh em sẽ bắt được ngay quả query "ngớ ngẩn" đầu tiên:

- `fileshaare`

![Mistyped hostname query that triggered the rogue response](/assets/images/cyberdefenders/poisonedcredentials/mistyped-query.png)

Chính vì lỗi typo này mà hệ thống phân giải tên thất bại, và đó là thời cơ vàng để thằng rogue responder ngoi lên.

### 2. Spot tên giả mạo (Identify the rogue system)

Lần theo luồng traffic name resolution bị poison, lù lù lòi ra quả IP giả mạo:

- `192.168.232.215`

![Rogue responder answering poisoned name resolution requests](/assets/images/cyberdefenders/poisonedcredentials/rogue-ip.png)

### 3. Trace các client bị ảnh hưởng

Cuộc tấn công không giới hạn ở một máy dính bẫy. Host thứ 2 nhận được câu trả lời giả mạo từ hệ thống là:

- `192.168.232.176`

### 4. Xác nhận lạm dụng Credential

Bới luồng SMB và NTLM, ta túm được:

- Dấu vết tài khoản bị xâm phạm: `janesmith`
- Máy đã bị bò vào: `AccountingPC`

![NTLM evidence showing the compromised account](/assets/images/cyberdefenders/poisonedcredentials/compromised-user.png)

![SMB follow-on access to AccountingPC](/assets/images/cyberdefenders/poisonedcredentials/accounting-pc.png)

Nước đi hoàn hảo từ lúc poison name resolution cho tới lúc lấy được internal access.

## Ý tưởng phát hiện (Detection Ideas)

- Tạo alert cho các LLMNR/NBT-NS responder mờ ám trên các vLAN của user.
- Tắt cụ LLMNR và NBT-NS luôn nếu policy của tổ chức cho phép.
- Tìm kiếm (Hunt) các outbound SMB session ngay sau những cú poisoned resolution traffic.
- Soi các failed authentication attempts liên tục đằng sau mớ multicast name queries.

## Answer

- Mistyped query: `fileshaare`
- Rogue IP: `192.168.232.215`
- Second poisoned host: `192.168.232.176`
- Compromised account: `janesmith`
- Accessed host: `AccountingPC`

## Ghi chú

Nguyên bộ screenshot mấu chốt của case này đã được đẩy thẳng vô local blog cho anh em dễ theo dõi.
