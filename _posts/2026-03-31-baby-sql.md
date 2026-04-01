---
title: "Phân Tích Log Brute Force Attack trong Windows Event Log"
date: 2026-03-30
ctf: "CyberDefenders - BruteForce"
category: soc
difficulty: easy
points: 100
tags: [soc, windows-event-log, brute-force, log-analysis]
---

Challenge yêu cầu phân tích Windows Security Event Log để tìm dấu hiệu brute force attack và xác định tài khoản bị compromise.

## Reconnaissance

Nhận được file `Security.evtx` — Windows Security Event Log. Mở file bằng Event Viewer hoặc import vào Splunk.

## Analysis

### Bước 1: Tìm failed login attempts

Event ID **4625** = Failed login attempt:

```splunk
source="Security.evtx" EventCode=4625
| stats count by Account_Name, Source_Network_Address
| sort -count
```

Kết quả:

| Account_Name | Source_Network_Address | Count |
|---|---|---|
| admin | 192.168.1.100 | 847 |
| administrator | 192.168.1.100 | 523 |
| root | 192.168.1.100 | 312 |

→ IP `192.168.1.100` đang thực hiện **brute force** với hàng trăm lần login thất bại.

### Bước 2: Kiểm tra successful login sau brute force

Event ID **4624** = Successful login:

```splunk
source="Security.evtx" EventCode=4624 Source_Network_Address="192.168.1.100"
| table _time, Account_Name, Logon_Type
```

Kết quả: Account `admin` login thành công lúc **14:32:17** sau 847 lần thử!

### Bước 3: Kiểm tra hành vi sau khi compromise

```splunk
source="Security.evtx" Account_Name="admin" _time>"2026-03-15 14:32:17"
| table _time, EventCode, Message
```

Phát hiện:
- **4672**: Special privilege logon (admin rights)
- **4688**: New process created (`cmd.exe`, `powershell.exe`)
- **4720**: New user account created (`backdoor`)

## Timeline

```
14:00:00 - Bắt đầu brute force từ 192.168.1.100
14:32:17 - Login thành công với account "admin"
14:32:45 - Escalate privileges (Event 4672)
14:33:12 - Mở cmd.exe (Event 4688)
14:35:00 - Tạo backdoor account (Event 4720)
```

## Flag

<div class="flag">flag{br0t3_f0rc3_d3t3ct3d_192.168.1.100}</div>

## Detection Rules

### Splunk Alert Rule
```splunk
index=windows EventCode=4625
| stats count by Account_Name, Source_Network_Address
| where count > 50
| eval alert="Possible Brute Force Attack"
```

### SIGMA Rule
```yaml
title: Brute Force Attack Detection
status: production
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4625
  condition: selection | count(TargetUserName) by IpAddress > 50
  timeframe: 1h
level: high
```

## Lessons Learned

1. **Monitor Event ID 4625** — failed logins là indicator đầu tiên
2. **Correlate 4625 → 4624** — brute force thành công khi có successful login ngay sau nhiều failures
3. **Alert threshold** — >50 failed logins/hour từ cùng IP = cần investigate
4. **Account lockout policy** — nên set lockout sau 5-10 lần sai
5. **MFA** — giải pháp hiệu quả nhất để chống brute force
