---
title: "Bắt đầu với CTF: Hướng dẫn cho người mới"
date: 2026-03-30
category: misc
tags: [ctf, beginner, guide]
---

CTF (Capture The Flag) là cuộc thi an ninh mạng nơi bạn giải các thử thách bảo mật để tìm "flag" — một chuỗi ký tự ẩn.

## Các loại challenge phổ biến

### 🌐 Web Exploitation
Khai thác lỗ hổng ứng dụng web: SQL Injection, XSS, SSRF, IDOR, ...

```python
# Ví dụ: SQL Injection payload
payload = "' OR 1=1 --"
url = f"http://target.com/login?user={payload}"
```

### 💻 Binary Exploitation (Pwn)
Khai thác lỗ hổng trong binary: Buffer Overflow, Format String, Use-After-Free, ...

### 🔐 Cryptography
Phá mã hoá: RSA, AES, Hash, XOR, ...

### 🔍 Forensics
Phân tích file, network traffic, memory dump, ...

### ⚙️ Reverse Engineering
Dịch ngược binary để hiểu logic chương trình.

## Tools cơ bản cần có

| Tool | Mục đích |
|------|----------|
| Burp Suite | Web testing |
| Ghidra / IDA | Reverse engineering |
| pwntools | Binary exploitation |
| Wireshark | Network analysis |
| CyberChef | Encode/decode/crypto |
| John the Ripper | Password cracking |

## Platforms luyện tập

- [picoCTF](https://picoctf.org/) — Cho beginner
- [Hack The Box](https://hackthebox.com/) — Machines & challenges
- [TryHackMe](https://tryhackme.com/) — Guided learning
- [OverTheWire](https://overthewire.org/) — Wargames
- [CryptoHack](https://cryptohack.org/) — Crypto challenges

> 💡 Bắt đầu từ picoCTF, sau đó chuyển sang HTB và THM khi đã quen.

Chúc bạn hack vui vẻ! 🚀
