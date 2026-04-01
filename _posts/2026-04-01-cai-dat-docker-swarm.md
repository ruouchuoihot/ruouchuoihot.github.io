---
layout: post
title: "Cài đặt Docker Swarm"
date: 2026-04-01
categories: [devops]
tags: [devops]
---

## Một số lưu ý:

## Kiến trúc Swarm Cyberrange: Manager (10.11.13.51), Worker (10.11.13.40)

1. Khởi tạo swarm trên node 10.11.13.51
1. Worker Join vào cluster
1. Verify:
1. Promote và demote các node trong Swarm
1. Update các node trong Swarm
[https://docs.docker.com/engine/swarm/stack-deploy/](https://docs.docker.com/engine/swarm/stack-deploy/)

## Cài đặt NFS server để share folder dùng chung giữa các node

NFS server (10.11.13.40), NFS client (10.11.13.51)

1. Mở port 2049 để sử dụng NFS trên 2 host
1. Cài đặt NFS server trên 10.11.13.40
1. Cài đặt NFS common trên Client 10.11.13.51
1. Tạo folder dùng chung trên server
1. Cấu hình NFS export trên server
1. Tạo folder /var/data trên client giống với server và mount folder:
1. Cấu hình để client tự mount NFS directory khi boot
1. Verify
[https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04)

