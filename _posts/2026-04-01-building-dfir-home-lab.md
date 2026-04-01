---
layout: post
title: "Building DFIR home lab"
date: 2026-04-01
categories: [dfir-knowledge]
tags: []
---

- Getting started with DFIR
    
    ## Getting started with DFIR
    
    DFIR (Digital Forensics & Incident Response) là một mảng đặc thù trong cyber security, nếu chỉ đọc lý thuyết và cài tools, chúng ta sẽ rất nhanh rơi vào trạng thái “biết tên tool nhưng không biết dùng vào đâu”. Lý do đơn giản: DFIR muốn học được thì phải **có thứ để điều tra**—log, disk image, máy bị compromise, artefact hệ thống…
    
    Vì vậy hợp lý nhất khi bắt đầu là sắp xếp việc học theo một chuỗi công việc liên tục: **dựng môi trường phân tích → tạo hiện trường → tạo kịch bản → điều tra → mở rộng lab**.
    
    ### Vì sao người mới hay bị ngợp khi học DFIR?
    
    Có hai “cục đá” thường gặp:
    
    - **Thiếu hiện trường**: DFIR không giống red teaming ở chỗ bạn không dễ “tạo lab” ngay nếu chưa có lab hoặc dữ liệu. Bạn cần một nguồn dữ liệu để thực hành điều tra.
    - **tools quá nhiều và không đồng đều**: open-source trên GitHub rất nhiều, nhưng nhiều tools dùng trong doanh nghiệp lại là thương mại, làm người mới khó chọn điểm bắt đầu.
    
    Vì vậy, cách vào DFIR nên đi từ “khung làm việc” (workflow) trước rồi mới tối ưu tool sau.
    
    ### Lộ trình học và build hệ thống DFIR tại nhà
    
    Một roadmap thực dụng có thể đi theo thứ tự sau:
    
    1. **Dựng forensic workstation**
        
        Mục tiêu là có một máy và môi trường phân tích tiêu chuẩn, ổn định, cài những tools phổ biến cho forensic—và ưu tiên tools miễn phí để bắt đầu nhanh.
        
    2. **Chuẩn bị hệ thống mục tiêu để điều tra (target systems)**
        
        Bạn cần “đối tượng” để tạo dữ liệu điều tra, thường bắt đầu bằng một vài VM (Windows là lựa chọn dễ tạo artefact).
        
    3. **Tạo kịch bản tấn công (attack scenarios)**
        
        Không cần phức tạp ngay từ đầu. Điều quan trọng là kịch bản tạo ra dấu vết rõ ràng để bạn luyện: điểm xâm nhập, thực thi, persistence, network, thao tác file. Bên cạnh đó, nên tham khảo các tài nguyên/mô hình tấn công và malware framework thường gặp ngoài thực tế để tạo kịch bản như Mitre Attack.
        
    4. **Thực hiện điều tra và phân tích (investigations & analysis)**
        
        Đây là phần bạn luyện kỹ năng chính: thu thập, trích xuất artefact, dựng timeline, trả lời câu hỏi điều tra, và viết báo cáo.
        
    5. **Xây lab theo cấp độ (Build Your Lab)**
        
        Mục tiêu dài hạn là có lab riêng để thử tool/kỹ thuật mới: từ mức đơn giản (virtualization + Windows VM) đến mức nâng cao (domain controller, thêm các security tool). Xa hơn là ứng dụng SIEM như Elastic, Splunk và Velociraptor.
        
- Dựng forensic workstation (Sử dụng **VMware Workstation**)
    
    Mục tiêu của một máy forensic workstation trong lab DFIR là có **một môi trường phân tích ổn định, sạch, có thể rollback**, và đủ công cụ để đi từ **acquire/mount → parse artefact → dựng timeline → tổng hợp IOC**. Cách triển là: **Windows VM**, kèm **Ubuntu chạy trong WSL** để tận dụng song song hệ tool Windows và Linux.
    
    ---
    
    ### 1) Kiến trúc workstatio
    
    - **Hypervisor**: VMware Workstation (Pro/Player đều được; Pro tiện hơn vì snapshot tốt).
    - **Guest chính**: Windows (khuyến nghị Server 2019 Evaluation hoặc Windows 10 Enterprise Evaluation).
    - **Linux toolchain**: Ubuntu trong WSL (chạy ngay trong Windows guest).
    
    Điểm mạnh của layout này là bạn không phải tạo share folder giữa hai VM riêng biệt để chia sẻ file/artefact; đa số workflow forensic Windows chạy trực tiếp trên Windows, còn phần timeline/memory/macro tooling có thể đẩy qua WSL khi cần.
    
    ---
    
    ### 2) Tạo Windows VM trên VMware (cấu hình khuyến nghị)
    
    Tạo VM mới trong VMware Workstation và đặt các thông số theo mức cơ bản sau (đây là mức đủ dùng cho lab và bài tập phân tích phổ biến):
    
    - Disk: **100 GB**, chọn kiểu **thin / grow as needed** (tương đương “dynamically allocated”).
    - RAM: **tối thiểu 4 GB** (càng nhiều càng dễ thở).
    - vCPU: **2+**
    - Network: **NAT**
    
    Sau khi cài Windows xong:
    
    - Cài **VMware Tools** (để clipboard, drag/drop, shared folder… hoạt động ổn định).
    - Tắt máy và tạo **snapshot mốc “Fresh Install”**.
    
    > Lưu ý: Windows bản Evaluation có thời hạn (workstation thường 90 ngày, server thường 180 ngày).
    > 
    
    ---
    
    ### 3) WSL: chọn WSL1 hay WSL2 khi chạy **bên trong Windows VM**
    
    Có hai hướng:
    
    **A. WSL1 (ổn định, ít phụ thuộc cấu hình ảo hóa lồng)**
    
    Phù hợp nếu bạn muốn môi trường “ít biến số”, chủ yếu dùng WSL cho các tool CLI. Trang hướng dẫn gốc cũng tập trung WSL1.
    
    **B. WSL2 (Linux kernel đầy đủ, nhưng cần nested virtualization trong VMware)**
    
    Nếu bạn cần tính năng kernel đầy đủ (một số workflow/container/một vài tooling), WSL2 tiện hơn. Khi chạy WSL2 *trong VM*, bạn thường phải bật **nested virtualization** trong cấu hình VM.
    
    Trong VMware Workstation, tham khảo cách bật nested virtualization tại link sau: [https://community.broadcom.com/vmware-cloud-foundation/discussion/vmware-workstation-does-not-support-nested-virtualization-on-this-host-module-hv-power-on-failed](https://community.broadcom.com/vmware-cloud-foundation/discussion/vmware-workstation-does-not-support-nested-virtualization-on-this-host-module-hv-power-on-failed)
    
    Nếu mục tiêu của bạn chỉ là dựng workstation forensic cho lab DFIR, **WSL1 thường đã đủ.**
    
    Các bước cài WSL1:
    
    - Chạy lệnh powershell sau dưới quyền Admin
        
        ```
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
        ```
        
    - Download phiên bản Linux tuỳ ý tại [Manual installation steps for older versions of WSL | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/install-manual#downloading-distributions)
    - Sau khi download, đổi tên file từ .appxbundle thành .zip và giải nén.
    - Truy cập vào folder đã giải nén và chạy command để cài đặt:
        
        ```bash
        Add-AppxPackage .\Ubuntu_<version>.appx
        ```
        
    - Reboot lại máy và mở Ubuntu tại thanh Start của Windows để setup username, password cho WSL
    - Verify lại bằng cách chạy lệnh **`wsl –version`**
    
    ---
    
    ### 4) Chuẩn hóa Windows guest
    
    1. **Set Time Zone**
        
        Giúp đồng bộ thời gian giữa các tool, dễ đối chiếu sự kiện nhiều múi giờ.
        
    2. File Explorer Bật:
        - **Hidden items**
        - **File name extensions**
    3. Tạo thư mục làm việc ngắn đường dẫn:
        - `C:\Cases` (evidence / working / exports)
        - `C:\Tools` (toolset)
    4. Microsoft Defender (tránh phá evidence/tool)
        - Tắt “Cloud-delivered protection” và “Automatic sample submission” (1 lần).
        - Khi cần có thể tạm tắt real-time protection.
        - Quan trọng: **Exclude** `C:\Cases` và `C:\Tools` để Defender không tự động cách ly/xóa file.
    
    ---
    
    ### 5) Toolset: (Windows + WSL)
    
    Mục tiêu là đủ cho các bài phân tích phổ biến: mount image, triage, registry/event log, timeline, memory, network, triage malware.
    
    ### 5.1. Linux tools trong Ubuntu (WSL)
    
    Trong Ubuntu (WSL), cài các tools sau:
    
    - `pip3`
    - **Volatility3** (+ capstone)
    - **Plaso / log2timeline** (timeline “kitchen sink”)
    - **oletools** (artefact Office/macro)
    
    ### 5.2. Windows tools (cài trong Windows VM)
    
    | Application | OS | Purpose | Notes (diễn giải tiếng Việt, giữ thuật ngữ) |
    | --- | --- | --- | --- |
    | Windows Server 2019 Evaluation | Any | Essentials | Bản Evaluation; nhiều người dùng cho forensics vì môi trường Windows Server “gọn”, ổn định cho toolset. |
    | Kali Linux Subsystem for Windows Server | Windows | Essentials | Kali Linux Subsystem cài trên Windows Server (WSL) để có bộ công cụ Linux ngay trong Windows. |
    | Notepad++ | Windows | Essentials | Text editor hỗ trợ syntax formatting cho nhiều loại text/code, đọc log nhanh. |
    | Firefox | Windows | Essentials | Ngoài browsing, Developer tools dùng debug website và HTTP requests (tương tự Chrome). |
    | Microsoft Excel | Windows | Essentials | Rất hợp để xử lý large CSV data sets, lọc/sort/pivot và dựng timelines. |
    | Visual Studio Code | Windows | Essentials | Text editor nâng cao; nhiều plugins cho text files; hữu ích khi đọc/viết code và cấu hình. |
    | 7-Zip | Windows | Essentials | compress/decompress nhiều định dạng (zip/7z/tar/gz…). |
    | FTK Imager | Windows | Image Mounting & Data Acquisition | Tool phổ biến để tạo memory and disk images và load/mount images.  |
    | KAPE - Kroll Artifact Parser and Extractor | Windows | Data Acquisition | Thu thập triage data từ disk images; có thể parse trực tiếp artifacts theo targets/modules. |
    | Arsenal Image Mounter | Windows | Image Mounting | Nổi tiếng vì mount disk images ổn định. |
    | DumpIt | Windows | Memory Acquisition | Tool đơn giản để tạo memory dumps trên Windows; lưu ý giới hạn ghi “chỉ handle 4GB RAM”. |
    | Eric Zimmerman Tools | Windows | Windows Analysis | Bộ tool forensic Windows rất phổ biến; gồm TimelineExplorer để xem kết quả timeline.  |
    | RegRipper 3.0 | Windows | Windows Analysis | Tool parse Registry hives; có cả GUI và command line; hữu ích cho triage registry nhanh. |
    | Event Log Explorer | Windows | Windows Analysis | UI mạnh hơn Windows Event Viewer để phân tích Windows event logs; cần registration nhưng free cho non-commercial use. |
    | Windows Sysinternals | Windows | Windows Analysis | Bộ Sysinternals (autoruns, process explorer, …) hỗ trợ điều tra artifacts runtime/autoruns/processes, hay bị “overlooked” nhưng rất hữu ích. |
    | Wireshark | Windows | Network Analysis | capture và phân tích network traffic (pcap), filter, reassemble, v.v. |
    | CyberChef | Windows | Malware Analysis | Dùng để encode/decode/transform payload; dùng nhiều trong malware/CTI. |
    | PEStudio | Windows | Malware Analysis | static analysis Windows executables; nhiều checks/indicators. |
    | ExifTool | Windows | Malware Analysis | Tool đơn giản để lấy meta-data của rất nhiều định dạng file; hữu ích khi triage file/doc/media. |
    | Plaso Log2Timeline | Linux | Windows & Linux Analysis | Nổi tiếng để tạo timelines bằng cách parse “kitchen sink approach” từ nhiều artifacts/OS; có nhiều parsers; đôi khi là alternative cho EZ tools với output format khác nhau. |
    | Volatility3 | Linux | Memory Analysis | “De facto standard” cho memory analysis; nên dùng Volatility version 3 để tương thích OS mới. |
    | oletools | Linux | Malware Analysis | Bộ Python tools phân tích Microsoft OLE2 files (Office docs…) phục vụ malware analysis (macro, streams, indicators…). |
    | Event Log Explorer | Windows | Windows Analysis | (Bị lặp) Vẫn là tool rất mạnh cho Windows Event Log analysis |
    
    Cài xong toàn bộ, tạo **snapshot mốc mới “Workstation Ready**”.
    
    ---
    
    ### 6) Cách dùng workstation: workflow tối thiểu cho một case
    
    Khi workstation đã sẵn, nhịp làm việc cơ bản (đủ cho hầu hết bài lab và nhiều tình huống thực tế) là:
    
    1. **Tạo memory image + disk image** từ máy cần điều tra
    2. **Import** về `C:\Cases`
    3. Bắt đầu phân tích theo thứ tự: **memory trước → disk sau**
    4. Dựng **timeline** để hiểu “chuyện gì xảy ra khi nào”
    5. Tổng hợp **IOC** để lần theo hành vi và phạm vi ảnh hưởng
    
    Nếu bạn chưa có dữ liệu mẫu để phân tích, cách bền vững nhất là tự tạo: dựng một “victim VM”, mô phỏng hành vi độc hại hoặc chạy lab scenario để sinh artefact rồi quay lại điều tra.
    
    ---