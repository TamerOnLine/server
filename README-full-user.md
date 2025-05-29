
# 🛡️ Complete Setup for User user with Flask, SSH, and GitHub

---

## 🧱 1. Create a New User on the Server

```bash
sudo adduser user
sudo usermod -aG sudo user
sudo mkdir -p /home/user/.ssh
sudo chown user:user /home/user/.ssh
sudo chmod 700 /home/user/.ssh
```

---

## 🔐 2. Generate SSH Key from Windows to Server

```powershell
ssh-keygen -t ed25519 -C "user-key-local to server" -f ${env:USERPROFILE}\.ssh\id_user
Get-Content ${env:USERPROFILE}\.ssh\id_user.pub | Set-Clipboard
```

### 📥 Paste the Key into the Server:

```bash
sudo nano /home/user/.ssh/authorized_keys
sudo chmod 600 /home/user/.ssh/authorized_keys
sudo chown user:user /home/user/.ssh/authorized_keys
```

### ✅ Test the Connection:

```powershell
ssh -i ${env:USERPROFILE}\.ssh\id_user -p 13976 user@78.47.205.8
```

---

## 🔗 3. Generate GitHub Key from Server

```bash
ssh-keygen -t ed25519 -C "user-key-local to server" -f ~/.ssh/id_github_user
cat ~/.ssh/id_github_user.pub
```

📌 Add the key to GitHub → Settings → SSH Keys.

```bash
ssh -T git@github.com
```

---

## 📦 4. Clone the Project from GitHub

```bash
cd ~
git clone git@github.com:TamerOnLine/user.git
cd user
```

---

## 🐍 5. Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💻 6. Run Flask Locally

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

---

## 🌀 7. Setup Gunicorn and Nginx

```bash
gunicorn --bind 127.0.0.1:8000 app:app
```

Configure Nginx File:

```nginx
server {
    listen 80;
    server_name user.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/user /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔒 8. Enable HTTPS

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d user.com --http-01-port 80
```

---

## 🛡️ 9. Enable UFW Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80,443,5000/tcp
sudo ufw enable
```

---

## ✅ Setup Completed Successfully 🎉
