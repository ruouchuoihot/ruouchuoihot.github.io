---
title: "PsExec Hunt"
date: 2026-03-31
ctf: "CyberDefenders"
category: soc
difficulty: medium
tags: [cyberdefenders, psexec, lateral-movement, smb, windows]
excerpt: "Theo doi lateral movement bang PsExec qua SMB de xac dinh host dau tien, service va cac share duoc dung."
---

Imported and adapted from my original Notion notes for the CyberDefenders `PsExec Hunt` challenge.

## Scenario

The traffic captures a PsExec-based lateral movement chain over SMB. The objective is to reconstruct which host was compromised first, which credentials were used, and how the attacker pivoted through the network.

This is a good case study because PsExec leaves a recognizable sequence across authentication, share access, service deployment, and follow-on movement.

## Key Findings

- Initial compromised IP: `10.0.0.130`
- First pivot hostname: `SALES-PC`
- Username used for authentication: `ssales`
- Service executable dropped on target: `PSEXESVC.EXE`
- Share used to install the service: `ADMIN$`
- Share used for communication: `IPC$`
- Next pivot target hostname: `Marketing-PC`

## Analysis Walkthrough

### 1. Find the first compromised machine

The earliest meaningful SMB activity points back to:

- `10.0.0.130`

### 2. Recover host and account context

From the session setup flow:

- First pivot host: `SALES-PC`
- Username: `ssales`

### 3. Confirm PsExec deployment

The service executable and shares in the notes are:

- Service: `PSEXESVC.EXE`
- Install share: `ADMIN$`
- Communication share: `IPC$`

### 4. Track further movement

The attacker then attempts to pivot toward:

- `Marketing-PC`

## Investigation Notes

PsExec leaves a very recognizable pattern:

1. SMB authentication to the remote host
2. Service binary copy over `ADMIN$`
3. Service control and named-pipe style coordination over `IPC$`
4. Follow-on execution and possible second-stage lateral movement

## Answer Matrix

- Initial access IP: `10.0.0.130`
- First pivot host: `SALES-PC`
- Username: `ssales`
- Service executable: `PSEXESVC.EXE`
- Install share: `ADMIN$`
- Communication share: `IPC$`
- Further pivot host: `Marketing-PC`
