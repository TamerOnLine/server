
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
# Create a new user account named 'mystro'
# This command will also create the home directory: /home/mystro
# You will be prompted to enter a password and some optional user info
sudo adduser mystro


# Add the user 'mystro' to the 'sudo' group
# This grants 'mystro' administrative privileges (ability to use 'sudo' command)
# -aG means: append (a) the user to the supplementary group(s) (G) without removing existing ones
sudo usermod -aG sudo mystro


# Create the .ssh directory inside the user's home directory
# -p ensures that the full path is created without errors if intermediate directories don't exist
# This directory will store authorized_keys and other SSH configuration files
sudo mkdir -p /home/mystro/.ssh


# Change the ownership of the .ssh directory to user 'mystro' and group 'mystro'
# This is required because the directory was created using 'sudo', so it's owned by root by default
# SSH will reject access if the directory is not owned by the correct user
sudo chown mystro:mystro /home/mystro/.ssh


# Set strict permissions on the .ssh directory:
# 7 = full access (read/write/execute) for the owner (mystro)
# 0 = no access for group
# 0 = no access for others
sudo chmod 700 /home/mystro/.ssh
```

### 🖥️ على **جهازك المحلي (Windows)**:

```powershell
# Generate a new SSH key pair using the ed25519 algorithm
# -t ed25519         → Specifies the key type (modern, secure, and fast)
# -C "mystro-server-clean" → Adds a label/comment to help identify the key later
# -f ${env:USERPROFILE}\.ssh\id_mystro_clean → Sets the file name and path to save the key pair
ssh-keygen -t ed25519 -C "mystro-server" -f ${env:USERPROFILE}\.ssh\id_mystro_clean


# Read the contents of your public SSH key (id_mystro_clean.pub)
# and copy it directly to the Windows clipboard
# This makes it easy to paste into the server's authorized_keys file
Get-Content ${env:USERPROFILE}\.ssh\id_mystro_clean.pub | Set-Clipboard

```

### 📥 الصق المفتاح العام داخل السيرفر:

```bash
# Open (or create) the 'authorized_keys' file for editing
# This file stores public keys that are allowed to SSH into the 'mystro' user account
# Paste the public key here (e.g., id_mystro_clean.pub) and save the file
sudo nano /home/mystro/.ssh/authorized_keys

# Set strict permissions for the 'authorized_keys' file:
# 6 = read/write for the owner (mystro)
# 0 = no permissions for group
# 0 = no permissions for others
# This ensures only the 'mystro' user can read or modify the file (security best practice)
sudo chmod 600 /home/mystro/.ssh/authorized_keys

# Set the owner and group of the 'authorized_keys' file to 'mystro'
# This ensures the file is owned by the user who will use it for SSH login
# Syntax: chown <user>:<group> <file>
sudo chown mystro:mystro /home/mystro/.ssh/authorized_keys
```

### ✅ جرّب الدخول:

```powershell
# "id_mystro_clean" is a dedicated SSH key used to access the server from your Windows machine
# It should be kept safe and never shared (private key)
ssh -i ${env:USERPROFILE}\.ssh\id_mystro_clean -p 13976 mystro@<IP_ADDRESS>
```

---

## 🔧 2. إعداد اتصال SSH من السيرفر إلى GitHub

### 🖥️ على **السيرفر** (كمستخدم `mystro`):

```bash
# Generate a new SSH key pair using the ed25519 algorithm for GitHub deployment
# -t ed25519        → Use the secure and modern ed25519 algorithm
# -C "github-deploy" → Add a comment to identify the key (visible in GitHub)
# -f ${HOME}/.ssh/github_key_mystro → Set a custom filename for the key pair
# This creates two files:
#   ${HOME}/.ssh/github_key_mystro      → private key (keep it secret)
#   ${HOME}/.ssh/github_key_mystro.pub  → public key (add it to GitHub)
ssh-keygen -t ed25519 -C "github-deploy" -f ${HOME}/.ssh/github_key_mystro
# The key will be located at: /home/mystro/.ssh/id_ed25519
```

### 🔑 انسخ المفتاح العام:

```bash
# Display the contents of your public SSH key (id_ed25519.pub)
# This is the key you will copy and paste into GitHub (or any other SSH host)
# Safe to share publicly — it's used for authentication, not encryption
cat ${HOME}/.ssh/id_ed25519.pub

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
# Change the current directory to the user's home directory
# '~' is a shortcut that represents the home directory of the current user
# Example: for user 'mystro', this means /home/mystro
cd ~


# Clone the private/public GitHub repository using SSH
# Make sure the server's SSH key is added to your GitHub account (as a deploy key)
# This will create a folder named 'mystro' with the repository's contents
git clone git@github.com:TamerOnLine/mystro.git
```

---

## 🗑️ حذف مستخدم بالكامل (اختياري)

```bash
# Completely delete the user 'mystro' and remove their home directory
# --remove-home ensures that /home/mystro and all its contents (including .ssh, files, configs) are deleted
# ⚠️ Warning: This is irreversible – make sure you no longer need the user or their data
sudo deluser --remove-home mystro

# List the contents of the /home directory
# This shows all user home directories on the system (e.g., mystro, tamer, ubuntu)
# Useful for verifying whether a user’s home directory still exists after deletion
ls /home

```

---

## ✅ انتهى الإعداد بنجاح 🎉
