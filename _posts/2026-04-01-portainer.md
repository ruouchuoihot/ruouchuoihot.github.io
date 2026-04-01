---
layout: post
title: "Quản lý bằng Portainer"
date: 2026-04-01
categories: [devops]
tags: [devops]
---

## 1. Tổng quan

- Portainer app open-source dùng để quản lý thông qua UI cho Docker và các công nghệ container như Docker Swarm, Kubernetes
## 2. Các tính năng chính của Portainer

1. Quản lý Docker Containers
1. **Quản lý Images**
1. Quản lý network
1. Quản lý volumes
## File Portainer Stack

File docker compose để tạo Portainer stack

```shell
services:
  portainer:
    image: portainer/portainer-ce:2.24.0-alpine
    command: -H tcp://tasks.agent:9001 --tlsskipverify
    ports:
      - "9443:9443"
      - "9000:9000"
      - "8000:8000"
    volumes:
      - portainer_data:/data
    networks:
      - agent_network
      - traefik-public
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - node.role == manager
          - node.ip == 10.11.13.51
      labels:
        - "traefik.enable=true"
        - "traefik.docker.network=traefik-public"
        - "traefik.http.routers.portainer.rule=Host(`portainer.cyberrange.local`)"
        - "traefik.http.routers.portainer.entrypoints=websecure"
        - "traefik.http.routers.portainer.tls=true"
        - "traefik.http.routers.portainer.service=portainer"
        - "traefik.http.services.portainer.loadbalancer.server.port=9000"
        

  agent:
    image: portainer/agent:latest
    environment:
      AGENT_CLUSTER_ADDR: tasks.agent
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/volumes:/var/lib/docker/volumes
    networks:
      - agent_network
    deploy:
      mode: global

networks:
  agent_network:
    external: true
  traefik-public:
    external: true

volumes:
  portainer_data:
```

### **1. Service: **`portainer`

**Image**:

**Command**:

**Ports**:

**Volumes**:

**Networks**:

**Deploy**:

---

### **2. Service: **`agent`

**Image**:

**Environment**:

**Volumes**:

**Networks**:

**Deploy**:

---

### **3. Networks**

- `agent_network`:
- `traefik-public`:
---

### **4. Volumes**

- `portainer_data`:
## Deploy stack

### Chạy lệnh deploy stack:

```shell
docker stack deploy -c </path/to/yml/file> portainer -d
# -c là option dùng để chỉ định đường dẫn đến file cấu hình Docker Compose
# -d chạy lệnh trong chế độ nền (detached mode).
```

## Verify

Truy cập vào domain `https://portainer.cyberrange.local`**  **

![image](/assets/images/devops/162bc35f-72fd-80b8-b96d-f12316a48296.png)

