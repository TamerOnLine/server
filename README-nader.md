
# Project nader – Step-by-Step Setup Guide

This guide explains how to set up a Flask project on a real server using a dedicated user, SSH, GitHub, Gunicorn, and Nginx with a free SSL certificate.

---

## 1. Create a New User on the Server

```bash
sudo adduser nader
sudo usermod -aG sudo nader
sudo mkdir -p /home/nader/.ssh
sudo touch /home/nader/.ssh/authorized_keys
sudo chmod 700 /home/nader/.ssh
sudo chmod 600 /home/nader/.ssh/authorized_keys
sudo chown -R nader:nader /home/nader/.ssh
```

---

## 2. Generate SSH Key on Your Local Machine

```bash
ssh-keygen -t ed25519 -C "nader-server" -f ~/.ssh/id_nader
```

---

## 3. Copy the Key to the Server

```bash
ssh-copy-id -i ~/.ssh/id_nader.pub -p 13976 nader@78.47.205.8
```

Or manually:

```bash
scp ~/.ssh/id_nader.pub nader@78.47.205.8:/home/nader/.ssh/authorized_keys
```

---

## 4. Generate Deployment Key for GitHub

```bash
ssh-keygen -t ed25519 -C "github-deploy"
cat ~/.ssh/id_ed25519.pub
```

---

## 5. Clone the Project from GitHub

```bash
git clone git@github.com:TamerOnLine/mystro.git
cd mystro
```

---

## 6. Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 7. Run the Project Locally (Flask)

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=6565
```

---

## 8. Configure Gunicorn and Nginx

```bash
gunicorn --bind 127.0.0.1:6565 app:app
```

### Nginx Configuration File:

```nginx
server {
    listen 80;
    server_name mystrotamer.com;

    location / {
        proxy_pass http://127.0.0.1:6565;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/nader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 9. Enable HTTPS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d mystrotamer.com --http-01-port 80
```

---

## 10. Set Up UFW Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80,443,6565/tcp
sudo ufw enable
```

---

## Contact

- GitHub: [@TamerOnLine](https://github.com/TamerOnLine)
- Email: info@denkengewinnen.com
