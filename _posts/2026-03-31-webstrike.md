---
title: "WebStrike"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: easy
tags: [cyberdefenders, webshell, web-forensics, exfiltration, pcap]
excerpt: "Theo doi web attack tu upload web shell den exfiltration trong challenge WebStrike."
---

Imported and adapted from my original Notion notes for the CyberDefenders `WebStrike` challenge.

## Scenario

The PCAP shows a web server under attack. The attacker uploads a web shell, executes commands through it, and attempts to exfiltrate sensitive data.

This is a compact but realistic sequence:

1. Malicious upload
2. Execution through the uploaded file
3. Interactive follow-up requests
4. Exfiltration attempt

## Key Findings

### Attacker profile

- Origin city: `Tianjin`
- User-Agent:
  `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`

![Geo lookup that maps the attacking IP to Tianjin](/assets/images/cyberdefenders/webstrike/origin-city.png)

![HTTP stream showing the attacker user-agent](/assets/images/cyberdefenders/webstrike/user-agent.png)

### Web shell activity

- Uploaded shell name: `image.jpg.php`
- Upload directory: `/reviews/uploads`
- Port used by the shell: `8080`

![Double-extension web shell upload used to bypass validation](/assets/images/cyberdefenders/webstrike/web-shell-upload.png)

![Execution path confirming the upload directory](/assets/images/cyberdefenders/webstrike/upload-directory.png)

The attacker first attempted a simpler payload name, then shifted to a double-extension file to bypass validation.

### Data theft

- File targeted for exfiltration: `passwd`

![Traffic showing the attacker targeting passwd for exfiltration](/assets/images/cyberdefenders/webstrike/passwd-exfil.png)

## Analysis Walkthrough

### 1. Identify the attacker profile

Following the HTTP stream is enough to recover the attacker user-agent and the geographic clue tied to the attacking IP.

### 2. Focus on uploads

Filtering `POST` requests highlights the malicious upload behavior quickly. The attacker first attempts a simpler payload name, then shifts to `image.jpg.php` to bypass file restrictions.

### 3. Confirm execution path

The file path `/reviews/uploads` reveals where the web application stores uploads and confirms the place from which the malicious code is later invoked.

### 4. Track command activity and exfiltration

The traffic associated with the shell shows the attacker using port `8080` and attempting to retrieve `passwd`, which confirms active post-upload exploitation rather than a failed upload attempt.

## Investigation Notes

The quickest way to solve this case is:

1. Filter `POST` requests to spot file uploads.
2. Follow the request and response flow for the uploaded shell.
3. Identify subsequent command-and-control style requests from the web shell.
4. Review outbound traffic to confirm what the attacker tried to read or export.

## Answer Matrix

- Origin city: `Tianjin`
- User-Agent: `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`
- Web shell: `image.jpg.php`
- Upload directory: `/reviews/uploads`
- Web shell port: `8080`
- Exfiltrated file target: `passwd`

## Notes

The main evidence screenshots from the original notes are now served from local blog assets.
