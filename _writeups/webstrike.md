---
title: "WebStrike"
date: 2026-03-31
ctf: "CyberDefenders"
category: network
difficulty: easy
tags: [cyberdefenders, webshell, web-forensics, exfiltration, pcap]
excerpt: "Theo doi web attack tu upload web shell den exfiltration trong challenge WebStrike."
---

Imported and adapted from my Notion notes for the CyberDefenders `WebStrike` challenge.

## Scenario

The PCAP shows a web server under attack. The attacker uploads a web shell, executes commands through it, and attempts to exfiltrate sensitive data.

## Key Findings

### Attacker profile

- Origin city: `Tianjin`
- User-Agent:
  `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`

### Web shell activity

- Uploaded shell name: `image.jpg.php`
- Upload directory: `/reviews/uploads`
- Port used by the shell: `8080`

The attacker first attempted a simpler payload name, then shifted to a double-extension file to bypass validation.

### Data theft

- File targeted for exfiltration: `passwd`

## Investigation Notes

The quickest way to solve this case is:

1. Filter `POST` requests to spot file uploads.
2. Follow the request and response flow for the uploaded shell.
3. Identify subsequent command-and-control style requests from the web shell.
4. Review outbound traffic to confirm what the attacker tried to read or export.

## Answers

- Origin city: `Tianjin`
- User-Agent: `Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0`
- Web shell: `image.jpg.php`
- Upload directory: `/reviews/uploads`
- Web shell port: `8080`
- Exfiltrated file target: `passwd`
