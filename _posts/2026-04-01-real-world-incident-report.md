---
layout: post
title: "Real-world Incident Report"
date: 2026-04-01
categories: [dfir]
tags: [dfir]
---

# **Real-world Incident Report**

# **Executive Summary**

- `Incident ID`: INC2019-0422-022
- `Incident Severity`: High (P2)
- `Incident Status`: Resolved
- `Incident Overview`: On the night of `April 22, 2019`, at precisely `01:05:00`, SampleCorp's Security Operations Center (SOC) detected unauthorized activity within the internal network, specifically through anomalous process initiation and suspicious-looking PowerShell commands. Leveraging the lack of robust network access controls and two security vulnerabilities, the unauthorized entity successfully gained control over the following nodes within SampleCorp's infrastructure:
- `Key Findings`: Owing to insufficient network access controls, the unauthorized entity was assigned an internal IP address by simply connecting their computer to an Ethernet port within a SampleCorp office. Investigative efforts revealed that the unauthorized entity initially compromised `WKST01.samplecorp.com` by exploiting a vulnerable version of `Acrobat Reader`. Additionally, the entity exploited a `buffer overflow vulnerability`, this time in a proprietary application developed by SampleCorp, to further penetrate the internal network. While no widespread data exfiltration was detected, likely owing to the rapid intervention by the SOC and DFIR teams, the unauthorized access to both `WKST01.samplecorp.com` and `HR01.samplecorp.com` raise concerns. As a result, both company and client data should be regarded as potentially compromised to some extent.
- `Immediate Actions`: SampleCorp's SOC and DFIR teams exclusively managed the incident response procedures, without the involvement of any external service providers. Immediate action was taken to isolate the compromised systems from the network through the use of VLAN segmentation. To facilitate a comprehensive investigation, the SOC and DFIR teams gathered extensive data. This included getting access to network traffic capture files. Additionally, all affected systems were plugged to a host security solution. As for event logs, they were automatically collected by the existing Elastic SIEM solution.
- `Stakeholder Impact`:
# **Technical Analysis**

### **Affected Systems & Data**

Owing to insufficient network access controls, the unauthorized entity was assigned an internal IP address by simply connecting their computer to an Ethernet port within a SampleCorp office.

The unauthorized entity successfully gained control over the following nodes within SampleCorp's infrastructure:

- `WKST01.samplecorp.com`: This is a development environment that contains proprietary source code for upcoming software releases, as well as API keys for third-party services. The unauthorized entity did navigate through various directories, raising concerns about intellectual property theft and potential abuse of API keys.
- `HR01.samplecorp.com`: This is the Human Resources system that houses sensitive employee and partner data, including personal identification information, payroll details, and performance reviews. Our logs indicate that the unauthorized entity did gain access to this system. Most concerning is that an unencrypted database containing employee Social Security numbers and bank account details was accessed. While we have no evidence to suggest data was extracted, the potential risk of identity theft and financial fraud for employees is high.
### **Evidence Sources & Analysis**

**WKST01.samplecorp.com**

On the night of `April 22, 2019`, at exactly `01:05:00`, SampleCorp's Security Operations Center (SOC) identified unauthorized activity within the internal network. This was detected through abnormal parent-child process relationships and suspicious PowerShell commands, as displayed in the following screenshot.

From the logs, PowerShell was invoked from `cmd.exe` to execute the contents of a remotely hosted script. The IP address of the remote host was an internal address, `192.168.220.66`, indicating that an unauthorized entity was already present within the internal network.

![image](/assets/images/dfir/31fbc35f-72fd-814f-ad37-d6536e2e521a.png)

The earliest signs of malicious command execution point to `WKST01.samplecorp.com` being compromised, likely due to a malicious email attachment with a suspicious file named `cv.pdf` for the following reasons:

- The user accessed the email client `Mozilla Thunderbird`
- A suspicious file `cv.pdf` was opened with Adobe Reader 10.0, which is outdated and vulnerable to security flaws.
- Malicious commands were observed immediately following these events.
![image](/assets/images/dfir/31fbc35f-72fd-81ae-9a2b-ce3298a10d7f.png)

Additionally, `cmd.exe` and `powershell.exe` were spawned from `wmiprvse.exe`.

![image](/assets/images/dfir/31fbc35f-72fd-811c-9760-d6724a072486.png)

![image](/assets/images/dfir/31fbc35f-72fd-81e4-8c5b-c885994e25ab.png)

As already mentioned, the unauthorized entity then executed specific PowerShell commands.

![image](/assets/images/dfir/31fbc35f-72fd-816b-b82c-f50a0ee89dce.png)

**Brief Analysis of 192.168.220.66**

From the logs, we identified four hosts on the network segment with corresponding IP addresses and hostnames. The host `192.168.220.66`, previously observed in the logs of `WKST01.samplecorp.com`, confirms the presence of an unauthorized entity in the internal network.

The below table is the result of a SIEM query that aimed to identify all instances of command execution initiated from `192.168.220.66`, based on data from `WKST01.samplecorp.com`.

The results suggest that the unauthorized entity has successfully infiltrated the hosts: `WKST01.samplecorp.com` and `HR01.samplecorp.com`.

**HR01.samplecorp.com**

`HR01.samplecorp.com` was investigated next, as the unauthorized entity, `192.168.220.66`, was shown to establish a connection with `HR01.samplecorp.com` at the earliest possible moment in the packet capture.

![image](/assets/images/dfir/31fbc35f-72fd-81c7-90cc-c5ffa431a18a.png)

Network traffic details suggest a buffer overflow attempt on the service running at port `31337` of `HR01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-814c-baee-c6fb6275fa26.png)

The network traffic was exported as raw binary for further analysis.

![image](/assets/images/dfir/31fbc35f-72fd-8183-ac2e-d962eee1f997.png)

The extracted binary was analyzed in a shellcode debugger, `scdbg`.

`Scdbg` reveals that the shellcode will attempt to initiate a connection to `192.168.220.66` at port `4444`. This confirms that there has been an attempt to exploit a service running on port `31337` of `HR01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-81ac-adaa-cd2c31a3f179.png)

A search for network connections between `HR01.samplecorp.com` and the unauthorized entity was conducted using the aforementioned traffic capture file. Results revealed connections back to the unauthorized entity on port `4444`. This indicates that the unauthorized entity successfully exploited a buffer overflow vuln to gain command execution on `HR01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-8165-85f6-c3b98354cc5d.png)

The depth of the technical analysis can be tailored to ensure that all stakeholders are adequately informed about the incident and the actions taken in response. While we've chosen to keep the investigation details concise in this module to avoid overwhelming you, it's important to note that in a real-world situation, every claim or statement would be backed up with robust evidence.

### **Indicators of Compromise (IoCs)**

- `C2 IP`: 192.168.220.66
- `cv.pdf` (SHA256): ef59d7038cfd565fd65bae12588810d5361df938244ebad33b71882dcf683011
### **Root Cause Analysis**

Insufficient network access controls allowed the unauthorized entity access to SampleCorp's internal network.

The primary catalysts for the incident were traced back to two significant vulnerabilities. The first vulnerability stemmed from the continued use of an outdated version of Acrobat Reader, while the second was attributed to a buffer overflow issue present within a proprietary application. Compounding these vulnerabilities was the inadequate network segregation of crucial systems, leaving them more exposed and easier targets for potential threats. Additionally, there was a notable gap in user awareness, evident from the absence of comprehensive training against phishing tactics, which could have served as the initial entry point for the attackers.

### **Technical Timeline**

- Initial Compromise
- Lateral Movement
- Data Access & Exfiltration
- C2 Communications
- Malware Deployment or Activity
- Containment Times
- Eradication Times
- Recovery Times
### **Nature of the Attack**

In this segment, we should meticulously dissect the modus operandi of the unauthorized entity, shedding light on the specific tactics, techniques, and procedures (TTPs) they employed throughout their intrusion. For instance, let's dive into the methods the SOC team used to determine that the unauthorized entity utilized the Metasploit framework in their operations.

**Detecting Metasploit**

To better understand the tactics and techniques of the unauthorized entity, we delved into the malicious PowerShell commands executed.

Particularly, the one shown in the following screenshot.

![image](/assets/images/dfir/31fbc35f-72fd-81f3-a951-c9f03acebdbb.png)

Upon inspection, it became clear that double encoding was used, likely as a means to bypass detection mechanisms. The SOC team successfully decoded the malicious payload, revealing the exact PowerShell code executed within the memory of `WKST01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-815b-b2ca-c347a6120fbd.png)

By leveraging open source intelligence, our SOC team determined that this PowerShell code is probably linked to the [Metasploit](https://github.com/rapid7/metasploit-framework) post-exploitation framework.

![image](/assets/images/dfir/31fbc35f-72fd-8115-950c-de0663598689.png)

To support our hypothesis that `Metasploit` was used, we dived deeper into the detected shellcode. We specifically exported the packet bytes containing the shellcode (as `a.bin`) and subsequently submitted them to VirusTotal for evaluation.

![image](/assets/images/dfir/31fbc35f-72fd-8144-895d-e599a041d1de.png)

![image](/assets/images/dfir/31fbc35f-72fd-81aa-9d3b-f407938d08c7.png)

![image](/assets/images/dfir/31fbc35f-72fd-817b-b3e4-f78d342c5693.png)

The results from VirusTotal affirmed our suspicion that `Metasploit` was in play. Both `metacoder` and `shikata` are intrinsically linked to the Metasploit-generated shellcode.

---

# **Impact Analysis**

In this segment, we should dive deeper into the initial stakeholder impact analysis presented at the outset of this report. Given the company's unique internal structure, business landscape, and regulatory obligations, it's crucial to offer a comprehensive evaluation of the incident's implications for every affected party.

---

# **Response and Recovery Analysis**

### **Immediate Response Actions**

**Revocation of Access**

- `Identification of Compromised Accounts/Systems`: Using Elastic SIEM solution, suspicious activities associated with unauthorized access were flagged on `WKST01.samplecorp.com`. Then, a combination of traffic and log analysis uncovered unauthorized access on `HR01.samplecorp.com` as well.
- `Timeframe`: Unauthorized activities were detected at `April 22, 2019, 01:05:00`. Access was terminated by `April 22nd, 2019, 03:43:34` upon firewall rule update to block the C2 IP address.
- `Method of Revocation`: Alongside the firewall rules, Active Directory policies were applied to force log-off sessions from possibly compromised accounts. Additionally, affected user credentials were reset and accessed API keys were revoked, further inhibiting unauthorized access.
- `Impact`: Immediate revocation of access halted potential lateral movement, preventing further system compromise and data exfiltration attempts.
**Containment Strategy**

- `Short-term Containment`: As part of the initial response, VLAN segmentation was promptly applied, effectively isolating `WKST01.samplecorp.com` and `HR01.samplecorp.com` from the rest of the network, and hindering any lateral movement by the threat actor.
- `Long-term Containment`: The next phase of containment involves a more robust implementation of network segmentation, ensuring specific departments or critical infrastructure run on isolated network segments, and robust network access controls, ensuring that only authorized devices have access to an organization's internal network. Both would reduce the attack surface for future threats.
- `Effectiveness`: The containment strategies were successful in ensuring that the threat actor did not escalate privileges or move to adjacent systems, thus limiting the incident's impact.
### **Eradication Measures**

**Malware Removal**

- `Identification`: Suspicious processes were flagged on the compromised systems, and a deep dive forensic examination revealed traces of the `Metasploit` post-exploitation framework, which was further confirmed by `VirusTotal` analysis.
- `Removal Techniques`: Using a specialized malware removal tool, all identified malicious payloads were eradicated from `WKST01.samplecorp.com` and `HR01.samplecorp.com`.
- `Verification`: Post-removal, a secondary scan was initiated, and a heuristic analysis was performed to ensure no remnants of the malware persisted.
**System Patching**

