
# إعداد مستخدم جديد بصلاحيات SSH على السيرفر

## 🧑‍💻 1. إنشاء المستخدم الجديد
```bash
sudo adduser mystro
# أدخل كلمة مرور ثم معلومات المستخدم (يمكن تخطيها بالضغط Enter)
```

## 👑 2. منحه صلاحيات sudo
```bash
sudo usermod -aG sudo mystro
```

## 🔐 3. إنشاء مجلد .ssh داخل مجلد المستخدم
```bash
sudo mkdir -p /home/mystro/.ssh
sudo chown mystro:mystro /home/mystro/.ssh
sudo chmod 700 /home/mystro/.ssh
```

## 🗝️ 4. إضافة المفتاح العام داخل authorized_keys
```bash
sudo nano /home/mystro/.ssh/authorized_keys
# الصق هنا المفتاح العام (public key) واحفظ
```

## 🔒 5. ضبط صلاحيات الملف والمجلد
```bash
sudo chmod 600 /home/mystro/.ssh/authorized_keys
sudo chown mystro:mystro /home/mystro/.ssh/authorized_keys
```

## ✅ 6. تجربة الدخول من الجهاز المحلي بدون كلمة مرور
```powershell
ssh -i "$env:USERPROFILE\.ssh\id_mystro_clean" -p 13976 mystro@78.47.205.8
```
