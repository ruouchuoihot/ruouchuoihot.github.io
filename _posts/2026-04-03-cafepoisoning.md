---
title: "CafePoisoning"
date: 2026-04-03
ctf: "Hack The Box"
category: forensics
tags: [hack-the-box, htb, dfir, wireshark, network-forensics, arp-poisoning]
---

![](/assets/images/htb/cafepoisoning/527d2172-92a8-48dd-b0b7-ae8f16cb8857.png " =324x120")

## Scenario

**While grabbing coffee at a cafe, I connected to public Wi-Fi and started a Windows update. The process never completed—it just kept running. As a digital forensics expert, can you help investigate?**

> Tag: DFIR

Challanges File:

* 1 File pcapng
* 1 Folder Triage `DESKTOP-TIT3D2T`

  ![](/assets/images/htb/cafepoisoning/abcd13cf-fbb3-422c-8322-03058de69a17.png " =244x77")

## Challanges

### 1. **The attacker performed a host discovery scan to identify devices on the network. Provide the start time of this activity in UTC.**

* Filter các gói ARP trong file pcapng, bắt đầu từ mốc thời gian `2025-03-10 21:07:05` có 1 loạt các gói broadcast ARP từ source devx-corp.net

  ![](/assets/images/htb/cafepoisoning/c1b6a3b8-5582-4279-ab58-c3a2d8daab6a.png " =1202x548")

```none
2025-03-10 21:07:05
```

### 2. **The attacker launched an ARP poisoning attack. Provide the start time in UTC**

* ARP poisoning thường xảy ra do attacker tạo ARP reply request giả để gán 1 IP của gateway hoặc victim với MAC của attacker => Network của victim cập nhật ARP table sai dẫn đến các gói tin giao tiếp sẽ bị man in the middle.
* Dấu hiệu detect bằng wireshark:
  * 1 IP xuất hiện với 2 MAC khác nhau trong gói ARP reply (opcode 2)
  * Lượng ARP gửi liên tục
  * sau đó layer 3/7 của victim (HTTP/DNS) đi unicast tới MAC của attacker

  ![](/assets/images/htb/cafepoisoning/c2b8fb59-7a25-41ad-a3bb-28cb3ec70323.png " =1882x636")
* IP 192.168.1.43 có ánh xạ chuẩn ban đầu: 192.168.1.43 is-at 1c:bf:ce:d9:b2:db lúc 21:07:07.
* Sau đó xuất hiện ARP reply giả từ 08:00:27:9b:8b:bd tự nhận "192.168.1.43 is-at 08:00:27:9b:8b:bd"

  => Attacker giả IP 192.168.1.43 bằng MAC 08:00:27:9b:8b:bd, khác với MAC hợp lệ 1c:bf:ce:d9:b2:db, và mốc thời gian đầu tiên của event này là 2025-03-10 21:07:33

```none
2025-03-10 21:07:33
```

### 3. **What MAC address did the attacker use during the ARP poisoning attack?**

* Từ câu 2, MAC address mà attacker dung để thực hiện ARP poisoning là 08:00:27:9b:8b:bd

```none
08:00:27:9b:8b:bd
```

### 4. **What is the IP address targeted by the attacker?**

* Từ câu 2, để ý trường target IP sẽ thấy được target IP là `192.168.1.90`

  ![](/assets/images/htb/cafepoisoning/dc618abb-29c7-4000-97e8-b86b78065660.png " =860x227")

```none
192.168.1.90
```

### 5. **Which spoofed domain was accessed by the compromised user?**

* Từ package của câu 2 cũng sẽ thấy domain mà attacker dùng là `devx-corp.net`
* Phân tích luồng package cũng sẽ thấy Reply của 192.168.1.90 tới domain này

  ![](/assets/images/htb/cafepoisoning/46e02542-16b7-40f7-a18c-dd887cf6399f.png " =609x178")

```none
devx-corp.net
```

### 6. **What was the legitimate IP address accessed by the compromised user before the DNS spoofing occurred?**

* Trong file pcap, các ip address đều k đúng đáp án, tuy nhiên nếu mò vào trong folder Triage, challange sẽ cho chúng ta các artifact về Google Chrome

  ![](/assets/images/htb/cafepoisoning/b00b23ea-66e8-4cb6-8c02-475458c3a169.png " =1304x308")
* Các file log của Chrome được viết dưới dạng sqlite database, sau khi research google ta tìm ra được 1 tool dùng để forensic cache của Google là ChromeCacheView
* Filter theo domain được attacker giả mạo là devx-corp.net ta sẽ thấy legitimate IPcủa domain này (137.50.21.6) và IP mà attacker giả mạo (192.168.1.11)

  ![](/assets/images/htb/cafepoisoning/6acddd23-77c5-4f10-bddf-e0d43c4366f9.png " =1880x740")

```none
137.50.21.6
```

### 7. **Identify the Wi-Fi network name (SSID) and the authentication algorithm used by the compromised user's connection.**

* Access vào folder chứa windows event log của Triage tại `C:\Windows\System32\winevt\logs`, ta sẽ thấy file Wlan-Autoconfig, đây là nơi chứa các log operation của wifi trong hđh Windows

  
:::info
  <https://www.dell.com/support/kbdoc/en-us/000150790/using-windows-logs-to-troubleshoot-wireless-issues-only-seen-at-customer-locations>

  :::
* Tại event 8001 ta sẽ thấy full các thông tin về SSID

  ![](/assets/images/htb/cafepoisoning/9283e5bd-9df3-445a-8b7b-bffc3b9500e3.png " =442x267")

```none
Cuppa Ce:WPA2-Personal
```

### 8. **Identify the download link used to fetch the malicious executable.**

* \

```none
192.168.1.11:5078
```

### **9. Identify the IP address and port number of the Command-and-Control (C2) server.**

\n

```none
s1rx-update.xyz
```

### 10. **The malicious executable is designed to check the C2 server before connecting. Provide the domain name of the C2 server.**

\n

```none
s1rx-update.xyz
```

### 11. **The malicious executable verifies privileges before execution to ensure it runs as administrator. Which Win32 API function is used for this check?**


```none
CheckTokenMembership()
```

### 12. **Which command was executed by the attacker to disable Windows Defender?**

* c
* c

  ```none
  if ($PSBoundParameters.ContainsKey('DisableRealtimeMonitoring')) {
            [object]$__cmdletization_value = ${DisableRealtimeMonitoring}
            $__cmdletization_methodParameter = [Microsoft.PowerShell.Cmdletization.MethodParameter]@{Name = 'DisableRealtimeMonitoring'; ParameterType = 'System.Boolean'; Bindings = 'In'; Value = $__cmdletization_value; IsValuePresent = $true}
          } else {
            $__cmdletization_methodParameter = [Microsoft.PowerShell.Cmdletization.MethodParameter]@{Name = 'DisableRealtimeMonitoring'; ParameterType = 'System.Boolean'; Bindings = 'In'; Value = $__cmdletization_defaultValue; IsValuePresent = $__cmdletization_defaultValueIsPresent}
          }
          $__cmdletization_methodParameters.Add($__cmdletization_methodParameter)
  ```
* c

```none
Set-MpPreference -DisableRealtimeMonitoring $true -Verbose
```

### 13. **A persistence mechanism was created by the attacker. Provide the registry key used for persistence.**


```none
HKCU\Control Panel\Desktop
```

\n ![](/assets/images/htb/cafepoisoning/c2fdecf2-fb91-4aca-ad8b-716ef0a9270f.png " =698x639")