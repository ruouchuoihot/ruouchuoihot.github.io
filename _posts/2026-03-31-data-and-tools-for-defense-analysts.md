---
title: "Data va Tools for Defense Analysts trong Splunk"
date: 2026-03-31
category: siem
tags: [splunk, siem, blue-team, soc, threat-intelligence]
excerpt: "Tong hop cac nguon data va cong cu ma defense analyst dua vao khi lam viec voi Splunk: auth, proxy, AV, firewall, endpoint, CTI va metadata."
---


## The SOC view of the stack

One useful theme from the note is that a defense analyst does not work with Splunk as a single isolated tool. Splunk sits in a wider SOC workflow with SIEM, automation, telemetry, and threat intelligence.

![SOC tool overview](/assets/images/splunk/defense-analyst-soc-overview.png)

![SOC stack and analyst workflow](/assets/images/splunk/defense-analyst-soc-stack.png)

In this setup:

- `Splunk Enterprise Security` acts as the SIEM
- `Splunk SOAR` helps automate repeatable response steps
- analysts use detections, notable events, and context to investigate suspicious activity

## Why notable events matter

One line from the note is still worth repeating:

> The beauty of a notable event is that it can highlight specific events for analysts that have a higher likelihood of being malicious.

That is why notables matter so much in a real SOC. They reduce the time spent searching through lower-priority noise.

## Core data sources for defense analysts

The strongest part of the note is the breakdown of what kinds of data analysts should care about.

### Network information

Network data helps analysts understand communications, flows, and potential movement across the environment.

Examples include:

- NetFlow and flow logs
- firewall events
- IDS or IPS alerts
- packet capture after an incident
- DPI for real-time packet inspection

This is critical when reconstructing suspicious traffic or confirming lateral movement.

### Authentication information

Authentication data is one of the most important foundations for investigation.

![Authentication and identity context](/assets/images/splunk/defense-analyst-authentication.png)

Useful sources include:

- Active Directory
- LDAP
- RADIUS
- TACACS+
- Okta or Azure AD
- VPN logs
- AWS CloudTrail

These logs help answer:

- who authenticated
- from where
- to what
- under which identity or role

### Proxy and gateway information

Web proxies and gateways give valuable context around:

- websites accessed by a user
- hidden traffic patterns
- suspicious downloads
- browsing activity tied to later malicious behavior

This data is often extremely useful when investigating phishing, malware delivery, or suspicious outbound traffic.

### AV and endpoint security logs

Anti-virus and endpoint protection logs are strong sources of evidence during incident response.

![AV logs and endpoint detections](/assets/images/splunk/defense-analyst-av-logs.png)

These logs can support:

- malware signature matches
- quarantine or remediation history
- suspicious files or hashes
- host-level infection timelines

### Firewall and network controls

Firewall logs help analysts identify:

- unusual allowed traffic
- unusual connections across protected zones
- unexpected protocol activity
- repeated denies from a single source
- evidence of scanning and follow-on access

### Endpoint information

Endpoint logs can show:

- failed logins
- privilege escalation attempts
- process creation
- file or system access anomalies
- behaviors linked to insider threat or policy violations

### Server and application logs

Important assets produce the telemetry that often confirms what actually happened:

- unusual communications
- application errors
- service changes
- process execution
- account activity
- privileged actions

## Threat intelligence inside the workflow

The note also ties this back to `Cyber Threat Intelligence`.

Two levels are especially important:

- `Tactical intelligence`: IPs, URLs, hashes, signatures, and other IOCs
- `Operational intelligence`: techniques, procedures, and attacker behavior patterns

Operational intelligence is especially useful for:

- threat hunting
- understanding the extent of compromise
- mapping behavior to MITRE ATT&CK

## Why this matters in Splunk

The reason all of this belongs in a Splunk learning path is simple:

- Splunk is only as good as the data being ingested
- detections are only as useful as the context surrounding them
- analysts need both telemetry and framework context to investigate well

## Practical takeaway

For me, this note reinforces one core lesson:

A good defense analyst is not only someone who can search logs. A good analyst knows:

- which data sources matter
- which tools add useful context
- how to pivot from one telemetry type to another
- how to combine detections with identity, asset, and intelligence context

That is what turns Splunk from a search interface into a real investigation platform.
