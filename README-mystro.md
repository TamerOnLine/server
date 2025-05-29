
# 🚀 مشروع mystro – إعداد متكامل خطوة بخطوة

هذا الدليل يشرح إعداد مشروع Flask على سيرفر حقيقي باستخدام مستخدم مستقل، SSH، GitHub، Gunicorn، وNginx مع شهادة SSL مجانًا.

---

## 🧱 1. إعداد مستخدم جديد على السيرفر

```bash
sudo deluser --remove-home mystro
```
⬅️ حذف المستخدم "mystro" إن وُجد سابقًا مع إزالة مجلد المنزل الخاص به بالكامل.

```bash
sudo adduser mystro
```
⬅️ إنشاء مستخدم جديد باسم "mystro".

```bash
sudo usermod -aG sudo mystro
```
⬅️ إعطاء المستخدم "mystro" صلاحيات sudo ليتمكن من تنفيذ أوامر إدارية.

```bash
sudo mkdir -p /home/mystro/.ssh
```
⬅️ إنشاء مجلد `.ssh` داخل مجلد المستخدم لتخزين مفاتيح SSH.

```bash
sudo touch /home/mystro/.ssh/authorized_keys
```
⬅️ إنشاء ملف `authorized_keys` لحفظ المفاتيح المسموح لها بالوصول.

```bash
sudo chmod 700 /home/mystro/.ssh
```
⬅️ إعطاء صلاحيات صحيحة للمجلد: فقط المستخدم يمكنه الدخول إليه.

```bash
sudo chmod 600 /home/mystro/.ssh/authorized_keys
```
⬅️ حماية ملف المفاتيح بحيث لا يمكن لأحد قراءته أو تعديله إلا المستخدم.

```bash
sudo chown -R mystro:mystro /home/mystro/.ssh
```
⬅️ جعل المستخدم "mystro" هو المالك الكامل لمجلد `.ssh` ومحتوياته.

---

## 🔐 2. توليد مفتاح SSH على جهازك المحلي

```bash
ssh-keygen -t ed25519 -C "mystro-server" -f %USERPROFILE%\.ssh\id_mystro
```
⬅️ توليد مفتاح SSH جديد من نوع ed25519 مع تسمية ملفه `id_mystro`.

---

## 📤 3. نسخ المفتاح إلى السيرفر

```bash
ssh-copy-id -i %USERPROFILE%\.ssh\id_mystro.pub -p 13976 mystro@your_server_ip
```
⬅️ نسخ المفتاح العام إلى ملف `authorized_keys` على السيرفر باستخدام المنفذ 13976.

أو بديل يدوي:

```bash
scp %USERPROFILE%\.ssh\id_mystro.pub mystro@your_server_ip:/home/mystro/.ssh/authorized_keys
```
⬅️ إرسال الملف يدويًا إلى السيرفر إن لم يعمل `ssh-copy-id`.

---

## 🔗 4. توليد مفتاح خاص لربط GitHub

```bash
ssh-keygen -t ed25519 -C "github-deploy"
```
⬅️ توليد مفتاح جديد مخصص لربط السيرفر بـ GitHub لاستخدامه في استنساخ المستودعات.

```bash
cat ~/.ssh/id_ed25519.pub
```
⬅️ عرض المفتاح العام لنسخه يدويًا ولصقه في GitHub تحت Deploy Keys.

---

## 📦 5. استنساخ المشروع من GitHub

```bash
git clone git@github.com:TamerOnLine/mystro.git
```
⬅️ استنساخ المشروع من GitHub باستخدام المفتاح المخصص.

```bash
cd mystro
```
⬅️ الدخول إلى مجلد المشروع.

---

## 🐍 6. إعداد بيئة Python افتراضية

```bash
python3 -m venv venv
```
⬅️ إنشاء بيئة افتراضية لتثبيت الحزم بداخلها بدون التأثير على النظام.

```bash
source venv/bin/activate
```
⬅️ تفعيل البيئة الافتراضية.

```bash
pip install --upgrade pip
```
⬅️ تحديث أداة pip لأحدث إصدار.

```bash
pip install -r requirements.txt
```
⬅️ تثبيت جميع الحزم المطلوبة الموجودة في ملف `requirements.txt`.

---

## 💻 7. تشغيل المشروع محليًا (Flask)

```bash
export FLASK_APP=app.py
```
⬅️ تعريف اسم الملف الرئيسي لتطبيق Flask.

```bash
export FLASK_ENV=development
```
⬅️ تفعيل وضع التطوير لتسهيل التتبع أثناء التجربة.

```bash
flask run --host=0.0.0.0 --port=5000
```
⬅️ تشغيل التطبيق على كل عناوين IP، على المنفذ 5000.

---

## 🌐 8. تشغيل المشروع باستخدام Gunicorn وNginx

```bash
gunicorn --bind 127.0.0.1:8000 app:app
```
⬅️ تشغيل Flask عبر Gunicorn على المنفذ 8000 محليًا، وجاهز لاستقباله من Nginx.

### ملف إعداد Nginx

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
⬅️ إعداد Nginx ليعكس الطلبات من النطاق إلى التطبيق عبر Gunicorn.

```bash
sudo ln -s /etc/nginx/sites-available/mystro /etc/nginx/sites-enabled/
```
⬅️ تفعيل إعداد Nginx الخاص بالمشروع.

```bash
sudo nginx -t
```
⬅️ اختبار إعدادات Nginx قبل إعادة تشغيله.

```bash
sudo systemctl reload nginx
```
⬅️ إعادة تحميل إعدادات Nginx بدون إعادة التشغيل الكامل.

---

## 🔒 9. تفعيل HTTPS باستخدام Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
```
⬅️ تثبيت أدوات `certbot` المطلوبة لإنشاء شهادة SSL مجانية.

```bash
sudo certbot --nginx -d mystro.yourdomain.com
```
⬅️ توليد شهادة SSL وربطها تلقائيًا بـ Nginx للمجال الفرعي `mystro.yourdomain.com`.

---

## 🛡️ 10. إعداد جدار الحماية UFW

```bash
sudo ufw allow OpenSSH
```
⬅️ السماح باتصالات SSH حتى لا تفقد الوصول للسيرفر.

```bash
sudo ufw allow 80,443,5000/tcp
```
⬅️ السماح بحركة المرور عبر HTTP (80)، HTTPS (443)، و Flask (5000).

```bash
sudo ufw enable
```
⬅️ تفعيل الجدار الناري (Firewall).

---

## 📬 تواصل

- GitHub: [@TamerOnLine](https://github.com/TamerOnLine)
- البريد الإلكتروني: info@denkengewinnen.com
