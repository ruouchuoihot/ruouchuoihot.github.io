---
title: "Splunk Fields và Data Models: Cách Đọc Dữ Liệu Nhanh Hơn"
date: 2026-03-31
category: siem
tags: [splunk, siem, fields, data-models, cim, blue-team]
excerpt: "Ghi chú thực hành về field, interesting field, field type, metadata browsing và data model trong Splunk."
---

Bài này tôi nhào nặn lại mấy cái note `Splunk Using Field` chung với cái đoạn móc mớ data thực tế ở trỏng bài `Data & tools for Defend Analysts` luôn. Ngắn gọn là cách nhảy dạo coi data của mình đang sống ở ngõ ngách nào.

## Tại sao Fields lại đáng giá đến thế?

Mấy tay mới chạm vô Splunk y như rằng cứ dí mắt xói mòn vào thanh search bar. Thực ra, tốc độ phá án (tức tốc độ investigation) ngậm ngùi phụ thuộc phần trăm siêu to lớn vào việc người chơi hệ Splunk nắm rõ field (trường dữ liệu) đến cỡ nào.

Cứ extraction đúng và bung chuẩn normalized, anh em dư dả khả năng:

- Bẻ lái chuyển hướng (pivot) trong vòng bán kính nửa nốt nhạc
- Filter gạn đục vớt trong bãi events sạch sẽ láng mướt
- Aggregate nhào nặn kết quả chả dính một hột nhiễu rác
- Gắn mạch mớ data sang detections siêu hạng hay dàn data models rắc rối sau này

## Giải phẫu Interesting Fields

Có một trò khá mướt của Splunk là gắn biển báo `interesting fields` (Trường dữ liệu quan trọng) một khi thằng Splunk đánh hơi được nó ngụp lặn rải rác đủ liều lượng trong lượng data đổ ra và chắc cốp là nó hữu ích để ae bới lông tìm vết.

![Interesting fields in Splunk](/assets/images/splunk/using-field-interesting-fields.png)

Trích nôm na từ note:

- Cứ vọc tay vô mấy trường này là ưu tiên số một lúc nhào vô triage (phân loại độ khẩn nổ alert) lẹ nhất.
- Chúng chổng mông mách nước cho mấy trục xoay sở (strongest pivots) khỏe nhất trên đống mâm bát hiện hữu.
- Hạ triệt để thời gian mỏi mắt cuốc bộ gõ line by line mò mẫm mớ text lềnh bềnh thô sơ raw events.

Riêng món này mà bứng ra dùng trên mớ logs xa lạ mới tanh, quả rưỡi là ngon tuyệt.

## Bảng hiệu String fields và Numeric fields

Thêm một thủ thuật ruồi bu xíu nhưng thực chiến cực kỳ khi coi thằng Splunk dán biển phân biệt chủng loại:

![Field type indicators in Splunk](/assets/images/splunk/using-field-field-types.png)

Ngó bằng mắt UI:

- `a` dán mác cho mấy gã chữ nghĩa kéo dây giá trị rặt hệ string (chuỗi).
- `#` dẹp mác cho mấy khứa số lộn (tính giá trị numeric).

Nhớ cho kỹ cái phân hóa này khi quyết ném chúng vô:

- Trò filter rút cạn
- Thống kê chằng chịt ngòi `stats` command
- Mấy thanh biểu đồ Visualizations
- Vẽ ra khối logic ngưỡng threshold để bật đèn đỏ bão

## Kéo giãn coi Field Details

Búng tay click vô một field phọt luôn cái chân tướng của mớ distribution (phân bổ số lượng) với cả giá trị chả còn sót lại gì.

![Field detail panel in Splunk](/assets/images/splunk/using-field-field-details.png)

Trò này là phao cứu sinh nhanh lẹ nhất để dội câu hỏi:

- Thằng value nàoo hay ngóc đầu lên nhất
- Value nào là quý hiểm (rare)
- Thật sự thì ráp cái field này để quay trục móc ra nghi can có thơm ngon hay đắng nghét

## Dạo phố bằng Browsing Hosts, Sourcetypes, và Sources

Thú vui tao nhã trước lúc ôm súng nhào vô bùn đen là gọi thẳng `metadata commands` dạo một vòng kiểm đếm kho đạn: Biết mình biết hệ thống có rác gì.

### Quét xem cái mâm Hosts

```spl
| metadata type=hosts index=*
```

![Browsing hosts with metadata](/assets/images/splunk/defense-analyst-browse-hosts.png)

Bắn cái pằng phọt ra:

- Thằng ma nào đang nôn dữ liệu (hosts đang tống log)
- Thằng nào đang gào thét khỏe ru
- Nên khoanh chỗ nào để khui tiếp (investigation nhảy vào)

### Quét điểm mặt Sourcetypes

```spl
| metadata type=sourcetypes index=*
```

![Browsing sourcetypes with metadata](/assets/images/splunk/defense-analyst-browse-sourcetypes.png)

Cái mâm này bày ra toàn bộ thể thức log các hãng đổ về nhà mình.

### Quét tới chân ngọn ngách Sources

```spl
| metadata type=sources index=*
```

![Browsing sources with metadata](/assets/images/splunk/defense-analyst-browse-sources.png)

Lòi ra cho anh em chèn rễ từng lỗ mũi của đống file quăng log trào lưu.

## CIM (Common Information Model) - Thế lực mài nhãn Normalize

`CIM` có thể nói nôm na là đỉnh chóp ngòi nổ tối quan trọng của Splunk trong dân bảo mật vì rổ quy tắc gọt sạch data về nằm chung khuôn mẫu chung cấu trúc.

![Splunk CIM view](/assets/images/splunk/defense-analyst-cim.png)

Sườn của cụ CIM rành rành ra:

- Dăm ba cái hãng văng chung một mớ hoạt động tương đối ngang ngữ nhau nhưng văng bằng đủ cấu trúc giang hồ.
- Bứt cái tay CIM thì ép thằng Splunk nén chung cục mô hình (shared model) cho cái bãi sự kiện rối mù đó.
- Xài tới detection xịn mịn xắt tới dashboard là ăn trọn cú mượt mà. Đống lề nén sạch sành sanh chung một quy cũ thì cái gì cũng nhẹ đầu (portable).

Hiểu sao việc gọt đẽo khui móc chất lượng (Field extraction) lừ lừ đằng trước là siêu đắt.

## Thế còn Data Models thì sao?

Dàn hậu cần Data models nằm trễm chệ đè trên đám data gọt sẵn normalized, việc cào mớ phân tích an ninh đùn lên tới nóc ngọc hoàng chớp nháy nhanh gọn.

Ví dụ bỏ túi từ cái note cũ xì:

```spl
| tstats summariesonly=true count from datamodel=Endpoint.Processes where Processes.user="*" Processes.process=* Processes.parent_process=* Processes.user="*" groupby _time span=1s Processes.process Processes.parent_process Processes.user | `drop_dm_object_name("Processes")`
| table _time process parent_process user count
| sort + _time
```

Rút thanh củi này ra đập vì:

- Mã `tstats` chạy bằng điện vượt hàng chục ki-lô ngàn lần cách lết bò của search raw event thô.
- Bằng cái data models rủng rỉnh này thì tha hồi dập theo kiểu lặp đi lặp lại ra analytics xịn.
- CIM bắt cặp cùng Data Models bưng cục detection này rinh đem chỗ khác (portable) nướng ngon mướt.

## Chốt gạch (Takeaway)

Với tôi, ba cái mớ Fields không phải cái trò búng chỏ của đám mới vô nêm. Nó phải xem như gạch móng tạc dựng lên bệ chóp cho tất cả thể loại thao tác:

- Bới coi (Exploration)
- Đào hang bắt ếch (Investigation)
- Nắn gọt đẽo (Normalization)
- Tung gậy (Detections)
- Trải bàn nhậu (Dashboards)

Trường mà rác, nhắm mắt cắm đầu thì vứt trọn mấy thằng đứng trên tầng nóc. Khóc!
