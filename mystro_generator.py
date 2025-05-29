import textwrap

def main():
    """
    Prompts the user for server and application configuration values,
    then generates a README file with setup instructions for a Flask project.

    The instructions include user creation, SSH key generation,
    GitHub repository cloning, virtual environment setup,
    Flask and Gunicorn setup, and enabling HTTPS with Let's Encrypt.
    """
    user = input("Enter the new username (e.g., mystro): ")
    server_ip = input("Enter the server IP address: ")
    ssh_port = input("Enter the SSH port (e.g., 13976): ")
    domain = input("Enter the full domain name (e.g., mystro.yourdomain.com): ")
    flask_port = input("Enter the Flask port (e.g., 5000): ")
    gunicorn_port = input("Enter the internal Gunicorn port (e.g., 8000): ")
    http_port = input("Enter the HTTP port (e.g., 80): ")
    https_port = input("Enter the HTTPS port (e.g., 443): ")

    filename = f"README-{user}.md"

    content = textwrap.dedent(f"""
        # Project {user} – Step-by-Step Setup Guide

        This guide explains how to set up a Flask project on a real server using a dedicated user, SSH, GitHub, Gunicorn, and Nginx with a free SSL certificate.

        ---

        ## 1. Create a New User on the Server

        ```bash
        sudo adduser {user}
        sudo usermod -aG sudo {user}
        sudo mkdir -p /home/{user}/.ssh
        sudo touch /home/{user}/.ssh/authorized_keys
        sudo chmod 700 /home/{user}/.ssh
        sudo chmod 600 /home/{user}/.ssh/authorized_keys
        sudo chown -R {user}:{user} /home/{user}/.ssh
        ```

        ---

        ## 2. Generate SSH Key on Your Local Machine

        ```bash
        ssh-keygen -t ed25519 -C "{user}-server" -f ~/.ssh/id_{user}
        ```

        ---

        ## 3. Copy the Key to the Server

        ```bash
        ssh-copy-id -i ~/.ssh/id_{user}.pub -p {ssh_port} {user}@{server_ip}
        ```

        Or manually:

        ```bash
        scp ~/.ssh/id_{user}.pub {user}@{server_ip}:/home/{user}/.ssh/authorized_keys
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
        flask run --host=0.0.0.0 --port={flask_port}
        ```

        ---

        ## 8. Configure Gunicorn and Nginx

        ```bash
        gunicorn --bind 127.0.0.1:{gunicorn_port} app:app
        ```

        ### Nginx Configuration File:

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

        ## 9. Enable HTTPS with Let's Encrypt

        ```bash
        sudo apt install certbot python3-certbot-nginx -y
        sudo certbot --nginx -d {domain} --http-01-port {http_port}
        ```

        ---

        ## 10. Set Up UFW Firewall

        ```bash
        sudo ufw allow OpenSSH
        sudo ufw allow {http_port},{https_port},{flask_port}/tcp
        sudo ufw enable
        ```

        ---

        ## Contact

        - GitHub: [@TamerOnLine](https://github.com/TamerOnLine)
        - Email: info@denkengewinnen.com
    """)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nThe file has been successfully created: {filename}")


if __name__ == "__main__":
    main()
