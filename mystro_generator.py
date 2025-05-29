import textwrap

def main():
    """
    Creates a README file with setup instructions for a new server user.

    Prompts the user for required information including username, server IP,
    SSH port, domain name, and internal app port. Uses this data to generate
    a markdown file with step-by-step setup instructions.

    Returns:
        None
    """
    user = input("Enter the new username (e.g., mystro): ")
    server_ip = input("Enter the server IP address: ")
    port = input("Enter the SSH port (e.g., 13976): ")
    domain = input("Enter the full domain name (e.g., mystro.yourdomain.com): ")
    app_port = input("Enter the internal application port (e.g., 8000): ")

    filename = f"README-{user}.md"

    content = textwrap.dedent(f"""
        # Project {user} – Step-by-Step Setup

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

        ## 2. Copy SSH Key to the Server

        ```bash
        ssh-copy-id -i ~/.ssh/id_{user}.pub -p {port} {user}@{server_ip}
        # Alternatively
        scp ~/.ssh/id_{user}.pub {user}@{server_ip}:/home/{user}/.ssh/authorized_keys
        ```

        ## 3. Configure Nginx

        ```nginx
        server {{
            listen 80;
            server_name {domain};

            location / {{
                proxy_pass http://127.0.0.1:{app_port};
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }}
        }}
        ```

        ## 4. SSL Certificate

        ```bash
        sudo certbot --nginx -d {domain}
        ```
    """)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nFile created: {filename}")

if __name__ == "__main__":
    main()
