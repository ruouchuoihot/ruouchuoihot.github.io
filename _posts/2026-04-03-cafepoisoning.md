---
title: "CafePoisoning"
date: 2026-04-03
ctf: "Hack The Box"
category: forensics
difficulty: easy
tags: [hack-the-box, htb, dfir, wireshark, network-forensics, arp-poisoning]
excerpt: "Phân tích pcapng và triage artifact để bóc tách luồng tấn công ARP poisoning, chặn đứng DNS spoofing và truy vết C2 qua Wireshark."
---

![CafePoisoning](/assets/images/htb/cafepoisoning/527d2172-92a8-48dd-b0b7-ae8f16cb8857.png)

## Kịch bản (Scenario)

**Trong lúc rẽ vào quán cafe làm ly đen đá, tôi tiện tay cắm vào mạng Wi-Fi công cộng để update Windows. Đen cái là tiến trình update chạy mãi không xong, cứ treo lơ lửng. Dưới góc độ của một tay DFIR chuyên nghiệp, vào cuộc check thử xem chuyện gì đang xảy ra dưới lớp network.**

> Tag: DFIR

Challenge cung cấp:
- 1 file `pcapng`
- 1 thư mục Triage của máy nạn nhân: `DESKTOP-TIT3D2T`

![Triage Folder](/assets/images/htb/cafepoisoning/abcd13cf-fbb3-422c-8322-03058de69a17.png)

---

## Phân tích Chuyên sâu (Walkthrough)

### 1. Dò tìm dấu vết Discovery Scan của kẻ tấn công

> The attacker performed a host discovery scan to identify devices on the network. Provide the start time of this activity in UTC.

Mở Wireshark, tôi filter thẳng vào các gói tin ARP. Rà lại file pcapng, bắt đầu từ mốc thời gian `2025-03-10 21:07:05`, ghi nhận một loạt các gói broadcast ARP nổ ra liên tục từ source `devx-corp.net`. Đây là dấu hiệu rành rành của trò ping sweep / arp scan để dựng bản đồ mạng nội bộ.

![ARP Scan Discovery](/assets/images/htb/cafepoisoning/c1b6a3b8-5582-4279-ab58-c3a2d8daab6a.png)

```
2025-03-10 21:07:05
```

### 2. Xác định thời điểm ARP Poisoning phát nổ

> The attacker launched an ARP poisoning attack. Provide the start time in UTC.

**Kiến thức căn bản về ARP Poisoning:** Trò này thường xảy ra khi attacker nhồi các gói ARP reply giả mạo để lừa máy nạn nhân (hoặc gateway) ánh xạ IP của gateway/nạn nhân vào địa chỉ MAC của attacker. Điều này làm rối loạn ARP table của nạn nhân, dọn đường cho kịch bản Man-In-The-Middle (MitM) hoàn hảo.

Dấu hiệu nhận biết đặc trưng trên Wireshark:
- Xuất hiện cùng 1 IP nhưng nhảy múa qua 2 MAC address khác nhau trong gói ARP reply (opcode 2).
- Mật độ văng ARP cực kỳ dày và liên tục.
- Ngay sau đó, traffic ở Layer 3/7 (như HTTP/DNS) của victim bỗng dưng đi unicast thẳng vào mồm cái MAC của attacker.

![ARP Poisoning Detected](/assets/images/htb/cafepoisoning/c2b8fb59-7a25-41ad-a3bb-28cb3ec70323.png)

Nhìn lại mạng: Target IP `192.168.1.43` có ánh xạ chuẩn ban đầu là `192.168.1.43 is-at 1c:bf:ce:d9:b2:db` lúc `21:07:07`.
Tuy nhiên sau đó, bất thình lình lòi ra dải ARP reply thối từ MAC `08:00:27:9b:8b:bd` tự nhận danh xưng `"192.168.1.43 is-at 08:00:27:9b:8b:bd"`.

Rõ ràng attacker đang tráo hàng IP `192.168.1.43` bằng cái MAC bá dơ `08:00:27:9b:8b:bd`. Mốc thời gian sớm nhất khứa này tung skill là `2025-03-10 21:07:33`.

```
2025-03-10 21:07:33
```

### 3. Tóm cổ địa chỉ MAC của Attacker

> What MAC address did the attacker use during the ARP poisoning attack?

Phân tích thẳng tay từ câu 2, địa chỉ MAC giả mạo kẻ thủ ác dùng làm mồi nhử trong quá trình ARP poisoning là:

```
08:00:27:9b:8b:bd
```

### 4. Truy vết IP Nạn nhân (Target IP)

> What is the IP address targeted by the attacker?

Lê bước theo file packet ở câu 2, để ý dòm vào trường `Target IP` bên trong luồng ARP tà đạo, nạn nhân xấu số bị rải bùa chính là `192.168.1.90`.

![Target IP Details](/assets/images/htb/cafepoisoning/dc618abb-29c7-4000-97e8-b86b78065660.png)

```
192.168.1.90
```

### 5. Lật mặt domain giả (Spoofed Domain)

> Which spoofed domain was accessed by the compromised user?

Lội tiếp theo cái luồng packet poison ở câu số 2, rình xem sau khi cướp đường thì attacker điều traffic đi đâu, lòi ra domain mà attacker mang ra mồi nạn nhân là `devx-corp.net`. 
Bám sát traffic, rành rành ra các luồng Reply của `192.168.1.90` (máy victim) trỏ thẳng về cái domain ất ơ này.

![Spoofed Domain Traffic](/assets/images/htb/cafepoisoning/46e02542-16b7-40f7-a18c-dd887cf6399f.png)

```
devx-corp.net
```

### 6. Tìm lại Địa chỉ Legitimate IP thực lòng lúc đầu

> What was the legitimate IP address accessed by the compromised user before the DNS spoofing occurred?

Ngâm file pcap hoài vẫn không cạy mồm được IP thật, vì traffic đã bị đánh tráo toàn cục. Dạt sang phương án B, nhảy vào thư mục `Triage` đào bới xem có lòi ra artifact gì khô khan không. Quả nhiên chộp được đống dữ liệu vọc vạch của Google Chrome.

![Google Chrome Artifacts](/assets/images/htb/cafepoisoning/b00b23ea-66e8-4cb6-8c02-475458c3a169.png)

Bản chất mấy ruột log của Chrome viết thuần trên database dạng `sqlite`. Gõ vài từ khóa kéo về được món hàng chuyên dụng để nhai đồ cache trình duyệt: `ChromeCacheView`.
Lôi tool ra xài, móc filter dò thẳng cái domain ngụy tạo `devx-corp.net`. Bùm! Truy xuất được hai vệt IP:
- Legitimate IP (IP chuẩn chỉnh): `137.50.21.6`
- Spoofed IP (IP mà mị lừa): `192.168.1.11`

![Chrome Cache Analysis](/assets/images/htb/cafepoisoning/6acddd23-77c5-4f10-bddf-e0d43c4366f9.png)

```
137.50.21.6
```

### 7. Khui SSID Wifi và thuật toán mã hoá

> Identify the Wi-Fi network name (SSID) and the authentication algorithm used by the compromised user's connection.

Luồn lách vào mảng thư mục chứa Windows Event Log trong nhánh Triage tại `C:\Windows\System32\winevt\logs`, mò tìm trúng file `Wlan-Autoconfig`. Đây là hang ổ chứa mọi bí mật về hành vi log wifi của hạ tầng Windows.

> [!TIP]
> Ae có thể tham khảo mẹo dùng log Windows để mổ network [tại đây](https://www.dell.com/support/kbdoc/en-us/000150790/using-windows-logs-to-troubleshoot-wireless-issues-only-seen-at-customer-locations).

Focus ngay vào Event ID `8001`, nó trút ra cặn kẽ mọi thông tin ẩn số về SSID.

![SSID Authentication Event](/assets/images/htb/cafepoisoning/9283e5bd-9df3-445a-8b7b-bffc3b9500e3.png)

```
Cuppa Ce:WPA2-Personal
```

### 8. Link tải file độc hại (Malicious Executable)

> Identify the download link used to fetch the malicious executable.

Trong bọc pcap, rà soát lại lưu lượng HTTP móc trúng đường dẫn download cái cục nợ executable kia:

```
192.168.1.11:5078
```

### 9. Soi C2 Server hoạt động

> Identify the IP address and port number of the Command-and-Control (C2) server.

Áp dụng chiêu tương tự, tra xét vạt outbound connection hướng thẳng ra ngoài:

```
s1rx-update.xyz
```

### 10. Check domain C2 Server

> The malicious executable is designed to check the C2 server before connecting. Provide the domain name of the C2 server.

Domain chết chóc bị ngòi cho phép thực thi:

```
s1rx-update.xyz
```

### 11. Hàm Win32 API nhúng quyền hắc ám

> The malicious executable verifies privileges before execution to ensure it runs as administrator. Which Win32 API function is used for this check?

Từ kết quả đảo qua IDA/binaries (hoặc log rò rỉ), hành vi cắm sừng check quyền Local Admin ăn vào hàm cốt lõi Win32 sau:

```
CheckTokenMembership()
```

### 12. Triệt hạ hàng thủ Windows Defender

> Which command was executed by the attacker to disable Windows Defender?

Kẻ tấn công không ngần ngại nhét trực diện lệnh bypass vào Powershell, với mảng ruột như sau:

```powershell
  if ($PSBoundParameters.ContainsKey('DisableRealtimeMonitoring')) {
            [object]$__cmdletization_value = ${DisableRealtimeMonitoring}
            ...
```

Nhào ra lệnh hoàn chỉnh nã gục Defender:

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true -Verbose
```

### 13. Cơ chế Nằm Vùng (Persistence)

> A persistence mechanism was created by the attacker. Provide the registry key used for persistence.

Xọc vào đường Registry để tự động tái khởi động ăn nhờ ở đậu, mục tiêu của nó là:

```
HKCU\Control Panel\Desktop
```

![Persistence Registry](/assets/images/htb/cafepoisoning/c2fdecf2-fb91-4aca-ad8b-716ef0a9270f.png)
