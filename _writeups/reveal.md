---
title: "Reveal"
date: 2026-03-31
ctf: "CyberDefenders"
category: dfir
difficulty: medium
tags: [cyberdefenders, memory-forensics, volatility, powershell, malware]
excerpt: "Memory forensics voi Volatility de tim process bi injected, payload giai doan hai va malware family."
---

Imported and adapted from my Notion notes for the CyberDefenders `Reveal` challenge.

## Scenario

This memory dump investigation focuses on a suspicious PowerShell execution chain and a second-stage payload loaded through signed binary proxy execution.

## Key Findings

- Malicious process: `powershell.exe`
- Parent PID: `4120`
- Second-stage payload filename: `3435.dll`
- Shared directory accessed: `davwwwroot`
- MITRE sub-technique: `T1218.011`
- Username running the process: `Elon`
- Malware family: `StrelaStealer`

## Investigation Flow

1. Use `windows.malfind` to identify suspicious injected or unpacked regions.
2. Pivot into process ancestry and user session information.
3. Identify the DLL used by the second stage.
4. Correlate the execution chain with threat intel to identify the family.

## Why this mattered

`powershell.exe` alone is not enough to call malicious. The stronger signal came from the combination of suspicious memory regions, the remote access path, and the rundll32-style second-stage execution pattern.

## Answers

- Process: `powershell.exe`
- Parent PID: `4120`
- DLL: `3435.dll`
- Shared directory: `davwwwroot`
- MITRE ID: `T1218.011`
- Username: `Elon`
- Family: `StrelaStealer`
