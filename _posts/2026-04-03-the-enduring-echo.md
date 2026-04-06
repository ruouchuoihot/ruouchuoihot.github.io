---
title: "The Enduring Echo"
date: 2026-04-03
ctf: "Hack The Box"
category: incident-response
difficulty: medium
tags: [hack-the-box, htb, dfir, windows-forensics, kape, splunk, lateral-movement]
excerpt: "Thực chiến triage bằng KAPE và Timeline Explorer để săn lùng dấu vết Lateral Movement qua WMI, Pivot PortProxy và cơ chế Persistence bằng Scheduled Tasks."
---

# The Enduring Echo

> LeStrade ném cho Watson một cục disk image dính đầy artifact nóng hổi. Đây là một trong những điểm breach trọng yếu, con máy chủ đang rú lên vì hoạt động CPU bất thường và một mớ anomaly bầy hầy trong process logs.

> [!TIP]
> Workflow thường dùng: KAPE First (quét triage nóng trước khi deep dive).

---

## Phân tích Chuyên sâu (Walkthrough)

### 1. Phân tích Command Line ban đầu của Attacker

> What was the first (non cd) command executed by the attacker on the host?

Môi trường thực chiến: Sử dụng `Timeline Explorer` để load file log event thần thánh KAPE đã thu thập ở `Results\EventLogs\20250923033121_EvtxECmd_Output.csv`.

Chạy filter lọc nhiễu các process lành tính để trơ ra các artifact từ attacker:

**Dùng Timeline Explorer:**
```text
[Channel] = 'Security' And Not Contains([Executable Info], 'backgroundTaskHost.exe') And Not Contains([Executable Info], 'RuntimeBroker.exe') And Not Contains([Executable Info], 'sppsvc.exe') And Not Contains([Executable Info], 'fontdrvhost.exe') And Not Contains([Executable Info], 'LocalService') And Not Contains([Executable Info], 'taskhostw.exe') And Not Contains([Executable Info], 'userinit.exe') And Not Contains([Executable Info], 'ctfmon.exe') And Not Contains([Executable Info], 'cd') And Contains([Executable Info], 'cmd') And [Event Id] = 4688
```

Hoặc **Nếu chạy qua Splunk**:
```spl
| inputlookup htb_chal2_eventlog.csv | search (EventId=4688) | table TimeCreated, Computer, PayloadData2, PayloadData3, PayloadData5, ExecutableInfo | rename PayloadData2 as PID,PayloadData3 as PPID, PayloadData5 as User, ExecutableInfo as Process | search User="Target User: HEISEN-9-WS-6\Werni"
| search NOT (Process IN ("*backgroundTaskHost.exe*", "*RuntimeBroker.exe*", "*sppsvc.exe*","*fontdrvhost.exe*","*LocalService*", "*taskhostw.exe*", "*userinit.exe*","*ctfmon.exe*"))
| search Process="*cmd.exe*"
```

Bản chất của các query này là dìm hàng các process tự sinh (như `RuntimeBroker`), và nhặt lên những process `cmd.exe` bị gọi với Event ID `4688` (khi Process mới thành hình).

![Splunk Process Logging](/assets/images/htb/the-enduring-echo/92553d72-2546-4a98-bdfb-e5d2666501b8.png)

Tua tới mốc `2025-08-24 22:51:09`, lòi ra một event đượm mùi Lateral Movement. Mấy cái event trước đó chỉ mấp mé lướt OneDrive với Vmware, đồ "nhà quê", không đáng bận tâm.

![Lateral Movement Event](/assets/images/htb/the-enduring-echo/7c0a831c-4fc8-4e74-9500-f36ae201dce0.png)

Giãi mã raw log này:
- **Time:** `2025-08-24 22:51:09`
- **Event ID:** `4688`
- **Computer:** `Heisen-9-WS-6`
- **Parent process:** `C:\Windows\System32\wbem\WmiPrvSE.exe`
- **Process:** `C:\Windows\System32\cmd.exe cmd.exe /Q /c systeminfo 1> \\127.0.0.1\ADMIN$\__1756075857.955773 2>&1`

Attacker vừa luồn lệnh dưới quyền WMI. Câu lệnh nguyên thủ ban đầu:

```
systeminfo
```

### 2. Định danh Target Parent Process 

> Which parent process (full path) spawned the attacker's commands?

Bóc trần thẳng từ kết quả câu trên, kẻ giật dây (Parent Process) chính là anh bạn thân thuộc quá độ của các cuộc khai thác nội bộ:

```
C:\Windows\System32\wbem\WmiPrvSE.exe
```

### 3. Công cụ Remote Execution tàng hình (Lateral Movement Tool)

> Which remote-execution tool was most likely used for the attack?

Bởi vì challenge giới hạn trong rổ artifacts của victim, mình không sờ tận tay cái tool mà gã hacker cầm. Thế nhưng, cái mùi `WmiPrvSE.exe` đẻ ra `cmd.exe` chạy ngầm, rồi dump output ngược qua `ADMIN$` share `\\127.0.0.1\ADMIN$\__...`, là signature 100% thuộc về `wmiexec.py` nức tiếng của đội ngũ Impacket.

```
wmiexec.py
```

### 4. Đào tung IP Attacker qua Event 4624

> What was the attacker's IP address?

Lấy mốc thời gian vừa nện `2025-08-24 22:51:09` làm cọc, ta lọc ngược về Event ID `4624` (Successful Logon).
Khui ra một đợt login nổ ra sớm hơn vài giây lúc `2025-08-24 22:50:58`, mang theo cục remote IP to tướng:

```
10.129.242.110
```

### 5. Cấy Persistance - Bước khởi thủy (Scheduled Tasks)

> What is the first element in the attacker's sequence of persistence mechanisms?

Nắm thóp được trò gọi lệnh qua `WmiPrvSE.exe`, quay lại rà gắt bộ lọc cột Parent Process bằng chính `WmiPrvSE.exe`.

![WmiPrvSE Logs](/assets/images/htb/the-enduring-echo/170376f9-ab8a-430f-b879-b154ef027075.png)

Ngay tại mốc `2025-08-24 23:03:50`, chộp được dòng lệnh cực "Persistence":
```cmd
C:\Windows\System32\cmd.exe cmd.exe /Q /c schtasks /create /tn "SysHelper Update" /tr "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\Users\Werni\Appdata\Local\JM.ps1" /sc minute /mo 2 /ru SYSTEM /f 1> \\127.0.0.1\ADMIN$\__1756076432.886685 2>&1
```

Phân tích: Hắn cắm một Scheduled Task tự xưng danh "SysHelper Update", ngầm chạy con powershell script `JM.ps1` ẩn dạng theo từng nấc 2 phút, nã bằng quyền tột đỉnh `SYSTEM`. Rõ như ban ngày.

```
SysHelper Update
```

### 6. Endpoint chứa cái Script ngầm

> Identify the script executed by the persistence mechanism.

Giật thẳng từ ruột cái Scheduled Tasks bên trên:

```
C:\Users\Werni\Appdata\Local\JM.ps1
```

### 7. Truy lại User Độc hại được đúc bằng Event 4720

> What local account did the attacker create?

Filter dò dẫm con hàng Event Id `4720` (A user account was created). Ở máy chủ victim `Heisen-9-WS-6`, hiện hồn một bóng ma Local User vừa được bơm vào hệ thống:

![User Creation Logging](/assets/images/htb/the-enduring-echo/568929c1-0863-4212-b98b-c55378186800.png)

```
svc_netupd
```

### 8. Bóc trần Domain được dùng để C2/Exfiltration

> What domain name did the attacker use for credential exfiltration?

Xâm nhập vào `Triage`, luồn tới thư mục nắm giữ cái script chết tiệt ở Câu 6 `C:\Users\Werni\Appdata\Local\JM.ps1`. Ban trần cái mã nguồn để dò hỏa mù:

![PowerShell Payload](/assets/images/htb/the-enduring-echo/e5b799ea-3efe-4fa0-b875-65e7e48da77f.png)

Payload C2 server:

```
NapoleonsBlackPearl.htb
```

### 9. Quá trình Sinh Password Dựa Theo Dòng Thời Gian (Timestamp-base Password DGA)

> What password did the attacker's script generate for the newly created user?

Đào vào ruột cái script powershell `JM.ps1`, đây là chu trình cấy cờ của nó:
- Khởi tạo array pool `$usernames` gồm những cái tên lôm côm: `svc_netupd`, `svc_dns`...
- Check if existing? Nhờ búa `Get-LocalUser`.
- Nếu sạch, nó sẽ pick ngẫu nhiên một cái tên, rồi đâm rễ đính password sinh ra tột độ phụ thuộc vào thời điểm `$timestamp = (Get-Date).ToString("yyyyMMddHHmmss")`.
- Cấu trúc format hardcode đứt: `Watson_$timestamp`.
- Bơm user, quẳng vào 2 Local Group mâm trên: `Administrators` và `Remote Desktop Users`.
- Kích động mở RDP qua Registry.
- Bắt tay tuồn dữ liệu Base64 tới con domain ở trên `NapoleonsBlackPearl.htb`.

Dựa vào chu trình sinh password: Thời điểm password được nhồi (nhìn theo mã sinh) chính là mốc Event Id `4720` nổ ra cho `svc_netupd` (`2025-08-24 23:05:09` UTC). Nếu bứng nguyên đoạn này `Watson_20250824230509` đâm vào đáp án, có thể sập bẫy.
Lý do: Lệnh `(Get-Date)` móc theo Local Time Zone của máy tính nạn nhân, còn Windows Security Event ném log lên ở khung giờ chuẩn vị UTC +0. Xảy ra chênh lệch giờ!

Tìm cho bằng được TimeZone: Lủi vào thư mục `C:\Windows\System32\config` của hạ tầng Triage thu thâp.

![System Config](/assets/images/htb/the-enduring-echo/89bad063-e00b-4f7f-9fb5-96c9324c1ae0.png)

Bốc Registry Hive SYSTEM ra thẩm với Powershell:
```powershell
reg load HKLM\TempSYSTEM <SYSTEM Path>
Get-ItemProperty -Path "HKLM:\TempSYSTEM\ControlSet001\Control\TimeZoneInformation" | Select-Object TimeZoneKeyName, StandardName, Bias, ActiveTimeBias, DaylightName, DynamicDaylightTimeDisabled
reg unload HKLM\TempSYSTEM
```

![Registry TimeZone](/assets/images/htb/the-enduring-echo/7caa3a28-ee6a-4eb3-a189-548bceea6cfe.png)

Dính rồi, thiết bị ôm khung giờ `Pacific Standard Time` (UTC - 7). Cứ thế đắp đi 7 tiếng khỏi đồng hồ UTC:
`23:05 - 7 tiếng = 16:05`.

```
Watson_20250824160509
```

### 10. Chặn vết Pivot Lùng Sục Điểm Vỡ (Internal Pivot Target)

> What was the IP address of the internal system the attacker pivoted to?

Quay vòng lại Timeline Explorer, filter lùng cặn với keyword: `ssh`, `rdp` hay `scp` rọi đuốc tìm mồi mạng nội bộ:
```
Contains([Executable Info], 'ssh') Or Contains([Executable Info], 'rdp') Or Contains([Executable Info], 'scp')
```

![SSH RDP Movement](/assets/images/htb/the-enduring-echo/7a1e6546-cea8-4449-90f6-02ed15b48797.png)

Va chạm vào con target nội bộ:

```
192.168.1.101
```

### 11. Giải mã Cú Đâm Xuyên PortProxy Pivot

> Which TCP port on the victim was forwarded to enable the pivot?

Nắm đầu được cái IP mục tiêu bên trên, ta ném thẳng IP này lại thanh search. Trồi lên nguyên một mâm câu lệnh port forwarding bá đạo bằng `netsh`:

![Netsh Pivot Command](/assets/images/htb/the-enduring-echo/32e2d516-99eb-4e4d-af79-2ebc5031a022.png)

Lệnh gốc: `C:\Windows\System32\netsh.exe netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9999 connectaddress=192.168.1.101 connectport=22`
Kẻ điều phối mở ngay cổng listening `9999` để bơm vào lò ssh bên trong.

```
9999
```

### 12. Full Registry Path đâm ngầm của Netsh

> What is the full registry path that stores persistent IPv4→IPv4 TCP listener-to-target mappings?

Bình thường ta có thể search chữ ký IP qua Timeline Explorer trên mảng log registry. 

![Registry Logs](/assets/images/htb/the-enduring-echo/bed1217a-dc4f-45c7-8154-0654319bc26a.png)

Sành sỏi hơn, vác cái tool `Registry Explorer` load cấu hình SYSTEM.
Xộc vào thư mục: `ROOT\ControlSet001\Services\PortProxy\v4tov4\tcp`, toàn bộ cái cờ proxy được móc ở dạng persist trong này (nhờ netsh xử lý platform).

![PortProxy Registry Tree](/assets/images/htb/the-enduring-echo/3c3a7027-a5af-4668-a08b-467aa56def21.png)

![PortProxy Details](/assets/images/htb/the-enduring-echo/c73af53d-b151-468c-9a66-2c9c0788dee1.png)

Quy đổi ra chuẩn full path:
```
HKLM\SYSTEM\CurrentControlSet\Services\PortProxy\v4tov4\tcp
```

### 13. Mapping Kỹ Thuật Lên Bảng phong thần MITRE ATT&CK 

> What is the MITRE ATT&CK ID associated with the previous technique used by the attacker to pivot to the internal system?

Tham khảo mapping của mớ Netsh v4tov4 Port Proxy trong hệ thống MITRE.

![MITRE Framework](/assets/images/htb/the-enduring-echo/0b0a68e7-e7a2-4468-86d0-c5899e252b1c.png)

```
T1090.001
```

### 14. Bóc trần Cấu rỉa Command Line Auditing

> Before the attack, the administrator configured Windows to capture command line details in the event logs. What command did they run to achieve this?

Thật may mắn vì các anh em Sysadmin đã mở sẵn Policy dòm Command Line Auditing (chi tiết có thể tham chiếu tệp MS Doc: Command line process auditing). Thường thì để Enable trò này, cần bơm cờ Policy LocalAccountTokenFilterPolicy vào mạn sườn `HKLM\Microsoft\Windows\CurrentVersion\Policies\System\Audit`.

![Command Line Logging Config](/assets/images/htb/the-enduring-echo/ce8a3776-d3a7-44b9-88fb-c75a62719f18.png)
![AI Verification](/assets/images/htb/the-enduring-echo/f4398fab-22cf-4240-a320-f94a70385582.png)

Nếu vạch kẽ tóc thư mục Triage, cắm vào artifact của Powershell Readline Histrory (`C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt`), ta sẽ lôi được ngay câu lệnh admin tự tay bấm chót:

![ConsoleHost History](/assets/images/htb/the-enduring-echo/d9a353f0-5a5a-4317-a07a-76392f637856.png)

```cmd
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
```
