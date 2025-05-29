from textwrap import dedent

def generate_readme(user, server_ip, ssh_port, domain, key_clean,
                    key_github, repo_name, flask_port, gunicorn_port,
                    http_port, https_port):
    """
    Generates a formatted README file for setting up a Flask application with
    SSH, GitHub, and server configurations.

    Args:
        user (str): Username for the server.
        server_ip (str): IP address of the server.
        ssh_port (int): SSH port number.
        domain (str): Domain name for the server.
        key_clean (str): Clean SSH key filename for local to server.
        key_github (str): SSH key filename for GitHub.
        repo_name (str): Name of the GitHub repository.
        flask_port (int): Port for running the Flask app.
        gunicorn_port (int): Port for Gunicorn server.
        http_port (int): HTTP port number.
        https_port (int): HTTPS port number.

    Returns:
        str: The content of the generated README.
    """
    filename = f"README-full-{user}.md"

    content = dedent(f"""
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
    gunicorn --bind 127.0.0.1:{gunicorn_port} app:app
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
    """)

    return content

def main():
    user = input("Enter username: ").strip() or "user"
    server_ip = input("Enter server IP: ").strip()
    
    ssh_port = int(input("Enter SSH port [13976]: ").strip() or "13976")
    domain = input(f"Enter domain name [{user}.com]: ").strip() or f"{user}.com"
    key_clean = input(f"Enter SSH key name (clean) [id_{user}]: ").strip() or f"id_{user}"
    key_github = input(f"Enter GitHub SSH key name [id_github_{user}]: ").strip() or f"id_github_{user}"
    repo_name = input(f"Enter GitHub repository name [{user}]: ").strip() or user

    flask_port = int(input("Enter Flask port [5000]: ").strip() or "5000")
    gunicorn_port = int(input("Enter Gunicorn port [8000]: ").strip() or "8000")
    http_port = int(input("Enter HTTP port [80]: ").strip() or "80")
    https_port = int(input("Enter HTTPS port [443]: ").strip() or "443")

    readme_content = generate_readme(
        user, server_ip, ssh_port, domain, key_clean, key_github,
        repo_name, flask_port, gunicorn_port, http_port, https_port
    )

    filename = f"README-full-{user}.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(readme_content)
    print(f"✅ README saved as {filename}")


if __name__ == "__main__":
    main()
