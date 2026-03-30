# CTF Blog

Blog cá nhân về CTF writeups và kiến thức Cyber Security.

## 🚀 Deploy lên GitHub Pages

### Bước 1: Tạo GitHub Repository
1. Vào [github.com/new](https://github.com/new)
2. Đặt tên repo: `<username>.github.io` (thay `<username>` bằng GitHub username của bạn)
3. Chọn **Public**
4. Click **Create repository**

### Bước 2: Push code lên GitHub
```bash
cd E:\app\ctf-blog
git init
git add .
git commit -m "Initial commit: CTF Blog"
git branch -M main
git remote add origin https://github.com/<username>/<username>.github.io.git
git push -u origin main
```

### Bước 3: Bật GitHub Pages
1. Vào repo Settings → Pages
2. Source: chọn **GitHub Actions** (hoặc **Deploy from a branch** → `main`)
3. Đợi 1-2 phút, truy cập `https://<username>.github.io`

## 📝 Viết bài mới

### Blog post thường
Tạo file trong `_posts/` theo format:
```
_posts/YYYY-MM-DD-ten-bai-viet.md
```

### CTF Writeup
Tạo file trong `_writeups/`:
```
_writeups/ten-challenge.md
```

## 📁 Cấu trúc thư mục

```
ctf-blog/
├── _config.yml          # Cấu hình Jekyll
├── _layouts/            # Layout templates
├── _includes/           # Components tái sử dụng
├── _posts/              # Blog posts
├── _writeups/           # CTF writeups
├── assets/
│   └── css/
│       └── style.css    # Theme CSS
├── index.html           # Trang chủ
├── writeups.html        # Trang danh sách writeups
└── about.md             # Giới thiệu
```

## 🎨 Tuỳ chỉnh

- Sửa `_config.yml` để đổi tên blog, author info
- Sửa `assets/css/style.css` để thay đổi theme
- Sửa `_layouts/` để thay đổi layout
