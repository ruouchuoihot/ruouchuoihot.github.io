---
title: "BlueSky Ransomware Investigation"
date: 2026-03-31
ctf: "CyberDefenders"
category: forensics
difficulty: medium
tags: [cyberdefenders, network-forensics, malware-forensics, ransomware]
excerpt: "Phan tich chuoi tan cong BlueSky tu port scan, MSSQL compromise den ransomware deployment."
---

Imported and adapted from my original Notion notes for the CyberDefenders `BlueSky` challenge.

## Scenario

This case starts from a PCAP and grows into a full compromise chain:

1. Reconnaissance against exposed services
2. Access to MSSQL with valid credentials
3. OS command execution through the database server
4. Multi-stage payload delivery
5. Defense evasion and persistence
6. Credential dumping and host discovery
7. Final ransomware deployment

That is what makes the challenge useful. It is not just one malicious file. It is an intrusion timeline.

## Phase 1: Initial access

The first clear signal in the traffic is scanning activity from `87.96.21.84`. The target host exposes several services, including MSSQL on `1433`, which becomes the attacker’s way in.

From the TDS traffic in the PCAP, the recovered SQL access is:

- Username: `sa`
- Password: `cyb3rd3f3nd3r$`

Once valid access exists, the attacker enables:

- `xp_cmdshell`

This is the pivot point where the case moves from database access into full host compromise.

## Phase 2: Payload staging

The notes show a staged execution chain rather than a single one-shot payload:

- a base64 payload is written to disk
- a VBScript decodes it into an executable
- the executable is launched
- follow-up PowerShell scripts are fetched and executed

One of the important processes tied to the malicious activity is:

- Injected process: `winlogon.exe`

The first downloaded PowerShell scripts are:

- `http://87.96.21.84/checking.ps1`
- `http://87.96.21.84/del.ps1`

## Phase 3: Privilege awareness and defense evasion

The attacker checks whether the running context has administrative rights by testing the SID:

- `S-1-5-32-544`

The PowerShell chain then tampers with Windows Defender-related settings through these keys:

- `DisableAntiSpyware`
- `DisableRoutinelyTakingAction`
- `DisableRealtimeMonitoring`
- `SubmitSamplesConsent`
- `SpynetReporting`

The persistence mechanism created in the notes is the scheduled task:

- `\\Microsoft\\Windows\\MUI\\LPupdate`

In the original notes, the tactic answer tied to the second malicious script is:

- `TA0005`

## Phase 4: Credential dumping and lateral preparation

The post-exploitation scripts do not stop at local execution. They move into credential theft and lateral movement preparation.

Key artifacts from the notes:

- Credential dumping script: `Invoke-PowerDump.ps1`
- Dumped credential file: `hashes.txt`
- Host discovery file: `extracted_hosts.txt`

This is where the case becomes much more serious. The attacker is no longer just running commands on one host. They are building the data needed to move further across the environment.

## Phase 5: Ransomware impact

The final stage is ransomware delivery.

Recovered answers from the notes:

- Ransom note name: `# DECRYPT FILES BLUESKY #`
- Ransomware family: `BlueSky`

By the time the ransomware is visible, the attacker already has:

- service access
- command execution
- persistence
- weakened defenses
- dumped credentials
- lateral movement preparation

That is why this case is best understood as a full intrusion, not just a malware detonation.

## Recommended investigation flow

1. Review the scan behavior and exposed services.
2. Reconstruct the TDS stream to recover authentication and SQL commands.
3. Confirm `xp_cmdshell` enablement and host command execution.
4. Extract staged scripts and map what each script is responsible for.
5. Identify persistence, AV tampering, and cleanup actions.
6. Trace credential dumping and host targeting.
7. Correlate final payload execution with the ransomware artifacts.

## Answer Matrix

- Source IP: `87.96.21.84`
- SQL user: `sa`
- Password: `cyb3rd3f3nd3r$`
- Enabled setting: `xp_cmdshell`
- Injected process: `winlogon.exe`
- Downloaded script 1: `http://87.96.21.84/checking.ps1`
- Group SID: `S-1-5-32-544`
- Defender keys: `DisableAntiSpyware,DisableRoutinelyTakingAction,DisableRealtimeMonitoring,SubmitSamplesConsent,SpynetReporting`
- Downloaded script 2: `http://87.96.21.84/del.ps1`
- Persistence task: `\\Microsoft\\Windows\\MUI\\LPupdate`
- MITRE tactic: `TA0005`
- Dumping script: `Invoke-PowerDump.ps1`
- Credential file: `hashes.txt`
- Host file: `extracted_hosts.txt`
- Ransom note: `# DECRYPT FILES BLUESKY #`
- Family: `BlueSky`

## Notes

This writeup now carries the fuller analysis structure from my Notion notes. The screenshots still need a separate local asset export pass so the blog can host them permanently instead of relying on temporary Notion file links.
