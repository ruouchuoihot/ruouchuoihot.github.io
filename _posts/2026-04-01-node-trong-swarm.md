---
layout: post
title: "Quản lý Node trong Docker Swarm"
date: 2026-04-01
categories: [devops]
tags: [devops]
---

## 

Trong Docker Swarm, **node** là một thành phần cơ bản của cụm (cluster). Một Docker Swarm cluster bao gồm nhiều nodes, và mỗi node là một máy chủ chạy Docker Engine. Các nodes làm việc cùng nhau để cung cấp dịch vụ phân tán.

### 

### Các loại nodes trong Docker Swarm:

1. **Manager Node**:
1. **Worker Node**:
### Vai trò của node trong Docker Swarm:

- **Manager Node**:
- **Worker Node**:
### Giao tiếp giữa các nodes:

- Các nodes trong Docker Swarm giao tiếp với nhau qua giao thức **Raft** để duy trì trạng thái nhất quán của cluster.
- Quản lý giao tiếp giữa các nodes qua cổng:
### 

### Các lệnh liên quan đến nodes trong Docker Swarm:

1. Khởi tạo một Docker Swarm cluster:
1. Thêm một node mới vào cluster (lấy token từ manager node):
1. Danh sách nodes trong cluster:
1. Xóa một node khỏi cluster:
1. Thay đổi vai trò của một node:
