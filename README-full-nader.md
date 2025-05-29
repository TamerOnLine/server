
# Complete Setup for User nader with Flask, SSH, and GitHub

## 1. Create a New User on the Server

```bash
sudo adduser nader
sudo usermod -aG sudo nader
sudo mkdir -p /home/nader/.ssh
sudo chown nader:nader /home/nader/.ssh
sudo chmod 700 /home/nader/.ssh
```

## 2. Generate SSH Key from Windows to Server

```powershell
ssh-keygen -t ed25519 -C "nader-server" -f ${env:USERPROFILE}\.ssh\id_nader
Get-Content ${env:USERPROFILE}\.ssh\id_nader.pub | Set-Clipboard
```

Paste the key into the server:

```bash
sudo nano /home/nader/.ssh/authorized_keys
sudo chmod 600 /home/nader/.ssh/authorized_keys
sudo chown nader:nader /home/nader/.ssh/authorized_keys
```

Test the connection:

```powershell
ssh -i ${env:USERPROFILE}\.ssh\id_nader -p 1976 nader@78.47.205.8
```

## 3. Generate GitHub Key from Server

```bash
ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/id_github_nader
cat ~/.ssh/id_github_nader.pub
```

Add this key to GitHub under Settings → SSH Keys.

```bash
ssh -T git@github.com
```

## 4. Clone the Project from GitHub

```bash
cd ~
git clone git@github.com:TamerOnLine/nader.git
cd nader
```

## 5. Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Run Flask Locally

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=
```

## 7. Setup Gunicorn and Nginx

```bash
gunicorn --bind 127.0.0.1: app:app
```

Nginx configuration:

```nginx
server {
    listen 80;
    server_name nader.com;

    location / {
        proxy_pass http://127.0.0.1:;
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

## 8. Enable HTTPS

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d nader.com --http-01-port 80
```

## 9. Enable UFW Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80,443,/tcp
sudo ufw enable
```

## Setup Complete
