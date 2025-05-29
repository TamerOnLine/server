
# 🛡️ إعداد مفاتيح SSH للوصول الآمن إلى السيرفر وGitHub

هذا الدليل يوضح كيفية إنشاء وضبط مفاتيح SSH لكل من:

1. 🔑 الدخول من الجهاز المحلي (Windows) إلى السيرفر (Ubuntu)
2. 🌐 السماح للسيرفر بالوصول إلى GitHub (clone/pull)

---

## 🧭 المفاتيح المستخدمة

| الجهة             | يستخدم للاتصال بـ     | اسم المفتاح         | مكان المفتاح الخاص            | المفتاح العام يذهب إلى              |
|------------------|------------------------|----------------------|-------------------------------|-------------------------------------|
| جهازك (Windows)  | السيرفر (`mystro`)     | `id_mystro_clean`    | `C:\Users\<User>\.ssh\`       | `/home/mystro/.ssh/authorized_keys` |
| السيرفر (mystro) | GitHub (repo access)   | `id_ed25519`         | `/home/mystro/.ssh/`          | حساب GitHub → Settings → SSH Keys  |

---

## 🧑‍💻 1. إعداد اتصال SSH من جهازك إلى السيرفر

### 🧱 الخطوات على **السيرفر** (كمستخدم root أو `tamer`):

```bash
# Create a new user named mystro
sudo adduser mystro

# Add mystro to the sudo group
sudo usermod -aG sudo mystro

# Create the .ssh directory for storing public keys
sudo mkdir -p /home/mystro/.ssh

# Set correct ownership and permissions
sudo chown mystro:mystro /home/mystro/.ssh

# Set strict permissions on the .ssh directory:
# 7 = full access (read/write/execute) for the owner (mystro)
# 0 = no access for group
# 0 = no access for others
sudo chmod 700 /home/mystro/.ssh
```

### 🖥️ على **جهازك المحلي (Windows)**:

```powershell
# Generate an SSH key pair named id_mystro_clean
ssh-keygen -t ed25519 -C "mystro-server-clean" -f $env:USERPROFILE\.
ssh\id_mystro_clean


# Copy the public key to clipboard
Get-Content $env:USERPROFILE\.ssh\id_mystro_clean.pub | Set-Clipboard
```

### 📥 الصق المفتاح العام داخل السيرفر:

```bash
sudo nano /home/mystro/.ssh/authorized_keys
# الصق المفتاح هنا واحفظ
sudo chmod 600 /home/mystro/.ssh/authorized_keys
sudo chown mystro:mystro /home/mystro/.ssh/authorized_keys
```

### ✅ جرّب الدخول:

```powershell
# "id_mystro_clean" is a dedicated SSH key used to access the server from your Windows machine
# It should be kept safe and never shared (private key)
ssh -i $env:USERPROFILE\.ssh\id_mystro_clean -p 13976 mystro@<IP_ADDRESS>
```

---

## 🔧 2. إعداد اتصال SSH من السيرفر إلى GitHub

### 🖥️ على **السيرفر** (كمستخدم `mystro`):

```bash
# Generate a deploy key to access GitHub
ssh-keygen -t ed25519 -C "github-deploy"
# The key will be located at: /home/mystro/.ssh/id_ed25519
```

### 🔑 انسخ المفتاح العام:

```bash
# Display the public key for copy-paste
cat ~/.ssh/id_ed25519.pub
```

### 🌐 أضف المفتاح في GitHub:

- ادخل إلى: `GitHub → Settings → SSH and GPG Keys`
- اضغط: **New SSH Key**
- العنوان مثلاً: `deploy key from liebe-server`
- الصق المفتاح، ثم احفظ

### ✅ اختبر الاتصال:

```bash
# Test SSH authentication with GitHub using the default SSH key
# -T: disables pseudo-terminal allocation (since we're not starting a shell)
# git@github.com: connect to GitHub's SSH interface as the 'git' user
# If successful, GitHub will greet you with your username
ssh -T git@github.com
# Should respond with: "Hi TamerOnLine! You've successfully authenticated..."
```

---

## 📂 3. نسخ المشروع من GitHub

```bash
# Navigate to the current user's home directory
cd ~

# Clone the private/public GitHub repository using SSH
# Make sure the server's SSH key is added to your GitHub account (as a deploy key)
# This will create a folder named 'mystro' with the repository's contents
git clone git@github.com:TamerOnLine/mystro.git
```

---

## 🗑️ حذف مستخدم بالكامل (اختياري)

```bash
# Remove the user and their home directory
sudo deluser --remove-home mystro
# Confirm deletion
ls /home  # تأكد من الحذف
```

---

## ✅ انتهى الإعداد بنجاح 🎉
