---
layout: page
title: About
---

## Xin chao!

Minh la **ruouchuoihot**, mot Blue Team enthusiast va SOC Analyst.

Blog nay la noi minh chia se:

- **Defensive CTF Writeups**: Giai thich chi tiet cach giai cac challenge Blue Team
- **Kien thuc bao mat**: SOC, SIEM, DFIR, Threat Hunting
- **Tools & Techniques**: Cac cong cu va ky thuat phong thu

## Focus Areas

- **SOC Operations**: Alert triage, investigation, escalation
- **SIEM**: Splunk, ELK Stack, log analysis
- **Digital Forensics & Incident Response (DFIR)**: Memory, disk, network forensics
- **Threat Hunting**: Proactive detection, MITRE ATT&CK
- **Malware Analysis**: Static va dynamic analysis
- **Network Security**: IDS/IPS, traffic analysis

## Toolset

| Loai | Tools |
| --- | --- |
| SIEM | Splunk, ELK, Wazuh |
| Forensics | Volatility, FTK Imager, Autopsy |
| Network | Wireshark, Suricata, Zeek |
| Malware | YARA, Cuckoo, Any.Run |
| Endpoint | Velociraptor, OSQuery |
| Framework | MITRE ATT&CK, Cyber Kill Chain |

## Certifications

{% if site.certifications and site.certifications.size > 0 %}
<div class="cert-grid">
  {% for cert in site.certifications %}
    <a class="cert-card" href="{{ cert.url }}" target="_blank" rel="noreferrer">
      <span class="cert-issuer">{{ cert.issuer }}</span>
      <strong class="cert-name">{{ cert.name }}</strong>
      {% if cert.issued %}
        <span class="cert-meta">Issued: {{ cert.issued }}</span>
      {% endif %}
      {% if cert.note %}
        <span class="cert-meta">{{ cert.note }}</span>
      {% endif %}
    </a>
  {% endfor %}
</div>
{% else %}
Chua co certification nao duoc them. Ban co the cap nhat danh sach trong `_config.yml` bang ten cert va link Credly.
{% endif %}

## Contact

- GitHub: [github.com/ruouchuoihot](https://github.com/ruouchuoihot)
