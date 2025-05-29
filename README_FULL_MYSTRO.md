# 🚀 مشروع mystro – إعداد متكامل من الألف إلى الياء (شامل هذه المحادثة)

هذا الملف التوثيقي (README) يجمع كافة خطوات إعداد مشروع mystro كما ناقشناها تفصيليًا خلال المحادثة، بما يشمل:

- إعداد مستخدم جديد على السيرفر
- توليد مفاتيح SSH وربطها بـ GitHub
- استنساخ مشروع Python من GitHub
- إنشاء بيئة افتراضية
- تشغيل المشروع محليًا
- تشغيل المشروع في بيئة الإنتاج باستخدام Gunicorn وNginx
- إعداد دومين فرعي مثل mystro.example.com مع دعم HTTPS (SSL)
- تعليمات الأمان وتحسين الإعدادات

---

## 🧱 1. إعداد مستخدم جديد على السيرفر

```bash
sudo deluser --remove-home mystro
```

```bash
sudo adduser mystro
```

```bash
sudo usermod -aG sudo mystro
```

```bash
sudo mkdir -p /home/mystro/.ssh
```

```bash
sudo touch /home/mystro/.ssh/authorized_keys
```

```bash
sudo chmod 700 /home/mystro/.ssh
```

```bash
sudo chmod 600 /home/mystro/.ssh/authorized_keys
```

```bash
sudo chown -R mystro:mystro /home/mystro/.ssh
```

---

## 🔐 2. توليد مفتاح SSH على جهازك المحلي

```bash
ssh-keygen -t ed25519 -C "mystro-server" -f %USERPROFILE%\.ssh\id_mystro
```

---

## 📤 3. نسخ المفتاح إلى السيرفر

```bash
ssh-copy-id -i %USERPROFILE%\.ssh\id_mystro.pub -p 13976 mystro@your_server_ip
```

أو:

```bash
scp %USERPROFILE%\.ssh\id_mystro.pub mystro@your_server_ip:/home/mystro/.ssh/authorized_keys
```

---

## 🔗 4. توليد مفتاح خاص لربط GitHub

```bash
ssh-keygen -t ed25519 -C "github-deploy"
```

```bash
cat ~/.ssh/id_ed25519.pub
```

> انسخه إلى GitHub → Settings → Deploy Keys → Add → ✅ Allow Read Access

---

## 📦 5. استنساخ المشروع من GitHub

```bash
git clone git@github.com:TamerOnLine/mystro.git
```

```bash
cd mystro
```

---

## 🐍 6. إعداد بيئة Python افتراضية

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

---

## 💻 7. تشغيل المشروع محليًا (Flask)

```bash
export FLASK_APP=app.py
```

```bash
export FLASK_ENV=development
```

```bash
flask run --host=0.0.0.0 --port=5000
```

---

## 🌐 8. إعداد Gunicorn وNginx

### Gunicorn:

```bash
gunicorn --bind 127.0.0.1:8000 app:app
```

### ملف Nginx:

```nginx
server {
    listen 80;
    server_name mystro.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/mystro /etc/nginx/sites-enabled/
```

```bash
sudo nginx -t
```

```bash
sudo systemctl reload nginx
```

---

## 🔒 9. تفعيل HTTPS باستخدام Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
```

```bash
sudo certbot --nginx -d mystro.yourdomain.com
```

---

## 🛡️ 10. إعداد جدار الحماية UFW

```bash
sudo ufw allow OpenSSH
```

```bash
sudo ufw allow 80,443,5000/tcp
```

```bash
sudo ufw enable
```

---

## 📬 تواصل

- GitHub: [@TamerOnLine](https://github.com/TamerOnLine)
- البريد الإلكتروني: info@denkengewinnen.com

---

> تم إنشاء هذا الدليل بناءً على محادثة تفصيلية بين المطور والمساعد الذكي – ويعكس إعدادًا فعليًا ناجحًا على سيرفر حقيقي.