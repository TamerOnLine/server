# 🚀 إضافة مفتاح SSH إلى GitHub

## الخطوة 1️⃣ - إنشاء مفتاح SSH (إذا لم يكن لديك)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- اضغط ENTER لاستخدام المسار الافتراضي `~/.ssh/id_ed25519`
- يمكنك ترك كلمة المرور فارغة أو إدخال كلمة مرور للحماية

## الخطوة 2️⃣ - نسخ المفتاح العام

```bash
cat ~/.ssh/id_ed25519.pub
```

- انسخ الناتج بالكامل، يبدأ بـ `ssh-ed25519 ...`

أو إذا كنت على Windows:

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard
```

## الخطوة 3️⃣ - إضافة المفتاح إلى GitHub

1. توجه إلى: [https://github.com/settings/keys](https://github.com/settings/keys)
2. اضغط على "New SSH key"
3. في خانة `Title` ضع اسم تعريفي مثل: `laptop-2025`
4. في خانة `Key` الصق المفتاح العام
5. اضغط على "Add SSH key"

## الخطوة 4️⃣ - التحقق من الاتصال

```bash
ssh -T git@github.com
```

- أول مرة سيطلب منك تأكيد الاتصال بـ GitHub.
- إذا نجح الاتصال، سترى رسالة مثل:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

📌 تأكد أن وكيل SSH (ssh-agent) يعمل ويحمّل المفتاح.

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

🎉 تم الآن ربط المفتاح بجهازك ويمكنك استخدام Git بشكل آمن عبر SSH.