---
title: "Web Investigation"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: medium
tags: [cyberdefenders, sql-injection, web-forensics, enumeration, webshell]
excerpt: "Phan tich SQL injection chain, enum database va web shell upload trong challenge Web Investigation."
---

Imported and adapted from my Notion notes for the CyberDefenders `Web Investigation` challenge.

## Scenario

The attacker abuses a vulnerable PHP search endpoint to enumerate the backend database, discover hidden directories, steal credentials, and finally upload a malicious PHP script.

## Key Findings

- Attacker IP: `111.224.250.131`
- Origin city: `Shijiazhuang`
- Vulnerable script: `search.php`
- First SQLi request:
  `/search.php?search=book%20and%201=1;%20--%20-`
- Request used to enumerate databases:
  `/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,schema_name)),0x7176706a71) FROM INFORMATION_SCHEMA.SCHEMATA-- -`
- Table containing website user data: `customers`
- Hidden directory found by the attacker: `admin`
- Credentials used to log in: `admin:admin123!`
- Uploaded malicious script: `NVri2vhp.php`

## Investigation Notes

The case is a good example of a full web compromise workflow:

1. SQL injection testing and database enumeration
2. Table and column discovery
3. Directory brute forcing
4. Credential abuse against the admin area
5. Web shell upload for persistent server-side control

## Answers

- Attacker IP: `111.224.250.131`
- City: `Shijiazhuang`
- Vulnerable script: `search.php`
- First SQLi URI: `/search.php?search=book%20and%201=1;%20--%20-`
- Database enumeration URI: `/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,schema_name)),0x7176706a71) FROM INFORMATION_SCHEMA.SCHEMATA-- -`
- User table: `customers`
- Hidden directory: `admin`
- Credentials: `admin:admin123!`
- Malicious script: `NVri2vhp.php`
