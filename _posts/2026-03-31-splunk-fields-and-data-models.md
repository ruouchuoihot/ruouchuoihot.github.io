---
title: "Splunk Fields và Data Models: Cách Đọc Dữ Liệu Nhanh Hơn"
date: 2026-03-31
category: siem
tags: [splunk, siem, fields, data-models, cim, blue-team]
excerpt: "Ghi chú thực hành về field, interesting field, field type, metadata browsing và data model trong Splunk."
---

Bài này tổng hợp lại các ghi chú về `Splunk Using Field` kết hợp với phần thực hành data trong bài `Data & tools for Defend Analysts`. Mục tiêu là nắm được cách duyệt và khai thác data hiệu quả trong Splunk.

## Tại sao Fields quan trọng?

Người mới dùng Splunk thường chỉ tập trung vào thanh search bar. Thực tế, tốc độ investigation phụ thuộc rất lớn vào việc hiểu rõ các field (trường dữ liệu).

Khi field được extract đúng và normalize chuẩn, ta có thể:

- Pivot nhanh giữa các góc nhìn khác nhau
- Filter chính xác những event cần thiết
- Aggregate kết quả không bị nhiễu
- Kết nối data vào detection rules hoặc data models

## Interesting Fields

Splunk tự động gắn nhãn `interesting fields` cho những field xuất hiện đủ nhiều trong kết quả và có giá trị phân tích.

![Interesting fields in Splunk](/assets/images/splunk/using-field-interesting-fields.png)

Đặc điểm:

- Đây là các field nên ưu tiên kiểm tra đầu tiên khi triage alert.
- Chúng cung cấp các pivot point mạnh nhất trên tập data hiện có.
- Giảm đáng kể thời gian phải đọc raw events thủ công.

Đặc biệt hữu ích khi làm việc với nguồn log mới chưa quen.

## String Fields và Numeric Fields

Splunk phân biệt loại field bằng icon trên giao diện:

![Field type indicators in Splunk](/assets/images/splunk/using-field-field-types.png)

Cách nhận biết:

- `a` — field chứa giá trị kiểu string (chuỗi ký tự).
- `#` — field chứa giá trị kiểu numeric (số).

Phân biệt này ảnh hưởng trực tiếp khi sử dụng:

- Filter conditions
- `stats` command
- Visualizations
- Threshold logic cho alerting

## Field Details

Click vào một field sẽ hiển thị chi tiết về distribution (phân bổ) và danh sách các giá trị.

![Field detail panel in Splunk](/assets/images/splunk/using-field-field-details.png)

Tính năng này giúp trả lời nhanh:

- Value nào xuất hiện nhiều nhất
- Value nào hiếm gặp (rare)
- Field này có đáng dùng để pivot trong investigation không

## Browsing Hosts, Sourcetypes và Sources

Trước khi bắt tay vào investigation, nên dùng `metadata commands` để khảo sát tổng quan data đang có.

### Duyệt Hosts

```spl
| metadata type=hosts index=*
```

![Browsing hosts with metadata](/assets/images/splunk/defense-analyst-browse-hosts.png)

Kết quả cho biết:

- Host nào đang gửi log
- Host nào có lượng event nhiều nhất
- Nên tập trung investigation vào đâu

### Duyệt Sourcetypes

```spl
| metadata type=sourcetypes index=*
```

![Browsing sourcetypes with metadata](/assets/images/splunk/defense-analyst-browse-sourcetypes.png)

Hiển thị toàn bộ các loại log đang được thu thập.

### Duyệt Sources

```spl
| metadata type=sources index=*
```

![Browsing sources with metadata](/assets/images/splunk/defense-analyst-browse-sources.png)

Liệt kê chi tiết từng file/đường dẫn nguồn log.

## CIM (Common Information Model)

CIM là thành phần quan trọng của Splunk trong lĩnh vực bảo mật, dùng để normalize data về một cấu trúc chung.

![Splunk CIM view](/assets/images/splunk/defense-analyst-cim.png)

CIM hoạt động như sau:

- Nhiều nguồn log khác nhau ghi nhận cùng loại sự kiện nhưng với format khác nhau.
- CIM áp dụng một shared model để chuẩn hóa các sự kiện này về cùng cấu trúc.
- Nhờ đó, detection rules và dashboard có thể tái sử dụng (portable) trên nhiều nguồn data khác nhau.

Đây là lý do field extraction chất lượng ngay từ đầu rất quan trọng.

## Data Models

Data models nằm trên nền data đã được normalize, giúp việc phân tích bảo mật nhanh hơn đáng kể.

Ví dụ query sử dụng data model:

```spl
| tstats summariesonly=true count from datamodel=Endpoint.Processes where Processes.user="*" Processes.process=* Processes.parent_process=* Processes.user="*" groupby _time span=1s Processes.process Processes.parent_process Processes.user | `drop_dm_object_name("Processes")`
| table _time process parent_process user count
| sort + _time
```

Ưu điểm:

- `tstats` chạy nhanh hơn gấp nhiều lần so với search raw events thông thường.
- Data models cho phép xây dựng analytics có thể tái sử dụng.
- CIM kết hợp Data Models giúp detection rules portable giữa các môi trường.

## Tổng kết (Takeaway)

Fields không phải khái niệm cơ bản để bỏ qua. Nó là nền tảng cho tất cả các thao tác:

- Exploration — khám phá data
- Investigation — điều tra sự cố
- Normalization — chuẩn hóa dữ liệu
- Detections — viết rule phát hiện
- Dashboards — trực quan hóa

Nếu field extraction kém chất lượng, tất cả những gì xây dựng phía trên đều bị ảnh hưởng.
