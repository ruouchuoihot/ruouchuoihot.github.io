---
title: "CryptoHash — Weak Hash Challenge"
date: 2026-03-29
ctf: "Example CTF 2026"
category: crypto
difficulty: medium
points: 200
tags: [hash, md5, rainbow-table, cryptography]
---

Challenge yêu cầu tìm plaintext từ một MD5 hash.

## Challenge Description

> Chúng tôi tìm được hash password của admin. Hãy crack nó!
> 
> `5f4dcc3b5aa765d61d8327deb882cf99`

## Solution

### Bước 1: Xác định loại hash

Hash có 32 ký tự hex → **MD5**.

```bash
hash-identifier 5f4dcc3b5aa765d61d8327deb882cf99
# Output: MD5
```

### Bước 2: Crack với hashcat

```bash
# Dùng wordlist rockyou.txt
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

# Hoặc dùng John the Ripper
echo "5f4dcc3b5aa765d61d8327deb882cf99" > hash.txt
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

### Bước 3: Kết quả

```
5f4dcc3b5aa765d61d8327deb882cf99:password
```

Plaintext là `password`. Quá đơn giản! 😄

Submit flag:

<div class="flag">flag{md5_1s_n0t_s3cur3}</div>

## Lessons Learned

1. **MD5 không an toàn** cho password hashing — dùng bcrypt, scrypt, or Argon2
2. Luôn dùng **salt** để chống rainbow table attacks
3. Password phổ biến luôn bị crack nhanh bởi wordlist attacks
