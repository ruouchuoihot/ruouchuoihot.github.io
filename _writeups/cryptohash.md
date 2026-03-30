---
title: "Memory Forensics — Detect Malicious Process"
date: 2026-03-29
ctf: "Blue Team Labs Online"
category: dfir
difficulty: medium
points: 200
tags: [memory-forensics, volatility, malware, dfir]
---

Challenge cung cấp một memory dump từ máy bị nhiễm malware. Nhiệm vụ: tìm process độc hại và xác định C2 server.

## Analysis

### Bước 1: Xác định profile

```bash
volatility -f memory.dmp imageinfo
```

Output: `Win7SP1x64` — Windows 7 SP1 64-bit.

### Bước 2: List running processes

```bash
volatility -f memory.dmp --profile=Win7SP1x64 pslist
```

| PID | Name | PPID | Start Time |
|-----|------|------|------------|
| 4 | System | 0 | 2026-03-15 |
| 384 | smss.exe | 4 | 2026-03-15 |
| 1892 | explorer.exe | 1780 | 2026-03-15 |
| 2456 | chrome.exe | 1892 | 2026-03-15 |
| **3124** | **svchost.exe** | **1892** | **2026-03-15 14:35** |

⚠️ `svchost.exe` (PID 3124) có PPID = **1892 (explorer.exe)**. Bất thường! `svchost.exe` thật phải có PPID là `services.exe`.

### Bước 3: Kiểm tra network connections

```bash
volatility -f memory.dmp --profile=Win7SP1x64 netscan | grep 3124
```

```
Proto  Local Address     Foreign Address    State    PID
TCP    10.0.0.5:49234    185.141.27.33:443  ESTABLISHED  3124
```

→ PID 3124 đang kết nối đến **185.141.27.33:443** — đây là **C2 server**!

### Bước 4: Dump suspicious process

```bash
volatility -f memory.dmp --profile=Win7SP1x64 procdump -p 3124 -D output/
```

### Bước 5: Kiểm tra strings

```bash
strings output/executable.3124.exe | grep -i "http\|cmd\|shell\|password"
```

Output:
```
http://185.141.27.33/beacon
cmd.exe /c whoami
cmd.exe /c net user
CreateRemoteThread
VirtualAllocEx
```

→ Malware đang dùng **process injection** và giao tiếp với C2 qua HTTP beacon.

## Summary

| Item | Value |
|---|---|
| Malicious Process | svchost.exe (PID 3124) |
| Parent Process | explorer.exe (bất thường) |
| C2 Server | 185.141.27.33:443 |
| Technique | Process Injection (T1055) |
| MITRE ATT&CK | T1055, T1071.001 |

## Flag

<div class="flag">flag{m4l1c10us_svchost_185.141.27.33}</div>

## Detection Recommendations

1. **Monitor parent-child process relationships** — `svchost.exe` phải có parent là `services.exe`
2. **Network anomaly detection** — connections từ system processes đến external IPs
3. **YARA rule** cho pattern matching:

```yara
rule Suspicious_Svchost {
    meta:
        description = "Detects fake svchost.exe"
    strings:
        $s1 = "CreateRemoteThread"
        $s2 = "VirtualAllocEx"
        $s3 = "/beacon"
    condition:
        uint16(0) == 0x5A4D and 2 of them
}
```
