# 🔐 إنشاء مفتاح SSH على الجهاز المحلي (Windows/Linux)

## ✅ الهدف
إنشاء زوج مفاتيح SSH (خاص + عام) في المسار الافتراضي على الجهاز، لاستخدامه لاحقًا في الاتصال بخوادم عن بُعد بدون كلمة مرور.

---

## 🧰 الخطوات

### 1. فتح الطرفية (Terminal)
- على **Windows**: افتح PowerShell أو Git Bash.
- على **Linux**: افتح Terminal.

---

### 2. إنشاء مفتاح جديد بالمسار الافتراضي

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

#### شرح الأوامر:
- `-t ed25519` : نوع المفتاح (موصى به).
- `-C "..."` : تعليق للمفتاح (عادة البريد الإلكتروني أو وصف واضح).

---

### 3. عند ظهور الرسالة التالية:

```
Enter file in which to save the key (/home/USERNAME/.ssh/id_ed25519):
```

اضغط **Enter** بدون كتابة أي شيء، ليتم الحفظ في المسار الافتراضي:

- على **Linux**: `~/.ssh/id_ed25519`
- على **Windows**: `C:\Users\USERNAME\.ssh\id_ed25519`

---

### 4. عند السؤال عن كلمة مرور للمفتاح (passphrase):

- يمكنك الضغط على **Enter** لتركها فارغة (بدون كلمة مرور).
- أو إدخال كلمة مرور لحماية المفتاح الخاص.

---

### 5. عرض المفتاح العام (لنسخه لاحقًا إلى السيرفر):

```bash
cat ~/.ssh/id_ed25519.pub
```

- على Windows PowerShell:

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub
```

---

### 6. نسخ المفتاح إلى الحافظة:

- على **Linux**:

```bash
xclip -sel clip < ~/.ssh/id_ed25519.pub
```

- على **Windows PowerShell**:

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard
```

---

## ✅ جاهز الآن لإضافته إلى السيرفر أو GitHub أو أي منصة دعم SSH.