---
title: "Web Investigation"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: medium
tags: [cyberdefenders, sql-injection, web-forensics, enumeration, webshell]
excerpt: "Phan tich SQL injection chain, enum database va web shell upload trong challenge Web Investigation."
---

Imported and adapted from my original Notion notes for the CyberDefenders `Web Investigation` challenge.

## Scenario

The attacker abuses a vulnerable PHP search endpoint to enumerate the backend database, discover hidden directories, steal credentials, and finally upload a malicious PHP script.

This is effectively a full web compromise story compressed into one capture:

1. SQL injection discovery
2. Schema and table enumeration
3. Hidden directory discovery
4. Credential abuse
5. Web shell upload

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

## Analysis Walkthrough

### 1. Identify the attacker and target

The attacking client recovered from the notes is:

- `111.224.250.131`

with origin city:

- `Shijiazhuang`

![Traffic evidence showing the attacker's IP in the SQL injection activity](/assets/images/cyberdefenders/web-investigation/attacker-ip.png)

### 2. Find the vulnerable endpoint

The vulnerable PHP file is:

- `search.php`

and the first observed SQLi URI is:

- `/search.php?search=book%20and%201=1;%20--%20-`

### 3. Reconstruct the enumeration phase

The notes walk through schema discovery and identify the user-related table:

- `customers`

![Database enumeration through SQL injection against INFORMATION_SCHEMA](/assets/images/cyberdefenders/web-investigation/database-enum.png)

### 4. Follow post-enumeration actions

The hidden directory discovered is:

- `admin`

The credentials abused are:

- `admin:admin123!`

The uploaded malicious script is:

- `NVri2vhp.php`

## Investigation Notes

The case is a good example of a full web compromise workflow:

1. SQL injection testing and database enumeration
2. Table and column discovery
3. Directory brute forcing
4. Credential abuse against the admin area
5. Web shell upload for persistent server-side control

## Answer Matrix

- Attacker IP: `111.224.250.131`
- City: `Shijiazhuang`
- Vulnerable script: `search.php`
- First SQLi URI: `/search.php?search=book%20and%201=1;%20--%20-`
- Database enumeration URI: `/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,schema_name)),0x7176706a71) FROM INFORMATION_SCHEMA.SCHEMATA-- -`
- User table: `customers`
- Hidden directory: `admin`
- Credentials: `admin:admin123!`
- Malicious script: `NVri2vhp.php`
