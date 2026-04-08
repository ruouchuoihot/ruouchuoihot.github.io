---
title: "Xây Dựng Splunk Security MCP Server Cho Blue Team"
date: 2026-04-08
category: siem
tags: [splunk, mcp, python, blue-team, siem, threat-hunting, mitre-attack, soc]
excerpt: "Ghi chú quá trình thiết kế và xây dựng một MCP Server kết nối AI assistant với Splunk, phục vụ các tác vụ Security Operations và Threat Hunting."
---

## Ý tưởng

Khi làm việc với Splunk, phần lớn thời gian của SOC analyst dành cho việc viết SPL query, tra cứu IOC, kiểm tra alert, và correlate event giữa nhiều nguồn log. Câu hỏi đặt ra: **nếu có thể kết nối một AI assistant trực tiếp vào Splunk thì workflow sẽ thay đổi như thế nào?**

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) là chuẩn mở cho phép AI assistant giao tiếp với các hệ thống bên ngoài thông qua tools, resources và prompts. Dự án này xây dựng một MCP Server chuyên biệt cho **Security Blue Team**, cho phép AI thực hiện trực tiếp các thao tác trên Splunk: từ chạy SPL query đến threat hunting tự động.



```
┌──────────────┐     MCP (stdio/SSE)    ┌────────────────────┐     REST API     ┌──────────┐
│ AI Assistant │ ◄────────────────────► │ Splunk Security    │ ◄──────────────► │  Splunk  │
│              │                        │ MCP Server         │    Port 8089     │ Instance │
└──────────────┘                        └────────────────────┘                  └──────────┘
```

## Kiến trúc tổng quan

Project được viết bằng Python, đóng gói thành package có thể cài bằng `pip install -e .` và chạy bằng `python -m splunk_security_mcp`.

```
splunk_security_mcp/
├── __main__.py           # Entry point — CLI
├── config.py             # Frozen dataclass settings từ .env
├── connector.py          # Async Splunk REST client + retry logic
├── validator.py          # SPL risk scoring engine
├── sanitizer.py          # Masking PII / credentials trong output
├── formatter.py          # Render output: JSON, Markdown, CSV, Summary
├── threat_hunter.py      # SPL query builders cho detection
├── mitre_atlas.py        # 26 MITRE ATT&CK techniques catalog
├── server.py             # MCP server: tools, resources, prompts
└── log.py                # Logging + audit trail
```

Một số quyết định thiết kế quan trọng:

- **Frozen dataclass cho config**: `AppSettings` dùng `@dataclass(frozen=True)` để đảm bảo config không bị thay đổi trong quá trình runtime. Toàn bộ giá trị load từ `.env` file.
- **Async HTTP client với retry**: `SplunkConnector` sử dụng `httpx.AsyncClient` với exponential backoff cho các lỗi transient (502, 503, 504, 429).
- **Lifecycle management**: Server dùng `asynccontextmanager` để quản lý vòng đời của Splunk connector — tự động mở connection khi start và đóng khi shutdown.

## Các module chi tiết

### 1. Risk Scoring Engine (`validator.py`)

Trước khi thực thi bất kỳ SPL query nào, server sẽ chấm điểm rủi ro từ 0 đến 100. Nếu điểm vượt ngưỡng (`RISK_THRESHOLD`, mặc định 75), query bị block.

Các yếu tố được kiểm tra:

| Rule | Điểm | Ý nghĩa |
|------|-------|---------|
| `\| delete` | 80 | Xóa data vĩnh viễn — rất nguy hiểm |
| `\| script/run/external` | 40 | Thực thi script bên ngoài |
| `index=*` không có filter | 35 | Scan toàn bộ data |
| All-time search | 50 | Không giới hạn thời gian |
| `transaction/map/join` | 20/cmd | Command tốn tài nguyên |
| Subsearch không limit | 20 | Có thể gây memory issues |

```python
def assess_query_risk(query: str, safe_window: str = "24h") -> RiskResult:
    q = query.lower()
    issues: list[_Issue] = []
    for fn in _CHECKS:
        issue = fn(q)
        if issue:
            issues.append(issue)
    total = min(sum(i.points for i in issues), 100)
    return total, message
```

Cơ chế này hoạt động như một **guardrail** — ngăn AI vô tình chạy những query phá hoại hoặc quá tốn tài nguyên trên production Splunk.

### 2. Sensitive Data Masking (`sanitizer.py`)

Khi bật `MASK_SENSITIVE_DATA=true`, output sẽ tự động redact các pattern nhạy cảm:

- **Credit card**: `4111-2222-3333-4444` → `****-****-****-4444`
- **SSN**: `123-45-6789` → `***-**-****`
- **AWS Access Key**: `AKIA...` → `AKIA****************`
- **Bearer Token**: `Bearer eyJ...` → `Bearer [REDACTED]`
- **API Key/Password headers**: `api_key: sk-xxx` → `api_key: [REDACTED]`
- **Email**: `admin@corp.com` → `a***n@corp.com`

Module dùng recursive scrubbing — parse sâu vào nested dict/list để đảm bảo không bỏ sót data nhạy cảm ở bất kỳ level nào.

### 3. Async Splunk Connector (`connector.py`)

HTTP client kết nối vào Splunk REST API (port 8089) với các tính năng:

- **Auth linh hoạt**: Hỗ trợ cả Splunk Token (`Authorization: Splunk <token>`) và Basic Auth (`username:password`).
- **Retry logic**: Tự động retry khi gặp 502/503/504/429 với exponential backoff (1s → 2s → 4s).
- **Query normalization**: Tự động thêm prefix `search` nếu query không bắt đầu bằng pipe `|`.
- **Dual-mode search**: Hỗ trợ cả `oneshot` (blocking) và `export` (streaming cho dataset lớn).
- **JSON parser**: Handle cả format chuẩn (`{"results": [...]}`) và line-delimited JSON từ export endpoint.

```python
class SplunkConnector:
    _RETRY_CODES = {502, 503, 504, 429}
    _MAX_RETRIES = 3
    _BACKOFF_BASE = 1.0

    async def oneshot(self, spl, earliest="-24h", latest="now", limit=100):
        resp = await self._request("POST", "/services/search/jobs/oneshot", ...)
        return self._parse_json_results(resp.text)
```

### 4. Threat Hunter Query Builders (`threat_hunter.py`)

Module này chứa các hàm tạo SPL query cho từng loại detection. Thay vì hardcode query, mỗi hàm nhận tham số linh hoạt và build query tương ứng.

**IOC Hunter** — tự phân loại IOC type (IP, hash, domain, email, URL, CVE) dựa trên regex:

```python
_IOC_PATTERNS = {
    "md5":     re.compile(r"^[a-fA-F0-9]{32}$"),
    "sha256":  re.compile(r"^[a-fA-F0-9]{64}$"),
    "ipv4":    re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    "domain":  re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"),
    "cve":     re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE),
    ...
}
```

Sau khi xác định type, query được build để search trên đúng các field liên quan. Ví dụ IOC type `ipv4` sẽ search trên `src_ip, dest_ip, source_ip, destination_ip, client_ip, remote_ip, dvc_ip`.

**Anomalous Execution Hunter** — phát hiện các pattern thực thi đáng ngờ:

- **Web/Office spawns shell**: `w3wp.exe` → `cmd.exe` (web server spawn shell — dấu hiệu web shell)
- **LolBin abuse**: Sử dụng `certutil`, `mshta`, `bitsadmin`, `regsvr32` cho mục đích độc hại
- **Obfuscated PowerShell**: Command chứa `-enc`, `-EncodedCommand`, hoặc `bypass`
- **Excessively long commands**: `CommandLine` dài hơn 500 ký tự

**Process-Network Correlation** — join Sysmon EventCode 1 (Process Create) với EventCode 3 (Network Connection) bằng `ProcessGuid` để biết chính xác process nào khởi tạo connection nào.

### 5. MITRE ATT&CK Catalog (`mitre_atlas.py`)

Tích hợp sẵn 26 kỹ thuật MITRE ATT&CK, mỗi kỹ thuật kèm template SPL query sẵn sàng thực thi:

| Platform | Số kỹ thuật | Ví dụ |
|----------|------------|-------|
| Windows | 10 | PowerShell (T1059.001), Scheduled Task (T1053.005), LSASS dump (T1003.001), RDP (T1021.001), SMB (T1021.002), Process Injection (T1055) |
| Linux | 6 | Shell Exec (T1059.004), Cron (T1053.003), SSH Keys (T1098.004), SUID (T1548.001) |
| Network | 5 | C2 Beaconing (T1071.001), DNS Tunneling (T1572), Port Scanning (T1046), Exfiltration (T1048.003) |
| Endpoint/EDR | 3 | Ransomware (T1486), Obfuscation (T1027), Malicious File (T1204.002) |
| Multi-platform | 2 | Service Creation (T1543.003), Brute Force (T1110.001) |

Cách hoạt động: gọi `mitre_search(technique_id="T1059.001")` → server lookup template SPL → thay thế `{index}` → chạy trực tiếp trên Splunk → trả về kết quả.

```python
@dataclass
class Technique:
    id: str          # T1059.001
    name: str        # PowerShell Execution
    tactic: str      # Execution
    platform: str    # windows
    description: str
    spl: str         # SPL query template
```

## Danh sách Tools (20+)

### Core Tools

| Tool | Mô tả |
|------|--------|
| `validate_spl` | Chấm điểm rủi ro SPL query (0-100) trước khi chạy |
| `search_splunk` | Chạy oneshot search với risk guard |
| `search_export` | Stream search cho dataset lớn |
| `get_indexes` | Liệt kê index kèm metadata |
| `get_saved_searches` | Liệt kê saved searches |
| `run_saved_search` | Chạy saved search theo tên |
| `get_server_config` | Kiểm tra config + Splunk health |

### Security / Blue Team Tools

| Tool | Mô tả |
|------|--------|
| `hunt_ioc` | Tìm kiếm IOC (IP, hash, domain, email, CVE) trên toàn bộ data |
| `hunt_anomalies` | Phát hiện suspicious execution: web shell, LolBin, obfuscation |
| `correlate_activity` | Join Process creation → Network connection (Sysmon Event 1 + 3) |
| `get_host_timeline` | Timeline an ninh theo thứ tự thời gian cho một host |
| `detect_bruteforce` | Phát hiện brute force (Windows + Linux + Web) |
| `detect_lateral_movement` | Phát hiện lateral movement qua logon + service creation |
| `detect_data_exfil` | Phát hiện data exfiltration (network + EDR) |
| `mitre_search` | Chạy detection theo MITRE ATT&CK technique ID |
| `list_mitre_techniques` | Duyệt catalog detection theo platform/tactic |
| `get_security_posture` | Tổng quan bảo mật: failed auth, account changes, firewall blocks |
| `analyze_user` | Phân tích hành vi user: login history, source IP, accessed systems |
| `check_log_sources` | Kiểm tra log source health — tìm source ngừng gửi data |
| `get_alert_history` | Liệt kê alert đã trigger gần đây |
| `get_query_history` | Audit trail — lịch sử query trong session |

## Guided Prompts cho SOC

Server cung cấp 3 prompt template hướng dẫn AI thực hiện workflow có cấu trúc:

### Incident Triage

Workflow 7 bước theo hướng **behavioral analysis** — không phụ thuộc vào tên process mà theo dõi execution chain:

1. Baseline môi trường (`get_security_posture` + `check_log_sources`)
2. Phát hiện anomaly (`hunt_anomalies`)
3. Deep-dive host (`get_host_timeline` + `correlate_activity`)
4. Map TTPs (`mitre_search`)
5. Pivot entity (`analyze_user` + `hunt_ioc`)
6. Kiểm tra persistence + lateral movement
7. Document evidence (`get_query_history`)

### Threat Hunt

Quy trình hunting 5 phase theo giả thuyết:
- Reconnaissance → Hypothesis-driven hunting → IOC sweep → Lateral movement & exfiltration → Reporting

### Daily SOC Review

Checklist đầu ca SOC analyst — đảm bảo không bỏ sót bất kỳ anomaly nào trong 24 giờ qua.

## Cấu hình và triển khai

### Environment Variables

| Biến | Mặc định | Ý nghĩa |
|------|----------|---------|
| `TRANSPORT` | `stdio` | Giao thức: `stdio` hoặc `sse` |
| `RISK_THRESHOLD` | `75` | Ngưỡng risk score tối đa (0-100) |
| `SAFE_TIME_WINDOW` | `24h` | Khoảng thời gian search an toàn |
| `MASK_SENSITIVE_DATA` | `false` | Bật/tắt masking PII trong output |
| `WINDOWS_INDEX` | `wineventlog` | Index Windows log |
| `LINUX_INDEX` | `linux` | Index Linux log |
| `NETWORK_INDEX` | `firewall` | Index network log |
| `EDR_INDEX` | `edr` | Index EDR log |

### Kết nối AI Client

**VSCode** — file `.vscode/mcp.json` đã bao gồm sẵn config, chỉ cần sửa credentials.

**Claude Desktop**:

```json
{
  "mcpServers": {
    "splunk-security": {
      "command": "python",
      "args": ["-m", "splunk_security_mcp"],
      "cwd": "E:/app/splunk-mcp-server",
      "env": {
        "SPLUNK_HOST": "your-splunk-host",
        "SPLUNK_PORT": "8089",
        "SPLUNK_USERNAME": "admin",
        "SPLUNK_PASSWORD": "your-password"
      }
    }
  }
}
```

**Docker**:

```bash
cp .env.example .env
docker compose up -d
```

## Ghi chú kỹ thuật

Một số điểm kỹ thuật đáng lưu ý trong quá trình phát triển:

- **SPL normalization**: Query người dùng nhập vào có thể không có prefix `search`. Connector tự xử lý — nếu query không bắt đầu bằng `|`, tự thêm `search `.
- **Docker networking**: Khi chạy trong Docker container, Splunk host cần trỏ về `host.docker.internal` thay vì `localhost`. Config `RUNNING_INSIDE_DOCKER=true` xử lý tự động.
- **Export vs Oneshot**: Oneshot blocking phù hợp cho query nhỏ, export streaming phù hợp cho dataset lớn. Cả hai đều qua risk check trước khi thực thi.
- **Audit trail**: Mọi thao tác đều được ghi log qua hàm `audit()`. Kết hợp với `get_query_history`, ta có thể trace lại chính xác những gì AI đã làm trên Splunk.

## Kết luận

MCP Server này giải quyết hai bài toán chính:

1. **Tăng tốc workflow**: SOC analyst không cần viết SPL thủ công cho các tác vụ lặp lại. Nói "kiểm tra brute force trong 24h qua" — AI tự build query và chạy.
2. **An toàn**: Risk scoring engine + sensitive data masking đảm bảo AI không vô tình phá hoại hoặc lộ thông tin nhạy cảm.



Với 20+ tools tích hợp sẵn, catalog 26 MITRE ATT&CK techniques, và 3 guided prompts, server này hoạt động như một **SOC co-pilot** — không thay thế analyst nhưng giảm đáng kể thời gian thao tác manual.

Source code: [splunk-mcp-server](https://github.com/ruouchuoihot/splunk-mcp-server)
