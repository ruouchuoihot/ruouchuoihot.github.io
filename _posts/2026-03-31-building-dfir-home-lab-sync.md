---
title: "Building DFIR Home Lab"
date: 2026-03-31
category: forensics
tags: [notion, sync, dfir, homelab, forensics]
excerpt: "Imported and adapted from the Notion page on building a DFIR home lab."
---

Source page in Notion:

- [Building DFIR home lab](https://www.notion.so/2edbc35f72fd807fb35ff0f21684c241)

## Getting started with DFIR

DFIR (Digital Forensics & Incident Response) is one of the areas in cyber security where reading theory alone is rarely enough. To get useful practice, you need evidence to investigate: logs, memory dumps, disk images, compromised hosts, and system artifacts.

That is why a practical starting path is:

1. Build an analysis environment.
2. Prepare target systems.
3. Create attack scenarios.
4. Investigate the resulting evidence.
5. Expand the lab over time.

## Why DFIR feels overwhelming at first

- There is often no realistic incident data available when you first begin.
- The tooling landscape is crowded, and enterprise tools do not always match what is easy to install at home.

Because of that, the best approach is to learn the workflow first and optimize the toolset later.

## Practical roadmap

### 1. Build a forensic workstation

Start with a stable workstation VM where you can install your core analysis tools and roll back with snapshots when needed.

Suggested baseline:

- VMware Workstation as the hypervisor
- A Windows guest as the main analysis machine
- Ubuntu in WSL for Linux-based tooling

### 2. Prepare target systems

Set up one or more Windows VMs that will act as evidence sources. These machines become the place where you generate logs, disk artifacts, persistence, and memory activity to investigate later.

### 3. Create attack scenarios

You do not need highly advanced malware to begin. A good first scenario is one that leaves a clear chain of evidence:

- initial execution
- persistence
- file activity
- process activity
- network connections

Using a framework like MITRE ATT&CK helps you build repeatable scenarios that map well to defensive analysis.

### 4. Perform investigations

Once the environment exists, the real skill-building starts:

- collect evidence
- extract artifacts
- build timelines
- answer investigation questions
- write short incident summaries

### 5. Grow the lab gradually

You can start with a single Windows VM and basic tooling, then evolve the lab into a more complete DFIR and detection stack:

- domain controller
- additional victim hosts
- Elastic or Splunk
- Velociraptor
- security monitoring pipelines

## Suggested workstation setup

Recommended starter configuration for the Windows forensic workstation:

- Disk: 100 GB thin provisioned
- RAM: at least 4 GB
- vCPU: 2 or more
- Network: NAT

After installation:

- install VMware Tools
- create a fresh snapshot
- enable hidden items and file extensions
- create short working paths like `C:\Cases` and `C:\Tools`
- exclude evidence and tool directories from Defender when appropriate

## Tooling baseline

### Windows-side tools

- FTK Imager
- KAPE
- Arsenal Image Mounter
- Eric Zimmerman tools
- RegRipper
- Event Log Explorer
- Sysinternals
- Wireshark
- CyberChef
- PEStudio
- ExifTool

### Linux / WSL-side tools

- Volatility 3
- Plaso / log2timeline
- oletools
- pip-based utility tooling

## Minimal investigation workflow

When the workstation is ready, a practical case workflow looks like this:

1. Acquire memory and disk evidence.
2. Copy evidence into `C:\Cases`.
3. Analyze memory first, then disk.
4. Build a timeline.
5. Extract IOCs and summarize findings.

## Final note

The most useful DFIR home lab is not the one with the most tools. It is the one that gives you repeatable evidence, repeatable scenarios, and a repeatable investigation routine.
