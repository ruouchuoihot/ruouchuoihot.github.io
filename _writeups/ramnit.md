---
title: "Ramnit Memory Analysis"
date: 2026-03-31
ctf: "CyberDefenders"
category: malware
difficulty: medium
tags: [cyberdefenders, memory-forensics, malware-analysis, volatility]
excerpt: "Phan tich memory dump de xac dinh process Ramnit, IOC mang va domain lien quan."
---

Imported and adapted from my Notion notes for the CyberDefenders `Ramnit` challenge.

## Scenario

This case is a memory analysis exercise. Most of the visible outbound connections look normal, so the investigation depends on isolating the suspicious process and validating it with malware intelligence.

## Key Findings

- Suspicious process: `ChromeSetup.exe`
- Executable path: `C:\\Users\\alex\\Downloads\\ChromeSetup.exe`
- Remote IP: `58.64.204.181`
- Related city: `Hong Kong`
- SHA1 hash: `280c9d36039f9432433893dee6126d72b9112ad2`
- Compilation timestamp: `2019-12-01 08:36:04`
- Related domain: `dnsnb8.net`

## Investigation Flow

1. Use `windows.netscan` to review outbound connections.
2. Isolate uncommon infrastructure among otherwise legitimate Microsoft and CDN traffic.
3. Pivot to the process owning that connection.
4. Dump the executable and hash it.
5. Validate the sample against external intel sources.

## Why the process stood out

The key anomaly was not the process tree alone. It was the rare outbound connection owned by `ChromeSetup.exe`, combined with a path and hash that pointed to known malicious infrastructure.

## Answers

- Process: `ChromeSetup.exe`
- Path: `C:\\Users\\alex\\Downloads\\ChromeSetup.exe`
- IP: `58.64.204.181`
- City: `Hong Kong`
- SHA1: `280c9d36039f9432433893dee6126d72b9112ad2`
- Compilation time: `2019-12-01 08:36:04`
- Domain: `dnsnb8.net`
