---
title: "Splunk Dashboard Basics"
date: 2026-03-31
category: siem
tags: [splunk, dashboard, siem, blue-team]
excerpt: "Ghi chu ngan ve dashboard framework trong Splunk va tai sao dashboard van quan trong voi analyst workflow."
---

This is a short note adapted from my `Splunk Dashboard` page.

## Why dashboards still matter

Dashboards are not a replacement for investigation, but they are useful because they:

- summarize the state of a dataset quickly
- surface anomalies worth clicking into
- help analysts understand trends without writing every search from scratch
- support repeatable SOC views for triage and reporting

## Dashboard framework note

My original note captured a simple point:

- there are multiple ways to create visualizations and dashboards in Splunk
- `Classic Splunk Dashboard` is XML-based
- XML dashboards are useful, but the UI layer is more limited than newer approaches

Even though this note is small, it matters because dashboard design affects how easily analysts can move from visibility to action.

## What I care about when building dashboards

If I continue expanding this part of the blog, the dashboard topics I want to cover are:

- what makes a dashboard useful for a SOC analyst
- when to use dashboards vs direct SPL
- how to design panels that support investigation instead of vanity metrics
- how dashboards relate to ES, notable events, and security domains

For now, this note stays as a lightweight checkpoint in the broader Splunk learning path.
