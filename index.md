# 🛡️ Complete Setup for User {user} with Flask, SSH, and GitHub

    ---

    ## 🧱 1. Create a New User on the Server

    ```bash
    sudo adduser {user}
    sudo usermod -aG sudo {user}
    sudo mkdir -p /home/{user}/.ssh
    sudo chown {user}:{user} /home/{user}/.ssh
    sudo chmod 700 /home/{user}/.ssh
    ```

    ---

    ## 🔐 2. Generate SSH Key from Windows to Server

    ```powershell
    ssh-keygen -t ed25519 -C "{user}-key-local to server" -f ${{env:USERPROFILE}}\\.ssh\\{key_clean}
    Get-Content ${{env:USERPROFILE}}\\.ssh\\{key_clean}.pub | Set-Clipboard
    ```

    ### 📥 Paste the Key into the Server:

    ```bash
    sudo nano /home/{user}/.ssh/authorized_keys
    sudo chmod 600 /home/{user}/.ssh/authorized_keys
    sudo chown {user}:{user} /home/{user}/.ssh/authorized_keys
    ```

    ### ✅ Test the Connection:

    ```powershell
    ssh -i ${{env:USERPROFILE}}\\.ssh\\{key_clean} -p {ssh_port} {user}@{server_ip}
    ```

    ---

    ## 🔗 3. Generate GitHub Key from Server

    ```bash
    ssh-keygen -t ed25519 -C "{user}-key-local to server" -f ~/.ssh/{key_github}
    cat ~/.ssh/{key_github}.pub
    ```

    📌 Add the key to GitHub → Settings → SSH Keys.

    ```bash
    ssh -T git@github.com
    ```

    ---

    ## 📦 4. Clone the Project from GitHub

    ```bash
    cd ~
    git clone git@github.com:TamerOnLine/{repo_name}.git
    cd {repo_name}
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
    flask run --host=0.0.0.0 --port={flask_port}
    ```

    ---

    ## 🌀 7. Setup Gunicorn and Nginx

    ```bash
    gunicorn --bind 127.0.0.1:{gunicorn_port} myapp:app
    ```

    Configure Nginx File:

    ```nginx
    server {{
        listen {http_port};
        server_name {domain};

        location / {{
            proxy_pass http://127.0.0.1:{gunicorn_port};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }}
    }}
    ```

    ```bash
    sudo ln -s /etc/nginx/sites-available/{user} /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    ```

    ---

    ## 🔒 8. Enable HTTPS

    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d {domain} --http-01-port {http_port}
    ```

    ---

    ## 🛡️ 9. Enable UFW Firewall

    ```bash
    sudo ufw allow OpenSSH
    sudo ufw allow {http_port},{https_port},{flask_port}/tcp
    sudo ufw enable
    ```

    ---

    ## ✅ Setup Completed Successfully 🎉