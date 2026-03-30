---
title: "PoisonedCredentials"
date: 2026-03-31
ctf: "CyberDefenders"
category: threat-hunting
difficulty: easy
tags: [cyberdefenders, llmnr, nbt-ns, credential-theft, smb]
excerpt: "Dieu tra poisoning qua LLMNR/NBT-NS de xac dinh rogue host, tai khoan bi lo va may muc tieu."
---

Imported and adapted from my original Notion notes for the CyberDefenders `PoisonedCredentials` challenge.

## Scenario

This challenge focuses on local name resolution abuse inside a Windows environment. A rogue machine answers poisoned resolution traffic, captures authentication attempts, and then uses the resulting access against another internal host.

## Core Concepts

- `LLMNR` and `NBT-NS` are local name resolution protocols.
- Neither provides strong authentication for responses.
- Attackers can poison these requests and capture hashes or relay credentials.

This is why the case matters operationally: it starts from something that looks small and noisy, then turns into real credential abuse.

## Key Findings

- Mistyped hostname query: `fileshaare`
- Rogue machine IP: `192.168.232.215`
- Second poisoned victim IP: `192.168.232.176`
- Compromised username: `janesmith`
- Host accessed through SMB: `AccountingPC`

## Analysis Walkthrough

### 1. Find the triggering typo

The mistyped query in the notes is:

- `fileshaare`

That mistake is what creates the opening for the rogue responder.

### 2. Identify the rogue system

By following the poisoned local resolution traffic, the rogue host is identified as:

- `192.168.232.215`

### 3. Track the impacted clients

The attack is not limited to one victim. The second host that receives poisoned responses is:

- `192.168.232.176`

### 4. Confirm credential abuse

From the SMB and NTLM flow in the notes:

- Compromised account: `janesmith`
- Accessed host: `AccountingPC`

The attack therefore moves from poisoned name resolution into usable internal access.

## Detection Ideas

- Alert on unusual LLMNR/NBT-NS responders on user VLANs
- Disable LLMNR and NBT-NS where possible
- Hunt for outbound SMB sessions following recent poisoned resolution traffic
- Look for repeated authentication attempts immediately after multicast name queries

## Answer Matrix

- Mistyped query: `fileshaare`
- Rogue IP: `192.168.232.215`
- Second poisoned host: `192.168.232.176`
- Compromised account: `janesmith`
- Accessed host: `AccountingPC`

## Notes

The full screenshot set from Notion still needs a dedicated local asset export step.
