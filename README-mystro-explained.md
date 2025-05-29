
# 🚀 مشروع mystro – إعداد متكامل خطوة بخطوة

هذا الدليل يشرح إعداد مشروع Flask على سيرفر حقيقي باستخدام مستخدم مستقل، SSH، GitHub، Gunicorn، وNginx مع شهادة SSL مجانًا.

---

## 🧱 1. إعداد مستخدم جديد على السيرفر

⬅️ حذف المستخدم "mystro" إن وُجد سابقًا مع إزالة مجلد المنزل الخاص به بالكامل.
```bash
sudo deluser --remove-home mystro
```

⬅️ إنشاء مستخدم جديد باسم "mystro".
```bash
sudo adduser mystro
```

⬅️ إعطاء المستخدم "mystro" صلاحيات sudo ليتمكن من تنفيذ أوامر إدارية.
```bash
sudo usermod -aG sudo mystro
```

⬅️ إنشاء مجلد `.ssh` داخل مجلد المستخدم لتخزين مفاتيح SSH.
```bash
sudo mkdir -p /home/mystro/.ssh
```

⬅️ إنشاء ملف `authorized_keys` لحفظ المفاتيح المسموح لها بالوصول.
```bash
sudo touch /home/mystro/.ssh/authorized_keys
```

⬅️ إعطاء صلاحيات صحيحة للمجلد: فقط المستخدم يمكنه الدخول إليه.
```bash
sudo chmod 700 /home/mystro/.ssh
```

⬅️ حماية ملف المفاتيح بحيث لا يمكن لأحد قراءته أو تعديله إلا المستخدم.
```bash
sudo chmod 600 /home/mystro/.ssh/authorized_keys
```

⬅️ جعل المستخدم "mystro" هو المالك الكامل لمجلد `.ssh` ومحتوياته.
```bash
sudo chown -R mystro:mystro /home/mystro/.ssh
```

---

## 🔐 2. توليد مفتاح SSH على جهازك المحلي

⬅️ توليد مفتاح SSH جديد من نوع ed25519 مع تسمية ملفه `id_mystro`.
```bash
ssh-keygen -t ed25519 -C "mystro-server" -f %USERPROFILE%\.ssh\id_mystro
```

---

## 📤 3. نسخ المفتاح إلى السيرفر

⬅️ نسخ المفتاح العام إلى ملف `authorized_keys` على السيرفر باستخدام المنفذ 13976.
```bash
ssh-copy-id -i %USERPROFILE%\.ssh\id_mystro.pub -p 13976 mystro@your_server_ip
```

⬅️ إرسال الملف يدويًا إلى السيرفر إن لم يعمل `ssh-copy-id`.
```bash
scp %USERPROFILE%\.ssh\id_mystro.pub mystro@your_server_ip:/home/mystro/.ssh/authorized_keys
```

---

## 🔗 4. توليد مفتاح خاص لربط GitHub

⬅️ توليد مفتاح جديد مخصص لربط السيرفر بـ GitHub لاستخدامه في استنساخ المستودعات.
```bash
ssh-keygen -t ed25519 -C "github-deploy"
```

⬅️ عرض المفتاح العام لنسخه يدويًا ولصقه في GitHub تحت Deploy Keys.
```bash
cat ~/.ssh/id_ed25519.pub
```

---

## 📦 5. استنساخ المشروع من GitHub

⬅️ استنساخ المشروع من GitHub باستخدام المفتاح المخصص.
```bash
git clone git@github.com:TamerOnLine/mystro.git
```

⬅️ الدخول إلى مجلد المشروع.
```bash
cd mystro
```

---

## 🐍 6. إعداد بيئة Python افتراضية

⬅️ إنشاء بيئة افتراضية لتثبيت الحزم بداخلها بدون التأثير على النظام.
```bash
python3 -m venv venv
```

⬅️ تفعيل البيئة الافتراضية.
```bash
source venv/bin/activate
```

⬅️ تحديث أداة pip لأحدث إصدار.
```bash
pip install --upgrade pip
```

⬅️ تثبيت جميع الحزم المطلوبة الموجودة في ملف `requirements.txt`.
```bash
pip install -r requirements.txt
```

---

## 💻 7. تشغيل المشروع محليًا (Flask)

⬅️ تعريف اسم الملف الرئيسي لتطبيق Flask.
```bash
export FLASK_APP=app.py
```

⬅️ تفعيل وضع التطوير لتسهيل التتبع أثناء التجربة.
```bash
export FLASK_ENV=development
```

⬅️ تشغيل التطبيق على كل عناوين IP، على المنفذ 5000.
```bash
flask run --host=0.0.0.0 --port=5000
```

---

## 🌐 8. تشغيل المشروع باستخدام Gunicorn وNginx

⬅️ تشغيل Flask عبر Gunicorn على المنفذ 8000 محليًا، وجاهز لاستقباله من Nginx.
```bash
gunicorn --bind 127.0.0.1:8000 app:app
```

### ملف إعداد Nginx

⬅️ إعداد Nginx ليعكس الطلبات من النطاق إلى التطبيق عبر Gunicorn.
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

⬅️ تفعيل إعداد Nginx الخاص بالمشروع.
```bash
sudo ln -s /etc/nginx/sites-available/mystro /etc/nginx/sites-enabled/
```

⬅️ اختبار إعدادات Nginx قبل إعادة تشغيله.
```bash
sudo nginx -t
```

⬅️ إعادة تحميل إعدادات Nginx بدون إعادة التشغيل الكامل.
```bash
sudo systemctl reload nginx
```

---

## 🔒 9. تفعيل HTTPS باستخدام Let's Encrypt

⬅️ تثبيت أدوات `certbot` المطلوبة لإنشاء شهادة SSL مجانية.
```bash
sudo apt install certbot python3-certbot-nginx -y
```

⬅️ توليد شهادة SSL وربطها تلقائيًا بـ Nginx للمجال الفرعي `mystro.yourdomain.com`.
```bash
sudo certbot --nginx -d mystro.yourdomain.com
```

---

## 🛡️ 10. إعداد جدار الحماية UFW

⬅️ السماح باتصالات SSH حتى لا تفقد الوصول للسيرفر.
```bash
sudo ufw allow OpenSSH
```

⬅️ السماح بحركة المرور عبر HTTP (80)، HTTPS (443)، و Flask (5000).
```bash
sudo ufw allow 80,443,5000/tcp
```

⬅️ تفعيل الجدار الناري (Firewall).
```bash
sudo ufw enable
```

---

## 📬 تواصل

- GitHub: [@TamerOnLine](https://github.com/TamerOnLine)
- البريد الإلكتروني: info@denkengewinnen.com
