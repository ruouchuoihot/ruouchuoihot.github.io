---
title: "Báo Cáo Sự Cố Thực Tế (Real-world Incident Report)"
date: 2026-04-01
category: dfir-knowledge
tags: [dfir, incident-response, malware, soc, blue-team]
excerpt: "Mẫu báo cáo Incident Report phân tích một vụ xâm nhập nội bộ sử dụng PowerShell payload, Metasploit, khai thác buffer overflow và truy cập dữ liệu trái phép."
---

# Báo cáo Sự cố Thực tế (Real-world Incident Report)

## Executive Summary

- `Incident ID`: INC2019-0422-022
- `Mức độ nghiêm trọng`: High (P2)
- `Trạng thái`: Đã khắc phục (Resolved)

**Tổng quan:** Vào ngày `22/04/2019` lúc `01:05:00`, đội SOC của SampleCorp phát hiện dấu hiệu truy cập trái phép vào mạng nội bộ. Cảnh báo được kích hoạt bởi các process bất thường và tập lệnh PowerShell đáng ngờ.

Kẻ tấn công lợi dụng lỗ hổng trong network access controls để xâm nhập và chiếm quyền kiểm soát một số hệ thống quan trọng.

**Key Findings:**
- Lỗ hổng trong network access controls cho phép kẻ tấn công có được internal IP và truy cập network nội bộ của SampleCorp.
- Máy `WKST01.samplecorp.com` bị tấn công thông qua lỗ hổng trong Adobe Acrobat Reader.
- Kẻ tấn công khai thác thêm lỗ hổng buffer overflow trong ứng dụng nội bộ để mở rộng phạm vi xâm nhập.
- Không có dữ liệu quy mô lớn bị đánh cắp nhờ đội SOC/DFIR phản ứng kịp thời, tuy nhiên `WKST01.samplecorp.com` và `HR01.samplecorp.com` đều bị xâm phạm.

**Immediate Actions:**
- Đội SOC/DFIR xử lý nội bộ, không thuê ngoài.
- Cô lập các máy bị ảnh hưởng bằng VLAN segmentation.
- Thu thập network traffic captures phục vụ điều tra.
- Tăng cường host security và tổng hợp log về Elastic SIEM.

---

## Phân tích Kỹ thuật (Technical Analysis)

### Hệ thống và Dữ liệu bị ảnh hưởng (Affected Systems & Data)

Lỗ hổng trong cấu hình Network Access Controls cho phép một thiết bị bên ngoài nhận được internal IP và kết nối vào network nội bộ của SampleCorp.

Kẻ tấn công đã có quyền truy cập vào:

- `WKST01.samplecorp.com`: Máy phát triển chứa source code nội bộ và API keys kết nối đến các dịch vụ bên thứ ba. Nguy cơ lộ source code và các API keys này.
- `HR01.samplecorp.com`: Máy chủ HR chứa thông tin nhân sự nhạy cảm bao gồm Payroll và thông tin định danh cá nhân (PII). Đặc biệt, database không được mã hóa chứa Social Security numbers và thông tin tài khoản ngân hàng của nhân viên. Rủi ro lộ thông tin và identity theft là đáng lo ngại.

### Bằng chứng và Phân tích (Evidence Sources & Analysis)

**Phân tích WKST01.samplecorp.com**

Lúc `22/04/2019 01:05:00`, đội SOC phát hiện activity bất thường. Log ghi nhận mối quan hệ parent-child process bất thường, với PowerShell được gọi bởi `cmd.exe` để thực thi remote script trỏ về IP `192.168.220.66` — một địa chỉ internal, xác nhận kẻ tấn công đã ở trong mạng nội bộ.

![image](/assets/images/dfir/31fbc35f-72fd-814f-ad37-d6536e2e521a.png)

Phân tích cho thấy kịch bản xâm nhập ban đầu vào `WKST01.samplecorp.com` nhiều khả năng bắt đầu từ email phishing đính kèm file `cv.pdf`, dựa trên các dấu hiệu sau:

- Người dùng đang dùng email client `Mozilla Thunderbird`
- File `cv.pdf` được mở bằng Adobe Reader 10.0, phiên bản cũ có nhiều lỗ hổng đã biết
- Lệnh độc hại được thực thi ngay sau khi người dùng mở file

![image](/assets/images/dfir/31fbc35f-72fd-81ae-9a2b-ce3298a10d7f.png)

`wmiprvse.exe` được xác định là parent process đã spawn `cmd.exe` và `powershell.exe` một cách bất thường.

![image](/assets/images/dfir/31fbc35f-72fd-811c-9760-d6724a072486.png)

![image](/assets/images/dfir/31fbc35f-72fd-81e4-8c5b-c885994e25ab.png)

Các PowerShell script độc hại được thực thi từ `wmiprvse.exe`:

![image](/assets/images/dfir/31fbc35f-72fd-816b-b82c-f50a0ee89dce.png)

**Phân tích IP 192.168.220.66**

Log sự kiện ghi nhận một loạt host kết nối đến IP này. Tổng hợp từ SIEM xác nhận `192.168.220.66` là máy của kẻ tấn công đang điều khiển `WKST01.samplecorp.com`. Bằng chứng cũng cho thấy kẻ tấn công tiếp tục lateral movement sang `HR01.samplecorp.com`.

**Phân tích HR01.samplecorp.com**

Packet capture ghi nhận traffic đáng ngờ giữa `192.168.220.66` và `HR01.samplecorp.com`:

![image](/assets/images/dfir/31fbc35f-72fd-81c7-90cc-c5ffa431a18a.png)

Traffic phân tích cho thấy kẻ tấn công gửi buffer overflow payload vào service đang lắng nghe tại port `31337` của HR01.

![image](/assets/images/dfir/31fbc35f-72fd-814c-baee-c6fb6275fa26.png)

Chuyển đổi raw traffic sang binary và phân tích bằng shellcode debugger `scdbg`:

![image](/assets/images/dfir/31fbc35f-72fd-8183-ac2e-d962eee1f997.png)

`scdbg` xác nhận shellcode thiết lập reverse connection về `192.168.220.66:4444`. Đây là dấu hiệu rõ ràng của việc khai thác buffer overflow tại port `31337` trên `HR01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-81ac-adaa-cd2c31a3f179.png)

Phân tích network connection xác nhận lưu lượng hai chiều giữa HR01 và `192.168.220.66`, với kết nối C2 thiết lập qua port `4444`. Kẻ tấn công đã chiếm quyền điều khiển `HR01.samplecorp.com` thành công.

![image](/assets/images/dfir/31fbc35f-72fd-8165-85f6-c3b98354cc5d.png)

### Indicators of Compromise (IoCs)

- `C2 IP`: 192.168.220.66
- `cv.pdf` (SHA256): ef59d7038cfd565fd65bae12588810d5361df938244ebad33b71882dcf683011

### Root Cause Analysis

Nguyên nhân cốt lõi là cấu hình network access control quá lỏng lẻo, cho phép thiết bị bên ngoài kết nối vào mạng nội bộ.

Các điểm yếu được xác định:
1. **Phần mềm lỗi thời**: Adobe Acrobat Reader phiên bản cũ không được vá, bị khai thác để tải payload.
2. **Lỗ hổng ứng dụng nội bộ**: Buffer overflow trong ứng dụng nội bộ cho phép kẻ tấn công leo thang sang toàn bộ `HR01.samplecorp.com`.
3. **Network segmentation yếu**: Thiếu phân tách mạng hiệu quả, cho phép lateral movement dễ dàng.
4. **Nhận thức bảo mật thấp**: Người dùng mở file đính kèm từ email không rõ nguồn gốc.

### Technical Timeline

| Thời gian | Sự kiện |
|---|---|
| Initial Compromise | Người dùng mở file `cv.pdf` độc hại, Adobe Reader bị exploit |
| Lateral Movement | Kẻ tấn công di chuyển từ WKST01 sang HR01 qua buffer overflow |
| Data Access | Kẻ tấn công truy cập database nhân sự trên HR01 |
| C2 Communications | Reverse connection về `192.168.220.66:4444` được thiết lập |
| Malware Deployment | PowerShell payload và shellcode được deploy |
| Containment | 22/04/2019 03:43:34 — Cô lập VLAN được thực hiện |
| Eradication | Malware removal và patch triển khai |
| Recovery | Hệ thống được khôi phục và tăng cường bảo mật |

### Nature of the Attack

Kẻ tấn công sử dụng TTPs phù hợp với framework Metasploit, bao gồm:

**Nhận diện Metasploit**

PowerShell payload được xác định có pattern đặc trưng của Metasploit, sử dụng double encoding để né tránh detection.

![image](/assets/images/dfir/31fbc35f-72fd-81f3-a951-c9f03acebdbb.png)

Sau khi decode payload, đội SOC xác nhận đây là Meterpreter shellcode thực thi trực tiếp trong memory của `WKST01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-815b-b2ca-c347a6120fbd.png)

Phân tích OSINT xác nhận PowerShell pattern này thuộc về framework Metasploit.

![image](/assets/images/dfir/31fbc35f-72fd-8115-950c-de0663598689.png)

Để xác nhận thêm, binary shellcode từ network packet được submit lên VirusTotal:

![image](/assets/images/dfir/31fbc35f-72fd-8144-895d-e599a041d1de.png)

![image](/assets/images/dfir/31fbc35f-72fd-81aa-9d3b-f407938d08c7.png)

![image](/assets/images/dfir/31fbc35f-72fd-817b-b3e4-f78d342c5693.png)

VirusTotal xác nhận đây là Metasploit payload với signature `shikata` encoder — đặc trưng của Metasploit shellcode.

---

## Impact Analysis

Phân tích tác động đã được trình bày trong Executive Summary ở đầu bản báo cáo. Dựa trên mức độ xâm nhập vào hệ thống nội bộ và các quy định pháp lý liên quan, hậu quả của sự cố này bao gồm nguy cơ lộ thông tin nhân sự và có thể phát sinh trách nhiệm pháp lý.

---

## Response and Recovery Analysis

### Immediate Response Actions

**Thu hồi quyền truy cập (Revocation of Access)**

- `Xác định tài khoản/hệ thống bị ảnh hưởng`: Sử dụng SIEM để truy vết các tài khoản và hệ thống liên quan đến `WKST01.samplecorp.com` và `HR01.samplecorp.com`.
- `Thời gian thực hiện`: Phát hiện lúc `22/04/2019 01:05:00`, quyền truy cập bị thu hồi và C2 bị chặn vào `22/04/2019 03:43:34`.
- `Phương pháp`: Cập nhật rule firewall, force log-off các session đang hoạt động, vô hiệu hóa tài khoản nghi ngờ và đổi tất cả API keys.
- `Hiệu quả`: Ngăn chặn lateral movement thêm và hạn chế nguy cơ data exfiltration.

**Chiến lược Containment**

- `Short-term Containment`: Áp dụng VLAN segmentation để cô lập `WKST01` và `HR01` khỏi phần còn lại của network, ngăn chặn lateral movement.
- `Long-term Containment`: Lên kế hoạch triển khai network segmentation nghiêm ngặt hơn và cập nhật network access control policy để giảm attack surface.
- `Hiệu quả`: Kẻ tấn công bị ngăn không thể di chuyển sang các hệ thống liền kề.

### Eradication Measures

**Malware Removal**

- `Xác định malware`: Phát hiện các process bất thường và xác nhận Metasploit payload qua VirusTotal.
- `Phương pháp loại bỏ`: Sử dụng tool chuyên dụng để gỡ bỏ malware khỏi `WKST01` và `HR01`.
- `Xác nhận`: Quét lại bằng heuristic analysis để đảm bảo không còn malware tồn tại.

**System Patching**

- `Xác định lỗ hổng`: Adobe Acrobat Reader phiên bản cũ và ứng dụng nội bộ có lỗ hổng buffer overflow.
- `Triển khai patch`: Cập nhật tất cả phần mềm liên quan, patch lỗ hổng buffer overflow trong ứng dụng nội bộ.
- `Fallback`: Chuẩn bị quy trình rollback trong trường hợp patch gây ảnh hưởng đến hoạt động.

### Recovery Steps

- `Backup Validation`: Xác minh tính toàn vẹn của backup trước khi restore.
- `Restoration Process`: Khôi phục hệ thống từ backup sạch.
- `Data Integrity Checks`: Kiểm tra dữ liệu sau khi restore đảm bảo không bị thay đổi.
- `Security Measures`: Cấu hình lại firewall rules, cập nhật IDS signatures.
- `Operational Checks`: Kiểm tra hệ thống hoạt động bình thường trước khi đưa vào production.

### Post-Incident Actions

**Enhanced Monitoring:**
- Tăng cường logging và monitoring trên các hệ thống quan trọng.
- Tích hợp các IoC mới vào SIEM để phát hiện pattern tương tự.

**Lessons Learned:**
- **Gap Analysis**: Network access control không đủ chặt chẽ; thiếu network segmentation; phần mềm không được vá kịp thời.
- **Recommendations**: Triển khai patch management tự động; tăng cường network segmentation; đào tạo nhận thức bảo mật cho nhân viên (đặc biệt về phishing).
- **Future Strategy**: Xem xét triển khai Zero Trust Network Architecture và nâng cao quy trình vulnerability management định kỳ.
