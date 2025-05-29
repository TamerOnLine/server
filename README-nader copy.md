
# Project nader – Step-by-Step Setup

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

## 2. Copy SSH Key to the Server

```bash
ssh-copy-id -i ~/.ssh/id_nader.pub -p 13976 nader@78.47.205.8
# Alternatively
scp ~/.ssh/id_nader.pub nader@78.47.205.8:/home/nader/.ssh/authorized_keys
```

## 3. Configure Nginx

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

## 4. SSL Certificate

```bash
sudo certbot --nginx -d mystrotamer.com
```
