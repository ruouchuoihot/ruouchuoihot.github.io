---
title: "Splunk ES Overview"
date: 2026-03-31
category: siem
tags: [splunk, siem, enterprise-security, detection, blue-team]
excerpt: "Tong hop cac ghi chu ve Splunk Enterprise Security: correlation search, notable events, CIM, dashboard va incident workflow."
---


## What Splunk ES is

`Splunk Enterprise Security (ES)` is a premium SIEM application built on top of Splunk Enterprise. In practice, it gives a SOC a structured layer for:

- threat detection
- investigation
- incident tracking
- response coordination
- security reporting

The important point is that ES is not separate from the Splunk data platform. It works on the data already onboarded into Splunk, then adds security-focused logic on top.

## Main functional areas

The original notes break ES into three practical functions.

### 1. Perimeter Defense

This part helps analysts detect risky users, assets, and suspicious activities using:

- threat intelligence context
- posture dashboards
- vulnerability-style signals
- prohibited traffic monitoring
- unexpected process visibility

It is the "what should worry us first?" layer.

### 2. Preventative Analysis

This layer focuses on detection logic and behavioral analytics, including:

- anomaly detection
- pattern matching
- traffic analysis
- statistical analysis

This is where correlation search becomes especially important because it turns raw events into detections that matter operationally.

### 3. Breach Response

This layer supports the analyst after detection:

- incident tracking
- investigation timelines
- asset and identity investigation
- forensic context
- auditing and reporting

This is the part that makes ES feel like more than dashboards. It becomes a working SIEM instead of just a log search UI.

## Correlation search

`Correlation search` is the core of Splunk ES.

It allows analysts to:

- search for malicious patterns in near real time
- run scheduled detections
- create notable events when conditions match
- trigger actions such as alerts, scripts, or workflow updates

If the base telemetry is weak, ES will stay weak too. That is why ES success depends on both good data onboarding and good detection logic.

## ES workflow

The workflow from the notes can be simplified like this:

1. data comes from sources into Splunk indexers
2. data is normalized with CIM and data models
3. correlation searches run on that data
4. matches create alerts and `notable events`
5. analysts investigate through ES dashboards

This is the cleanest mental model for understanding how ES turns logs into incident handling.

## Notable events

`Notable events` are one of the most useful ES concepts.

They are created when a correlation search matches suspicious activity. Those events are then stored in the `notable` index and used by investigation dashboards.

Important characteristics from the notes:

- they hold incident context such as source, tags, event type, and raw data
- they help drive analyst triage
- urgency depends on `assets` and `identities` in the environment
- asset and identity context is maintained through lookup and KV store structures

That urgency model matters because the same event can be more or less serious depending on who or what is affected.

## Dashboard and data model concepts

The notes also highlight a few core building blocks behind ES:

- `CIM` for normalization
- accelerated data models for detection and dashboards
- KV store for workflow state, lookups, threat intel collections, and incident metadata

This matters because many ES dashboards and detections depend on these layers being configured correctly. If CIM mapping is poor, detections and reports can become unreliable.

## Kill chain view

Another useful point in the notes is how ES can be used across the attack lifecycle:

- delivery
- exploitation
- installation
- command and control
- follow-on impact

The value here is not just seeing one isolated alert. ES helps connect the attacker journey so defenders can reduce dwell time and investigate faster.

## Why ES is useful in a SOC

From a practical Blue Team point of view, ES is valuable because it helps convert:

- telemetry
- detections
- context
- urgency

into something analysts can actually triage and investigate in a repeatable way.

That is why I treat ES as the operational SIEM layer in the Splunk stack, not just an add-on dashboard pack.
