---
title: "BlueSky Ransomware Investigation"
date: 2026-03-31
ctf: "CyberDefenders"
category: forensics
difficulty: medium
tags: [cyberdefenders, network-forensics, malware-forensics, ransomware]
excerpt: "Phan tich chuoi tan cong BlueSky tu port scan, SQL compromise den ransomware deployment."
---

Imported and adapted from my Notion notes for the CyberDefenders `BlueSky` challenge.

## Scenario

The case starts from a PCAP that shows reconnaissance, compromise of an exposed MSSQL service, privilege escalation, payload delivery, and finally ransomware execution inside the target environment.

## Key Findings

### Initial access

- Source IP performing the scan: `87.96.21.84`
- Targeted account: `sa`
- Discovered password: `cyb3rd3f3nd3r$`

The attacker brute forced or recovered the MSSQL `sa` credentials, then enabled `xp_cmdshell` to execute commands on the compromised host.

### Post-exploitation

- Setting enabled for command execution: `xp_cmdshell`
- Injected process used for elevated execution: `winlogon.exe`
- First downloaded script: `http://87.96.21.84/checking.ps1`
- Second downloaded script: `http://87.96.21.84/del.ps1`

The downloaded PowerShell chain disabled defenses, created persistence, removed traces, and prepared the host for credential theft and lateral movement.

### Privilege checks and persistence

- Group SID checked by the script: `S-1-5-32-544`
- Defender-related registry keys:
  `DisableAntiSpyware,DisableRoutinelyTakingAction,DisableRealtimeMonitoring,SubmitSamplesConsent,SpynetReporting`
- Scheduled task for persistence: `\\Microsoft\\Windows\\MUI\\LPupdate`
- MITRE tactic ID tied to the cleanup/persistence flow: `TA0005`

### Credential dumping and spread

- Credential dumping script: `Invoke-PowerDump.ps1`
- Dumped credential file: `hashes.txt`
- Discovered host list file: `extracted_hosts.txt`

The attacker used dumped credentials for SMB-based movement and then downloaded an additional payload.

### Ransomware stage

- Ransom note name: `# DECRYPT FILES BLUESKY #`
- Identified ransomware family: `BlueSky`

## Investigation Flow

1. Review the PCAP for scan behavior and MSSQL traffic.
2. Reconstruct TDS commands to identify account use and command execution.
3. Extract and inspect the dropped VBScript and PowerShell stages.
4. Map scheduled task creation, AV tampering, and cleanup activity.
5. Correlate the final payload with the observed ransomware behavior.

## Answers

- Source IP: `87.96.21.84`
- Username: `sa`
- Password: `cyb3rd3f3nd3r$`
- Enabled setting: `xp_cmdshell`
- Injected process: `winlogon.exe`
- Script 1: `http://87.96.21.84/checking.ps1`
- Group SID: `S-1-5-32-544`
- Defender keys: `DisableAntiSpyware,DisableRoutinelyTakingAction,DisableRealtimeMonitoring,SubmitSamplesConsent,SpynetReporting`
- Script 2: `http://87.96.21.84/del.ps1`
- Persistence task: `\\Microsoft\\Windows\\MUI\\LPupdate`
- MITRE tactic: `TA0005`
- Dumping script: `Invoke-PowerDump.ps1`
- Credential file: `hashes.txt`
- Host file: `extracted_hosts.txt`
- Ransom note: `# DECRYPT FILES BLUESKY #`
- Family: `BlueSky`
