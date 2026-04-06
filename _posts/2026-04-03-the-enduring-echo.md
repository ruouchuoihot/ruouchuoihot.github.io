---
title: "The Enduring Echo"
date: 2026-04-03
ctf: "Hack The Box"
category: incident-response
tags: [hack-the-box, htb, dfir, event-logs, windows-forensic, lateral-movement]
---

> LeStrade passes a disk image artifacts to Watson. It's one of the identified breach points, now showing abnormal CPU activity and anomalies in process logs.


:::info
KAPE First

:::


 1. What was the first (non cd) command executed by the attacker on the host? (string)
    * Sử dụng tool Timeline Explorer và invest log tại Results\\EventLogs\\20250923033121_EvtxECmd_Output.csv


    * Lệnh để filter các thông tin:
      * Nếu dùng Timeline Explorer

        ```none
        [Channel] = 'Security' And Not Contains([Executable Info], 'backgroundTaskHost.exe') And Not Contains([Executable Info], 'RuntimeBroker.exe') And Not Contains([Executable Info], 'sppsvc.exe') And Not Contains([Executable Info], 'fontdrvhost.exe') And Not Contains([Executable Info], 'LocalService') And Not Contains([Executable Info], 'taskhostw.exe') And Not Contains([Executable Info], 'userinit.exe') And Not Contains([Executable Info], 'ctfmon.exe') And Not Contains([Executable Info], 'cd') And Contains([Executable Info], 'cmd') And [Event Id] = 4688
        ```

        \
      * Nếu dùng splunk:

        ```none
        | inputlookup htb_chal2_eventlog.csv | search (EventId=4688) | table TimeCreated, Computer, PayloadData2, PayloadData3, PayloadData5, ExecutableInfo | rename PayloadData2 as PID,PayloadData3 as PPID, PayloadData5 as User, ExecutableInfo as Process | search User="Target User: HEISEN-9-WS-6\\Werni"
        | search NOT (Process IN ("*backgroundTaskHost.exe*", "*RuntimeBroker.exe*", "*sppsvc.exe*","*fontdrvhost.exe*","*LocalService*", "*taskhostw.exe*", "*userinit.exe*","*ctfmon.exe*"))
        | search Process="*cmd.exe*"
        ```
      * Trong lệnh này ta loại bỏ các process khả năng cao không diễn ra do attacker như (backgroundTaskHost.exe, RuntimeBroker.exe, …), sau đó filter process của cmd với Envent Id 4688 (__[A new process has been created.](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688)__).

        ![](/assets/images/htb/the-enduring-echo/92553d72-2546-4a98-bdfb-e5d2666501b8.png " =614x448")
    * Khi này tại mốc thời gian 2025-08-24 22:51:09, ta thu được 1 event có signature khá giống với các cuộc tấn công lateral movement, các event ở trước đó chỉ là OneDrive và Vmware nên khả năng cao không phải hành vi của attacker

      ![](/assets/images/htb/the-enduring-echo/7c0a831c-4fc8-4e74-9500-f36ae201dce0.png " =2547x1000")
      * Thông tin về Event như sau:
        * 2025-08-24 22:51:09
        * Event Id: 4688
        * Computer: Heisen-9-WS-6
        * User name: WORKGROUP\\HEISEN-9-WS-6$
        * Parent process: C:\\Windows\\System32\\wbem\\WmiPrvSE.exe
        * Process: C:\\Windows\\System32\\cmd.exe cmd.exe /Q /c systeminfo 1&gt; \\\\127.0.0.1\\ADMIN$\\__1756075857.955773 2&gt;&amp;1

        ```powershell
        systeminfo
        ```

        \
 2. Which parent process (full path) spawned the attacker's commands? (C:\\FOLDER\\PATH\\FILE.ext)
    * Dựa vào Parent process ở câu trên, ta có full path của parent process là `C:\Windows\System32\wbem\WmiPrvSE.exe`
    * Nếu dùng lệnh splunk:

      ```none
      | inputlookup htb_chal2_eventlog.csv | search (EventId=4688)  PayloadData2="PID: 0xF34"
      ```

      ```powershell
      C:\Windows\System32\wbem\WmiPrvSE.exe
      ```
 3. Which remote-execution tool was most likely used for the attack? (filename.ext)
    * Vì challange chỉ có các file forensic của máy victim nên chúng ta sẽ không nắm chắc được tool mà attacker dùng, tuy nhiên dựa vào những signature như WmiPrvSE.exe thực hiện lateral movement có thể suy ra đc tool sử dụng là `wmiexec.py` của Impacket

      ```powershell
      wmiexec.py
      ```
 4. What was the attacker's IP address? (IPv4 address)
    * Dựa vào mốc thời gian 2025-08-24 22:51:09, ta filter các event Id 4624 (__[An account was successfully logged on.](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624)__)
    * Có 1 event login diễn ra trước mốc thời gian này vào lúc 2025-08-24 22:50:58 với remote ip là `10.129.242.110`

      ```powershell
      10.129.242.110
      ```
 5. What is the first element in the attacker's sequence of persistence mechanisms? (string)
    * Sau khi đã xác định được process spawned attacker command là `WmiPrvSE.exe`, ta filter cột parent process theo `WmiPrvSE.exe` 

      ![](/assets/images/htb/the-enduring-echo/170376f9-ab8a-430f-b879-b154ef027075.png " =1793x868")
    * Trong đó, event diễn ra tại `2025-08-24 23:03:50` có câu lệnh gần giống với câu hỏi "first element of persistence mechanisms" nhất:
      * Process: `C:\Windows\System32\cmd.exe cmd.exe /Q /c schtasks /create /tn "SysHelper Update" /tr "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\Users\Werni\Appdata\Local\JM.ps1" /sc minute /mo 2 /ru SYSTEM /f 1&gt; \\127.0.0.1\ADMIN$\__1756076432.886685 2&gt;&amp;1`
    * Lệnh này thực hiện việc tạo một scheduled task có tên là "SysHelper Update" và chạy một script PowerShell JM.ps1 mỗi 2 phút với quyền SYSTEM. Các output của lệnh sẽ được ghi vào folder share (\\127.0.0.1\\ADMIN$....)

      ```none
      SysHelper Update
      ```
 6. Identify the script executed by the persistence mechanism. (C:\\FOLDER\\PATH\\FILE.ext)
    * Dựa trên đáo án câu 5, path của script thực hiện hành vi persistence là `C:\Users\Werni\Appdata\Local\JM.ps1`
    * Nếu dùng splunk:

      ```none
      | inputlookup htb_chal2_eventlog.csv | search (EventId=4688)  PayloadData2="PID: 0xF34"
      ```

    ```none
    C:\Users\Werni\Appdata\Local\JM.ps1
    ```
 7. What local account did the attacker create? (string)
    * Filter Event Id 4720 ([4720(S) A user account was created. - Windows 10](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4720)) Với computer name của máy victim là Heisen-9-WS-6, ta sẽ thấy được target user được tạo ra là `svc_netupd`

      ![](/assets/images/htb/the-enduring-echo/568929c1-0863-4212-b98b-c55378186800.png " =1370x296")
    * Nếu dùng splunk:

      ```none
      | inputlookup htb_chal2_eventlog.csv | search (EventId=4720)
      ```

    ```none
    svc_netupd
    ```
 8. What domain name did the attacker use for credential exfiltration? (domain)
    * Dựa vào câu 6 của challange, ta có thể tìm thấy script attack tại path `C:\Users\Werni\Appdata\Local\JM.ps1` của folder triage

      ![](/assets/images/htb/the-enduring-echo/e5b799ea-3efe-4fa0-b875-65e7e48da77f.png " =2321x1069")

    ```none
    NapoleonsBlackPearl.htb
    ```
 9. What password did the attacker's script generate for the newly created user? (string)
    * Dựa vào script JS1.py, ta sẽ xác định được format tạo password sau khi add user của script như sau:
      * **Khởi tạo list** $usernames), bao gồm các tên như svc_netupd, svc_dns, v.v.
      * Kiểm tra nếu các user này đã tồn tại trong hệ thống bằng cách sử dụng lệnh Get-LocalUser để kiểm tra các tài khoản có tên tương ứng trong danh sách.
      * Nếu không có user nào trong tồn tại, script sẽ:
        * Chọn một tên ngẫu nhiên từ danh sách $usernames.
        * Tạo một mật khẩu dựa trên thời gian hiện tại (timestamp) bằng lệnh  $timestamp = (Get-Date).ToString("yyyyMMddHHmmss")

          và có format là `Watson_$timestamp`.
        * Tạo user mới với mật khẩu đã mã hóa dưới dạng SecureString.
        * Thêm user vào group Administrators và Remote Desktop Users
        * Enable Remote Desktop (RDP) thông qua registry
        * Gử HTTP request tới NapoleonsBlackPearl.htb với thông tin tài khoản và mật khẩu dưới dạng Base64.
    * Từ đây ta xác định được rằng password sẽ là Waston + timestamp tại thời điểm script chạy => Waston + timestamp tại thời điểm diễn ra Event Id 4720 (tạo user svc_netupd) vì khi script chạy user `svc_netupd` đã được tạo ra
    * Filter Event Id 4720 với user `svc_netupd` sẽ ra được mốc thời gian là `2025-08-24 23:05:09` => đáng lẽ sẽ có password là `Watson_20250824230509`
    * Tuy nhiên challange này có 1 trick để lừa chúng ta, đó là lệnh (Get-Date).ToString("yyyyMMddHHmmss") sẽ lấy time dựa theo múi giờ trên máy local, còn khi event được ghi vào log dưới Event Id sẽ luôn lấy múi giờ UTC +0 nên kết quả trên sẽ sai => Ta cần tìm ra múi giờ của máy để giải được câu này.
    * Các Registry key thường sẽ nằm ở `C:\Windows\System32\config` khi access folder của triage folder ta sẽ thấy:

      ![](/assets/images/htb/the-enduring-echo/89bad063-e00b-4f7f-9fb5-96c9324c1ae0.png " =1380x816")
    * Khi này có thể dùng lệnh powershell để load và đọc nội dung time zone

      ```none
      reg load HKLM\TempSYSTEM <SYSTEM Path>
      >> Get-ItemProperty -Path "HKLM:\TempSYSTEM\ControlSet001\Control\TimeZoneInformation" |
      >> Select-Object TimeZoneKeyName, StandardName, Bias, ActiveTimeBias, DaylightName, DynamicDaylightTimeDisabled
      >> reg unload HKLM\TempSYSTEM
      ```

      ![](/assets/images/htb/the-enduring-echo/7caa3a28-ee6a-4eb3-a189-548bceea6cfe.png " =1810x509")
    * Pacific Standard Time tương đương với UTC - 7 => Password là `Watson_20250824160509`

    ```none
    Watson_20250824160509
    ```
10. What was the IP address of the internal system the attacker pivoted to? (IPv4 address)
    * Khi filter log với nội dung chứa các keyword như `ssh`, `rdp` ta sẽ thấy hành vi truy cập tới IP này của attacker
    * Filter khi dung Timeline Explorer

      ```none
      Contains([Executable Info], 'ssh') Or Contains([Executable Info], 'rdp') Or Contains([Executable Info], 'scp')
      ```

      ![](/assets/images/htb/the-enduring-echo/7a1e6546-cea8-4449-90f6-02ed15b48797.png " =1507x862")

    ```none
    192.168.1.101
    ```
11. Which TCP port on the victim was forwarded to enable the pivot? (port 0-65565)
    * Sau khi có đc câu 10, ta filter IP này trong trường Process sẽ được 1 Event như sau:

      ![](/assets/images/htb/the-enduring-echo/32e2d516-99eb-4e4d-af79-2ebc5031a022.png " =1563x224")

      `C:\Windows\System32\netsh.exe netsh  interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9999 connectaddress=192.168.1.101 connectport=22`
    * Vậy port internal được mở để listen là 9999

    ```none
    9999
    ```
12. What is the full registry path that stores persistent IPv4→IPv4 TCP listener-to-target mappings? (HKLM......)
    * Ta có thể dùng Timeline Explorer để đọc log về Registry và filter địa chỉ IP từ câu 10

      ![](/assets/images/htb/the-enduring-echo/bed1217a-dc4f-45c7-8154-0654319bc26a.png " =2520x305")
    * Hoặc để trực quan hơn, ta sử dụng 1 tool về registry forensic là Registry Explorer để đọc các config về SYSTEM

      ![](/assets/images/htb/the-enduring-echo/3c3a7027-a5af-4668-a08b-467aa56def21.png " =2549x1450")
    * Khi này sẽ xác định được registry key là `ROOT\ControlSet001\Services\PortProxy\v4tov4\tcp`, lưu ý registry key và registry path là 2 định nghĩa khác nhau (có thể tham khảo thêm AI) => ta cần xác định được registry path nào load key này

      ![](/assets/images/htb/the-enduring-echo/c73af53d-b151-468c-9a66-2c9c0788dee1.png " =2549x1396")
    * Khi này sẽ xác định được Registry path là `HKLM\SYSTEM\CurrentControlSet\Services\PortProxy\v4tov4\tcp`
    * Nếu dùng splunk

      ```none
      | inputlookup htb_chal2_registry.csv
      | search KeyPath="*tcp*"
      ```

    ```none
    HKLM\SYSTEM\CurrentControlSet\Services\PortProxy\v4tov4\tcp
    ```
13. What is the MITRE ATT&CK ID associated with the previous technique used by the attacker to pivot to the internal system? (Txxxx.xxx)
    * Có thể hỏi AI hoặc google về thông tin của technique này

      ![](/assets/images/htb/the-enduring-echo/0b0a68e7-e7a2-4468-86d0-c5899e252b1c.png " =494x279.3333333333333")

    ```none
    T1090.001
    ```

    \
14. Before the attack, the administrator configured Windows to capture command line details in the event logs. What command did they run to achieve this? (command)
    * Thông tin về cách audit log này có thể kiếm trên google __[Command line process auditing](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing)__
    * Để bật policy này ta phải vào Computer Configuration > Windows Settings > Security Settings > Advanced Audit Policy Configuration > System Audit Policies > Detailed Tracking and open the Audit Process Creation và Registry Path thường sẽ nằm ở `HKLM\Microsoft\Windows\CurrentVersion\Policies\System\Audit`

      ![](/assets/images/htb/the-enduring-echo/ce8a3776-d3a7-44b9-88fb-c75a62719f18.png " =2555x1488")
    * Có thể nhờ AI để render giúp lệnh vì ta sẽ k biết chính xác câu lệnh này (vì sau khi câu lệnh này đc chạy, các Event Id 4688 mới thực hiện lưu lại các command)

      ![](/assets/images/htb/the-enduring-echo/f4398fab-22cf-4240-a320-f94a70385582.png " =1452x1043")
    * Ngoài ra nếu mò đủ sâu folder mà challange cung cấp, ta sẽ thấp 1 file tại `C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline` cũng ghi lại câu lệnh này

      ![](/assets/images/htb/the-enduring-echo/d9a353f0-5a5a-4317-a07a-76392f637856.png " =2269x1336")

    ```none
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
    ```

    \