# 🚀 رفع ملفات المشروع من GitHub إلى السيرفر

## ✅ المتطلبات
- تم إعداد مستخدم على السيرفر بصلاحيات SSH (مثل `mystro`)
- تم إعداد مفتاح SSH الخاص وربطه بـ GitHub (كـ Deploy Key أو GitHub Actions)
- الاتصال متاح للسيرفر عبر منفذ مثل `13976`

---

## 🛠️ 1. الدخول إلى السيرفر
```bash
ssh -i ~/.ssh/id_mystro_clean -p 13976 mystro@78.47.205.8
```

## 📁 2. إنشاء مجلد للمشروع
```bash
mkdir -p ~/mystro
cd ~/mystro
```

## 🔧 3. تهيئة Git (مرة واحدة فقط)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 🔑 4. إضافة المفتاح الخاص إذا لم يكن موجود
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/id_ed25519  # الصق هنا المفتاح الخاص
chmod 600 ~/.ssh/id_ed25519
```

### ➕ (اختياري) إضافة إعداد GitHub للملف config
```bash
nano ~/.ssh/config
```

أضف الأسطر التالية:
```
Host github.com
  IdentityFile ~/.ssh/id_ed25519
  User git
```

---

## 🌐 5. استنساخ المشروع من GitHub
```bash
cd ~/mystro
git clone git@github.com:YourUsername/your-repo.git .
```

## 🔁 6. لتحديث المشروع لاحقًا
```bash
cd ~/mystro
git pull origin main
```

---

## 🧹 7. لحذف المستخدم ومجلده (اختياري)
```bash
sudo deluser --remove-home mystro
ls /home
```