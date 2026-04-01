---
layout: post
title: "DevOps Tools - Introduction"
date: 2026-04-01
categories: [devops]
tags: [devops]
---

![image](/assets/images/devops/13dbc35f-72fd-806b-9c8e-ed58883c3034.png)

## Original development step

![image](/assets/images/devops/13dbc35f-72fd-8058-a38c-f789e1408847.png)

## Working with team:

![image](/assets/images/devops/13dbc35f-72fd-8054-b989-d55fdea2dae9.png)

git là cli tools cung cấp việc code with tea và push lên github, github là nơi chứa repo của project đc push lên

## Testing:

- Vì push new build lên production có thể gây ra bug, … ta cần bước test
## CI/CD - **Continuous Integration** (Tích hợp liên tục) và **Continuous Delivery/Continuous Deployment** (Phân phối liên tục/Triển khai liên tục)

- Là một phương pháp trong DevOps giúp tự động hóa và tối ưu hóa quá trình phát triển phần mềm. Đối với cách vận hành truyền thống ta cần phải lưu, build và test toàn bộ source lại từ đầu khi update 1 tính năng nào đó → không tối ưu.
- CI/CD giúp tự động hoá quá trình
## Container

- Trong quá trình vận hành triển khai, 1 sản phẩm đc dev sẽ có env vì vậy các bước build test, production cũng phải có chung env → container giải quyết vấn đề
- Container đóng gói app và env của nó thành image và có thể chạy image trên mọi os, mọi hệ thống giúp cho việc vận hành đc tự động hoá hơn
## K8S

- Giả sử để mở rộng giai đoạn production, số lượng server đc tăng thêm và các server sẽ chạy các container trên đó → để quản lý các container cần k8s
- k8s giúp định nghĩa cần deploy bao nhiêu container và đảm bảo các container hđ 1 cách giống với cấu hình đc định nghĩa. k8s giúp auto-scale số lượng container cần thiết dựa trên cơ sở hạ tầng, manage resources, tối ưu resources
## Infrastructure as Code - IaC

- Containers và K8s giúp đảm bảo tính nhất quán của ứng dụng giữa các môi trường nhờ đóng gói ứng dụng và quản lý việc triển khai thì Infrastructure as Code (quản lý và cấu hình hạ tầng) có thể hiểu là bạn có thể thiết lập/quản lý những stack trước kia của hệ thống thông qua việc định nghĩa chúng trong 1 file script chẳng hạn thay vì tốn thời gian và công sức setup manual từng thứ (chạy docker run, cài package, lib trên server mới, …).
- VD khi triển khai k8s, gg cloud, aws, thay vì phải lên từng cái để cấu hình, IaC sẽ giải quyết việc này.
Tổng kết:

![image](/assets/images/devops/13fbc35f-72fd-803e-b130-ea7b986fd87b.png)

