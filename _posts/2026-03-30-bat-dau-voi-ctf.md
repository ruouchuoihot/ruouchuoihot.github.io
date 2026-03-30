---
title: "Blue Team CTF: Hướng dẫn cho người mới bắt đầu"
date: 2026-03-30
category: soc
tags: [blue-team, ctf, beginner, defense]
---

Blue Team CTF (Defensive CTF) tập trung vào kỹ năng **phòng thủ** — phát hiện, phân tích, và ứng phó sự cố an ninh mạng, thay vì tấn công.

## Blue Team CTF vs Red Team CTF

| | Blue Team CTF | Red Team CTF |
|---|---|---|
| **Mục tiêu** | Phát hiện & phân tích tấn công | Tấn công & khai thác lỗ hổng |
| **Kỹ năng** | SIEM, log analysis, forensics | Exploitation, privilege escalation |
| **Công cụ** | Splunk, Wireshark, Volatility | Burp Suite, Metasploit, nmap |
| **Vai trò** | SOC Analyst, IR, Threat Hunter | Pentester, Red Teamer |

## Các thể loại challenge phổ biến

### 🔍 Log Analysis / SIEM
Phân tích log từ Windows Event Log, Syslog, hoặc SIEM để tìm dấu hiệu tấn công.

```splunk
index=windows EventCode=4625
| stats count by Account_Name, Source_Network_Address
| where count > 10
| sort -count
```

### 🧠 Threat Hunting
Sử dụng MITRE ATT&CK framework để tìm IOCs (Indicators of Compromise).

### 🦠 Malware Analysis
Phân tích mẫu malware bằng static/dynamic analysis.

```bash
# Static analysis
strings suspicious_file.exe | grep -i "http"
file suspicious_file.exe
sha256sum suspicious_file.exe
```

### 🔬 Digital Forensics (DFIR)
Phân tích disk image, memory dump, network capture.

### 📡 Network Security
Phân tích PCAP, phát hiện network anomalies.

```bash
# Wireshark filter cho suspicious DNS
dns.qry.name contains "evil" || dns.resp.len > 512
```

## Platforms luyện tập

| Platform | Focus |
|----------|-------|
| [CyberDefenders](https://cyberdefenders.org/) | Blue Team labs |
| [LetsDefend](https://letsdefend.io/) | SOC Analyst simulation |
| [Blue Team Labs Online](https://blueteamlabs.online/) | DFIR challenges |
| [TryHackMe](https://tryhackme.com/) | SOC & Blue Team paths |
| [Splunk BOTS](https://bots.splunk.com/) | Splunk challenges |

## Tools cơ bản

| Tool | Mục đích |
|------|----------|
| Splunk / ELK | SIEM & log analysis |
| Wireshark | Network traffic analysis |
| Volatility | Memory forensics |
| FTK Imager | Disk forensics |
| YARA | Malware pattern matching |
| Suricata | Network IDS/IPS |
| Velociraptor | Endpoint monitoring |
| CyberChef | Data transformation |

> 💡 Bắt đầu từ CyberDefenders và LetsDefend, sau đó nâng cao với Blue Team Labs Online!

Chúc bạn defend vui vẻ! 🛡️
