---
title: "Using Splunk ES: Risk Framework, Security Domains va Investigation"
date: 2026-03-31
category: siem
tags: [splunk, siem, enterprise-security, risk-based-alerting, blue-team]
excerpt: "Tong hop ghi chu thuc hanh ve Splunk ES: risk framework, notable events, security domains va cach analyst dieu huong dieu tra."
---

This post is adapted from my original Notion page `Using Splunk ES`, but rewritten here as a native blog article with local screenshots.

## Why this note matters

After understanding what Splunk Enterprise Security is in theory, the next step is learning how analysts actually use it during triage and investigation.

The most useful parts from my notes are:

- the `risk framework`
- the way `notable events` are generated
- how `security domains` help pivot faster
- what kinds of activity analysts should investigate first

## Risk framework in ES

One of the most practical ideas in Splunk ES is that not every suspicious event should immediately be treated as the same level of incident. ES can accumulate risk over time and then raise the priority when the threshold becomes meaningful.

![Splunk ES risk framework](/assets/images/splunk/using-es-risk-framework.png)

In my notes, the main examples were:

- `ATT&CK Tactic Threshold Exceeded for Object Over Previous 7 Days`
- `Risk Threshold Exceeded for Object Over 24 Hour Period`

That model is useful because it turns separate low-signal observations into one investigation-worthy event.

## Risk notable logic

Risk-based detections become much more useful when they are tied to real thresholds and real object context.

![Splunk ES notable events and risk view](/assets/images/splunk/using-es-notables.png)

The important idea is:

- low-level observations contribute to a risk score
- the score is attached to a user, host, or other tracked object
- once the threshold is crossed, a higher-value notable can be created

For a SOC, this reduces alert noise compared to treating every single event as a standalone incident.

## Security domains inside ES

Another useful part of the notes is the way ES organizes investigation through `security domains`.

![Splunk ES security domain dashboard](/assets/images/splunk/using-es-security-domain.png)

The main domains I captured were:

- `Access`
- `Endpoint`
- `Network`
- `Identity`

These domains are helpful because they mirror how analysts actually think during triage.

### Access

The `Access` domain helps investigate:

- brute-force attempts
- privileged account activity
- access by rare or new accounts
- access by disabled or expired accounts
- access by unusual applications such as SSH or other remote access tooling

This is often one of the quickest places to validate suspicious authentication behavior.

### Endpoint

The `Endpoint` area is useful for:

- malware infections
- system configuration changes
- unusual process execution
- patch state and history
- uptime or system state anomalies

If an alert is tied to host behavior, this is usually where the investigation gets more concrete.

### Network

The `Network` domain gives context around:

- traffic patterns
- firewall activity
- IDS or IPS findings
- router and network device events
- suspicious communications between hosts

This becomes especially important when you are trying to connect authentication, host, and lateral movement behavior together.

### Identity

The `Identity` domain helps analysts examine:

- user context
- roles
- access profiles
- identity collections tied to other detections

Identity context matters because the same event can have a very different urgency depending on who performed it.

## How I would use this in practice

If I were using ES in a real SOC workflow, I would treat the investigation sequence like this:

1. start from the notable event
2. check the risk object and risk score history
3. pivot into the relevant security domain
4. decide whether the behavior is isolated, repeated, or part of a larger chain
5. enrich with asset and identity context before escalating

That flow is what makes ES more useful than a plain search interface. It gives structure to triage.

## Takeaway

For me, the real value of Splunk ES is not just `correlation search` by itself. It is the combination of:

- risk scoring
- notable events
- domain-based investigation
- context around assets and identities

That is what turns Splunk ES into an analyst workflow tool instead of just a dashboard collection.
