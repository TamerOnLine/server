import textwrap

def main():
    """
    Collects setup information from the user and generates a markdown configuration guide
    for a new user with Flask, SSH, and GitHub setup instructions.
    
    Prompts the user for various configuration inputs, generates a README markdown file
    based on the inputs, and saves it to the disk.
    """
    user = input("Enter new username (e.g., mystro): ").strip()
    server_ip = input("Enter server IP address: ").strip()

    ssh_port = input("Enter SSH port (default: 13976): ").strip() or "13976"
    domain = input(f"Enter full domain name (default: {user}.com): ").strip() or f"{user}.com"
    key_clean = input(f"Enter Windows-to-server SSH key name (default: id_{user}): ").strip() or f"id_{user}"
    key_github = input(f"Enter GitHub key name on server (default: id_github_{user}): ").strip() or f"id_github_{user}"
    repo_name = input(f"Enter GitHub repository name (default: {user}): ").strip() or user

    flask_port = input("Enter Flask port (e.g., 5000): ").strip()
    gunicorn_port = input("Enter Gunicorn port (e.g., 8000): ").strip()
    http_port = input("Enter HTTP port (default: 80): ").strip() or "80"
    https_port = input("Enter HTTPS port (default: 443): ").strip() or "443"

    filename = f"README-full-{user}.md"

    content = textwrap.dedent(f"""
        # Complete Setup for User {user} with Flask, SSH, and GitHub

        ## 1. Create a New User on the Server

        ```bash
        sudo adduser {user}
        sudo usermod -aG sudo {user}
        sudo mkdir -p /home/{user}/.ssh
        sudo chown {user}:{user} /home/{user}/.ssh
        sudo chmod 700 /home/{user}/.ssh
        ```

        ## 2. Generate SSH Key from Windows to Server

        ```powershell
        ssh-keygen -t ed25519 -C "{user}-server" -f ${{env:USERPROFILE}}\\.ssh\\{key_clean}
        Get-Content ${{env:USERPROFILE}}\\.ssh\\{key_clean}.pub | Set-Clipboard
        ```

        Paste the key into the server:

        ```bash
        sudo nano /home/{user}/.ssh/authorized_keys
        sudo chmod 600 /home/{user}/.ssh/authorized_keys
        sudo chown {user}:{user} /home/{user}/.ssh/authorized_keys
        ```

        Test the connection:

        ```powershell
        ssh -i ${{env:USERPROFILE}}\\.ssh\\{key_clean} -p {ssh_port} {user}@{server_ip}
        ```

        ## 3. Generate GitHub Key from Server

        ```bash
        ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/{key_github}
        cat ~/.ssh/{key_github}.pub
        ```

        Add this key to GitHub under Settings → SSH Keys.

        ```bash
        ssh -T git@github.com
        ```

        ## 4. Clone the Project from GitHub

        ```bash
        cd ~
        git clone git@github.com:TamerOnLine/{repo_name}.git
        cd {repo_name}
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
        flask run --host=0.0.0.0 --port={flask_port}
        ```

        ## 7. Setup Gunicorn and Nginx

        ```bash
        gunicorn --bind 127.0.0.1:{gunicorn_port} app:app
        ```

        Nginx configuration:

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

        ## 8. Enable HTTPS

        ```bash
        sudo apt install certbot python3-certbot-nginx -y
        sudo certbot --nginx -d {domain} --http-01-port {http_port}
        ```

        ## 9. Enable UFW Firewall

        ```bash
        sudo ufw allow OpenSSH
        sudo ufw allow {http_port},{https_port},{flask_port}/tcp
        sudo ufw enable
        ```

        ## Setup Complete
    """)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nFile successfully created: {filename}")


if __name__ == "__main__":
    main()
