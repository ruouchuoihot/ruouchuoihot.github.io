---
title: "PoisonedCredentials"
date: 2026-03-31
ctf: "CyberDefenders"
category: threat-hunting
difficulty: easy
tags: [cyberdefenders, llmnr, nbt-ns, credential-theft, smb]
excerpt: "Dieu tra poisoning qua LLMNR/NBT-NS de xac dinh rogue host, tai khoan bi lo va may muc tieu."
---

Imported and adapted from my Notion notes for the CyberDefenders `PoisonedCredentials` challenge.

## Scenario

This challenge focuses on a classic local network poisoning scenario. A rogue system answers LLMNR/NBT-NS name resolution traffic, captures authentication attempts, and uses the leaked credentials to access another host over SMB.

## Core Concepts

- `LLMNR` and `NBT-NS` are local name resolution protocols.
- Neither provides strong authentication for responses.
- Attackers can poison these requests and capture hashes or relay credentials.

## Key Findings

- Mistyped hostname query: `fileshaare`
- Rogue machine IP: `192.168.232.215`
- Second poisoned victim IP: `192.168.232.176`
- Compromised username: `janesmith`
- Host accessed through SMB: `AccountingPC`

## Why it matters

The interesting part here is not just the poisoned response. The important observation is that the attack moves from simple local name resolution abuse into credential capture and authenticated SMB access.

## Detection Ideas

- Alert on unusual LLMNR/NBT-NS responders on user VLANs
- Disable LLMNR and NBT-NS where possible
- Hunt for outbound SMB sessions following recent poisoned resolution traffic
- Look for repeated authentication attempts immediately after multicast name queries

## Answers

- Mistyped query: `fileshaare`
- Rogue IP: `192.168.232.215`
- Second poisoned host: `192.168.232.176`
- Compromised account: `janesmith`
- Accessed host: `AccountingPC`
