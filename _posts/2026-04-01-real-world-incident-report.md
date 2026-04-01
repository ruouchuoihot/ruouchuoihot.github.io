---
title: "Báo Cáo Sự Cố Thực Tế (Real-world Incident Report)"
date: 2026-04-01
category: dfir-knowledge
tags: [dfir, incident-response, malware, soc, blue-team]
excerpt: "Mẫu báo cáo Incident Report một vụ xâm nhập nội bộ với thủ đoạn payload nắn gân PowerShell, xài Metasploit, exploit buffer overflow và rón rén dòm ngó data."
---

# **Báo cáo Sự cố Thực tế (Real-world Incident Report)**

## **Bản tóm tắt Executive Summary**

- `Incident ID`: INC2019-0422-022
- `Độ nghiêm trọng`: High (P2)
- `Tình trạng sự cố`: Đã khắc phục (Resolved)
- `Tổng quan sự kiện`: Vào rạng sáng ngày `22/04/2019`, lúc đúng `01:05:00`, biệt đội SOC của SampleCorp hú còi đinh tai về dấu vết unauthorized (trái phép) rục rịch thọt vào mạn lưới mạng nội bộ (internal network). Tín hiệu phát nổ chủ yếu từ bộ đếm cọc cạch những tiến trình process dị dạng (anomalous process) phòi ra đi kèm một đống tập lệnh rác rưởi bằng PowerShell hắc ám.
Kẻ thù thừa cơ ăn hôi cái rào cản sơ sài trong network access controls (kiểm soát truy cập mạng) với thọt móc hai lổ thủng bảo mật giăng chờ sẵn tróc nã toàn phần để chễm chệ đoạt quyền điều khiển (gain control) một lượng lớn tụ điểm nút giao thông mấu chốt:
- `Phát hiện cốt tử (Key Findings)`: Chỉ một đống network policy lủng lỗ cũng đủ đẻ ra con internal IP cho tên lựu đạn kia nghiễm nhiên đập cáp Ethernet dạo công ty hệt như sếp dòm lính. Đi sâu vào phá án moi ruột lòi ra thằng này băm vào trúng khoẻ `WKST01.samplecorp.com` chỉ bằng cách câu exploit vô con lổ phơi hàng sẵn của `Acrobat Reader`.
Chưa dừng ở con số một điểm dính đạn, khứa nhào nặn luôn quả `buffer overflow vulnerability` đục băm thêm con app vườn nhà SampleCorp làm rốn nhún chui tợn vào nội khu.
Dù mẻ lưới dữ liệu to tổ chảng chưa bị cào sạch (no widespread data exfiltration) nhờ ơn cự binh biệt đội SOC/DFIR kéo sập mạc, dư âm hậu chấn từ lỏ mâm xâm phạm thô thiển đối với tổ kiến mọng `WKST01.samplecorp.com` và cả khu rốn HR `HR01.samplecorp.com` cũng gióng rụng tai. Nguy cơ vung vãi rác công ty ra dơ mặt cho dù ít cũng dính.
- `Phản hồi thần tốc (Immediate Actions)`: Toàn đội SOC x DFIR tự chơi mâm nhà chứ chả rảnh thuê ngoài dòm ngó. Vạch thẳng đường ranh cô lập mấy máy móc thối hoắc đi tong bằng dao phay mảng chia VLANs (VLAN Segmentation).
Để tiện bề phá án vỡ nợ tổ chức rớt rác khắp nẻo đường, SOC/DFIR cắm đầu vô vét toàn bãi chứng cứ bằng màn hứng Network Traffic Captures. Ngay trong cơn nước rút rịt đống máy đó xâu vào kim hoàn Host Security. Log lội các thể loại cũng đổ dồn dập về tổng bộ Elastic SIEM chổng đầu hứng hớt tự động.

## **Phân tích Chuyên sâu (Technical Analysis)**

### **Hệ thống tịt ngòi & Dữ liệu bốc hơi (Affected Systems & Data)**

Toét nòng ngán do Network Access Controls sơ hở lỏng lẻo chình ình, cái thực thể (entity) rảnh háng kia cấp trớt con Internal IP nhờ điềm nhiên vớ sợi lõi đồng Ethernet đút róc tại công ty SampleCorp.

Khứa thành công đặt gót gạc toàn quyền lên ngõ điểm chèn mạng lưới nội tình khép kín SampleCorp:

- `WKST01.samplecorp.com`: Tạm gọi bãi phát hành Development giấu nhẹm mớ rác source code (Mã nguồn nội bộ) nức tiếng sắp trào ra chợ. Đính lủng lẳng là dăm ba cái nốt API Keys chọt vào chuỗi dịch vụ bên thứ ba (Third-party services). Bọn xâm nhập mò nhẵn đống xó thư mục (directories bypass) thắp lên cơn rung kinh hoàng rách rốn: Sợ rách mẹ xớ bản quyền với nỗi uất hận dăm con Key bãi trượt bốc hơi nọc độc tứ tán.
- `HR01.samplecorp.com`: Bãi phế liệu chúa đựng dăm tờ khai thông tin HR (Nhân sự) nhét cục hằng hà sa số mảnh dính dáng personal (Thông tin định danh thân thể), ngân báu Payroll và review đấm lộn nhân viên rón rén. Manh lới chỉ về việc thằng mạt rệp kia trơn tuột ních thân vào hệ thống. Chấn động nhất là bị hốt phanh ổ Database phơi rốn trần trụi (Unencrypted) quật lỏng hớ hệ càn quấy Social Security numbers (Mã An sinh Xã hội) nối đít banh mã bank chéo vèo bãi hốc nhân viên. Không bắt quả tang lật úp cái trò nẫng tay trên, xong rủi ro lộ thóp Identity theft phọt bọt lừa đảo chấn động hãm thì chót vót.

### **Bằng chứng Cốt lõi & Tiến độ Điều tra (Evidence Sources & Analysis)**

**Khoảng vạch WKST01.samplecorp.com**

Lúc chớp chớp `22/04/2019`, đồng hồ phẹt vạch `01:05:00`, nhóm canh cổng rào SampleCorp SOC chộp gáy luồng ma mãnh. Tín hiệu vớt trơn màn gõ cảnh giác hằn in lẹ tay Parent-child process relationships méo mó kì dị thọt nguyên thanh PowerShell rác như hình dưới.

Nhìn dấu log xé toạc thì chóp mũ PowerShell bị vác súng tòi ra từ thằng `cmd.exe` thi hành dội script xả xa xăm Remote. Mà cay đắng là trỏ về rún IP `192.168.220.66` (Rõ mười mươi quả Internal Network chà léc khứa hôi của đứng lổ nhổ thọt lỗ thủng nội bộ).

![image](/assets/images/dfir/31fbc35f-72fd-814f-ad37-d6536e2e521a.png)

Soi lủng đoạn thì cái màn bóc phốt thực thi trái lệnh chỉ ngón cụt về tổ `WKST01.samplecorp.com` nát dính chấu, 99.9% là rước tà bám rịt bằng đuôi Email rác rưới đính theo mộc rác `cv.pdf` chỉ bởi mớ xằng xịt:

- Thằng dùng đụng ngón vọc con Client Mail huyền thoại `Mozilla Thunderbird`
- Rớt nhầm kéo bẹt màn rác dẻo `cv.pdf` dội app lủng Adobe Reader 10.0 rặt khú bãi, vá nát.
- Rõ mặt thọt lệnh đục chọc ác ý sau cái cú cick ngu nhóc đấy.

![image](/assets/images/dfir/31fbc35f-72fd-81ae-9a2b-ce3298a10d7f.png)

Trớ trêu bốc hơi cành, ông `wmiprvse.exe` xọt đùi thòi lòi lách nhách cho chóp mã `cmd.exe` với `powershell.exe` sinh tồn vô cớ.

![image](/assets/images/dfir/31fbc35f-72fd-811c-9760-d6724a072486.png)

![image](/assets/images/dfir/31fbc35f-72fd-81e4-8c5b-c885994e25ab.png)

Nhắc lại cho đỡ trớ, thằng quỷ dữ quật dạo nguyên mớ PowerShell băm vằm.

![image](/assets/images/dfir/31fbc35f-72fd-816b-b82c-f50a0ee89dce.png)

**Bóc ngắn gọn gã 192.168.220.66**

Thông báo log sổ lòi ra đội hình một dọc 4 mạng Hosts sượng rụng với mớ IP ngầm. Đỉnh điểm soi ngáp tới ngáp lui lại nổ đom đóm rờ cái mã `192.168.220.66` chỏng vó đè vạch vạch bãi log thu hoạch trên con hàng nát `WKST01.samplecorp.com`, đè tay đập móp sọ đính danh con nghiệt súc (unauthorized entity) đang cắm cọc luồn lách nhà người ta.

Cấu trúc bảng sau nốc nguyên nhát SIEM chưởng quật xói cho nhả nhớt cọng thi hành dội lệnh từ cuống rốn `192.168.220.66` gối trên mảng `WKST01.samplecorp.com`.

Sát chảo chứng cứ bung lụa giặc đã lòn trọt trôi thông chọt đống hàng: `WKST01.samplecorp.com` và cả ngạch bự `HR01.samplecorp.com`.

**Lăn lội HR01.samplecorp.com**

Tập kế dội dằn tới bến mảng `HR01.samplecorp.com` do cha quỷ xứ kia `192.168.220.66` lộ mặt cấu rễ nhầy với tụ HR01 găm ngọc gật gù luồng mạng dòm bằng Packet capture nhanh lẹ nhất cỏ.

![image](/assets/images/dfir/31fbc35f-72fd-81c7-90cc-c5ffa431a18a.png)

Xoi ngòi traffic tuôn dội màn Buffer overflow lấp liếm vào mồm Service phình phịch cắm mỏ tại port `31337` cái lò HR01.

![image](/assets/images/dfir/31fbc35f-72fd-814c-baee-c6fb6275fa26.png)

Rê gắp rác traffic thành Binary nguyên thủy đập tơi khô lòi bằng ruột con tool rạch bọc Shellcode debugger thần tháng `scdbg`.

![image](/assets/images/dfir/31fbc35f-72fd-8183-ac2e-d962eee1f997.png)

Thằng cún `scdbg` sủa gâu lòi ra Shellcode lấp lấp cấu nhão đòi bung vòi kéo chân kết nối bóc đùi dội về cái động nhện `192.168.220.66` tận port chà bát `4444`. Rành mạch là màn Exploitation con chóp bóp Buffer phọt nọc trên cổng rác tủi `31337` lò rốn cắm tại `HR01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-81ac-adaa-cd2c31a3f179.png)

Rượt bắt cuống cuồng nhát Network connection lềnh bềnh rũ rượi giằng co giữa thằng rách khía HR01 và tay to mặt lớn xằng bậy từ rổ rác gắp gói traffic chỏm. Ép ra phọt cứt mớ tròng rợ liên lạc giật gút về tà thần port `4444`. Chốt luôn đi, thằng đầu lĩnh đã bung rốn đấm toạc mã đục vách Buffer overflow xỏ ngòi kéo command dâm dật gỡ gạc banh đét `HR01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-8165-85f6-c3b98354cc5d.png)

*Cái độ thọc sâu (depth) bản cớ mớm phang tay bóc phốt mảng miếng này linh động tha hồ xả cho đội cúng bàn Stakeholder vạch rành chân rết băm vút.* Căn bản ném túm rác này nhỏ lẻ gọn nỏ là cho đỡ xoắn óc rách não, trong vũng lầy lội ngoài kia bới lông phải ném vèo sọt bằng rành thạch đúc cục chứng cứ khô mới yên mạng.

### **Cọc Tiêu Tố Giác (Indicators of Compromise - IoCs)**

- `C2 IP`: 192.168.220.66
- `cv.pdf` (SHA256): ef59d7038cfd565fd65bae12588810d5361df938244ebad33b71882dcf683011

### **Phục Dựng Nguyên Nhân Cốt Lõi (Root Cause Analysis)**

Gốc rễ sơ hở toang hoác cạn lõi rập rìu Network access control tưng bừng dâng trọn chòm chóp network của SampleCorp vào mõm sói.

Ngán nhẩm chốt phát mâm cộ do hại cục bọc rách bảo mật móm ruột. Thọt điểm thứ nhất lầy nhất ở cái trò chơi nhầy ngoác mồm ôm rốn cái thằng mảng già cụt hứng Acrobat Reader ế nhệ. Trò thứ hai lấn ruột cấn cái Buffer tràn đống cứt thúi đẻ trong App nội bộ lầy mủ lót mòm. Phết dăm mớ hão lại dội tới chót lấp mạng yếu hèn nghẹo gạch (nội cục Network segregation rách dẻ) vãi ỉa cho tụi chỏm rụng phơi ngực hứng dội bom. Ép nốt vô mảng nhét ngu học lãng xoẹt dân ngáo (kém nhận thức) lọt kẽ ngách training mớ Phishing sặc mùi để dâng mạng thọt kẽm ngách ngòi mâm.

### **Lịch Tự Ròng Rã (Technical Timeline)**

- Bắt đầu dính (Initial Compromise)
- Phọt ngòi leo dọc ngang (Lateral Movement)
- Cáo mâm nẫng dữ liệu (Data Access & Exfiltration)
- Đấm kết nối dội máy chú (C2 Communications)
- Vọt nọc Malware bung mủ (Malware Deployment or Activity)
- Kẹp phanh khóa mỏm (Containment Times)
- Nhai cứt dọn phét (Eradication Times)
- Lội lóp bục (Recovery Times)

### **Màu Bản Chất (Nature of the Attack)**

Cuốc khui móc dặm thẳng bụng kẻ ăn mày ngầm giang sơn, bắt ruột tuồn rác Tactics, Techniques, & Procedures (TTPs) xỏ lõi vào từng mảng ngoạm gạch của gã bợm. Đính xàm cút chỉ cách tay chơi SOC lật dập thẳng tay lũ Metasploit tì mọc nanh khéo.

**Ngửi Mùi Metasploit**

Ngứa não đào móc cho lủng kẽ tay giặc trò mài nhão PowerShell thọt lém lĩnh nổ bong bóng rụng lỗ tay.
Điển hình đấm cái Screenshot này lên mà soi cho tòe mắc lác quắn lác.

![image](/assets/images/dfir/31fbc35f-72fd-81f3-a951-c9f03acebdbb.png)

Vuốt cái bọng lòi tói gã dùng mã kéo mã (Double encoding) đánh thẹo chùi dọn sạch trơn detection. Lính SOC rách rưới phá tanh banh cái lõi Payload lộ mẻ PowerShell xát nguyên mặt thi triển chằng xọng bung vỡ óc trong Memory con bò nát `WKST01.samplecorp.com`.

![image](/assets/images/dfir/31fbc35f-72fd-815b-b2ca-c347a6120fbd.png)

Bơi ngửa với OSINT (Tình báo mã nguồn mở), tay sai SOC dõng dạc dóng đinh mảng PowerShell cợt nhả buộc chung nùi rốn với khung `Metasploit`.

![image](/assets/images/dfir/31fbc35f-72fd-8115-950c-de0663598689.png)

Để đỡ cứng càng nói mồm cho cái nghi mọt `Metasploit`, hất hàm đụp văng rốn bằng cước mổ ấu Shellcode dính nhũn. Xả nhị phân tháo đùn mớ Packet (Trọn gỏi `a.bin`) dúi cho mặt lợn VirusTotal móc óc rạch vách soi cật.

![image](/assets/images/dfir/31fbc35f-72fd-8144-895d-e599a041d1de.png)

![image](/assets/images/dfir/31fbc35f-72fd-81aa-9d3b-f407938d08c7.png)

![image](/assets/images/dfir/31fbc35f-72fd-817b-b3e4-f78d342c5693.png)

Kết cục VirusTotal in vết bằng nhành khằng định `Metasploit` chính cống gõ phím thiển gieo hờ. Chóp mỏ của mớ `metacoder` chen lõm `shikata` tòi lo gán với mã rớt từ mớ shellcode bồi ra từ Metasploit không chật vạch chữ đực ruồi.

---

## **Chấn động Vung Vãi (Impact Analysis)**

Mảng móc ngoét này bắt chóp đi luồn lọt xoắn vô bản Impact vạch lột lúc gáy sổ ở đầu Report. Dựa mặt với mảng miếng Internal rối nhũn với gọng kiềm luật lá lủng lỗ, cắm mũi thọt dao nặn nốt phọt rớt thê thảm của vụ phơi mình này trét bã lên thân cho khóm bậu xậu liên đới.

---

## **Vuông Góc Phá Lầy (Response and Recovery Analysis)**

### **Nhát Búa Tức Khắc (Immediate Response Actions)**

**Tháo Quyền Băm Cổ (Revocation of Access)**

- `Nhặt lá cành Accounts/Systems Nhám`: Xai ngọc xẹt rực SIEM rọi lấp lửng mớ quậy trốc dội tung mạc lở cợn trét bóng vào `WKST01.samplecorp.com`. Kéo ruột tòi mạng rờ lòi xoi chọt bãi rác HR01 văng ra thúm chùi nức mắt bị đút ngòi.
- `Bấm Đèn (Timeframe)`: Soi phọt bọt lúc `April 22, 2019, 01:05:00`. Chặn gáy cắt tiệt bám méo ở vạch chót `April 22nd, 2019, 03:43:34` với rọi cản ngạnh vách chặn họng rốn C2.
- `Ngón Tuyệt (Method of Revocation)`: Ghè ngàm nhót Firewall rịt cho bằng được tháo chuỗi Active Directory tọng sút (Force log-off) trôi dạt bay màu từ nùi account dính thọt tróc kẽm. Vuốt cho tát đổi rộp Password tuột xả văng hàm API Keys để chặn mỏ khứa cẩu xực khịt ngửi liếm cháp vô.
- `Dấu Ấn Máu (Impact)`: Lấy gáy cúp đuôi chọt ngang ngăn cước lết hông (Lateral movement), ngáng mạn chui nốt xỏ hệ thống khét để dành dồn dập tẩu mẻ dữ liệu thúi phèo (Data Exfiltration).

**Khoanh Bắt Ghì Mỏm (Containment Strategy)**

- `Bít Vòng Đoản (Short-term Containment)`: Màn chọt tọt nứt banh cái mỏ xẻ bằng VLAN segmentation văng nhát dao cô lập tách bầy luồn ngoét tụ `WKST01` với `HR01` bặt tăm cái lũ ngụp lặn network nứt lác ngăn trọn đường rảo chéo Lateral movement nghoe nguẩy.
- `Trét Bẫy Gọng Luân Đen (Long-term Containment)`: Chóp rọi tương lai vắt vẻo lộng phễu cho chia cắt mạng tít vòm (Network segmentation). Chỉ mặt đưa tụng riêng biệt thòi hạ tầng nén ngầm bằng Network access control khép hòm kín cứng mới chịu buông xấp mở lỗ nhét network thòm thèm. Chót ghim ngòi nạp dẹp mờ màn bãi công hạ mảng (Attack Surface).
- `Sờ Cằm Chém Rắn (Effectiveness)`: Ách họng kịch liệt cho khứa tay chơi đứng chững rịt chéo ngạc Escalation cũng đếch cắn trộm tụ kề ranh láng giềng bóc sạch, ghị phèo khứa quạt tơi bời sập ngáp tỏi.

### **Gạc Ma Đổ Ải Dọn Sạch Trơn (Eradication Measures)**

**Hút Mủ Dứt Điểm (Malware Removal)**

- `Làm Chớp Giật Mắt Găm (Identification)`: Chớp trúng bãi quá trình nhầy quặn dị tướng. Nương nớt chỏi vắt bóp ruột tròng vớt rướn lồi đống trát phân dơ `Metasploit` rặt nhũn bồi tụ với VirusTotal.
- `Chùi Phết Ngập Lau (Removal Techniques)`: Ụp lôi găm thần khí nạo xỉ sút mã độc chém đứt ngập vọt mạn lầy tải bự ra khỏi mớ tủi `WKST01` với `HR01` dọn bóng mướt mồ hôi.
- `Xác Cháy Xác Nhá Lộ Đom (Verification)`: Cuốc lượt hộc hơi móc rượt vòng sau quét nhũn, nhích nhẹ phân bua móng Heuristic lượn dòm gắp lôi cho khỏi xót hủ cút rác ngãi vung văng (rác rưới tàng nhẫn malware tồn kho dư).

**Lấp Lỗ Ố Trám Tường (System Patching)**
