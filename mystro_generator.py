import textwrap

def main():
    """
    Collects SSH configuration details from the user and generates a
    Markdown file containing SSH setup instructions for server and GitHub access.
    """
    user = input("Enter the new username (e.g., mystro): ")
    server_ip = input("Enter the server IP address: ")
    ssh_port = input("Enter the SSH port (e.g., 13976): ")
    key_clean = input("Enter the Windows to Server SSH key filename (e.g., id_mystro_clean): ")
    key_github = input("Enter the GitHub SSH key filename on the server (e.g., github_key_mystro): ")
    repo_name = input("Enter the GitHub repository name (e.g., mystro): ")

    filename = f"README-ssh-{user}.md"

    content = textwrap.dedent(f"""
        # SSH Key Setup for Secure Server and GitHub Access

        This guide provides instructions for setting up SSH keys for:

        1. Connecting from your Windows machine to the server ({user})
        2. Allowing the server to access GitHub

        ---

        ## SSH Keys Used

        | Device           | Connects To           | Key Name           | Private Key Location             | Public Key Destination            |
        |------------------|------------------------|---------------------|----------------------------------|----------------------------------|
        | Windows Machine  | Server ({user})        | {key_clean}         | C:\\Users\\<User>\\.ssh\\           | /home/{user}/.ssh/authorized_keys  |
        | Server ({user})  | GitHub (repo access)   | {key_github}        | /home/{user}/.ssh/               | GitHub → Settings → SSH Keys     |

        ---

        ## 1. Setup SSH Access from Windows to Server

        ### On the server (as root or sudo user):

        ```bash
        sudo adduser {user}
        sudo usermod -aG sudo {user}
        sudo mkdir -p /home/{user}/.ssh
        sudo chown {user}:{user} /home/{user}/.ssh
        sudo chmod 700 /home/{user}/.ssh
        ```

        ### On your Windows machine:

        ```powershell
        ssh-keygen -t ed25519 -C "{user}-server" -f ${{env:USERPROFILE}}\\.ssh\\{key_clean}
        Get-Content ${{env:USERPROFILE}}\\.ssh\\{key_clean}.pub | Set-Clipboard
        ```

        ### Paste the key on the server:

        ```bash
        sudo nano /home/{user}/.ssh/authorized_keys
        sudo chmod 600 /home/{user}/.ssh/authorized_keys
        sudo chown {user}:{user} /home/{user}/.ssh/authorized_keys
        ```

        ### Test the connection:

        ```powershell
        ssh -i ${{env:USERPROFILE}}\\.ssh\\{key_clean} -p {ssh_port} {user}@{server_ip}
        ```

        ---

        ## 2. Setup SSH Key for Server to GitHub Access

        ### On the server (as user {user}):

        ```bash
        ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/{key_github}
        cat ~/.ssh/{key_github}.pub
        ```

        Then add the key to GitHub:

        - Navigate to: GitHub → Settings → SSH and GPG Keys
        - Click: **New SSH Key**
        - Title: `deploy key from server`
        - Paste the public key

        ### Test the connection:

        ```bash
        ssh -T git@github.com
        ```

        ---

        ## 3. Clone the GitHub Repository

        ```bash
        cd ~
        git clone git@github.com:TamerOnLine/{repo_name}.git
        ```

        ---

        ## Optional: Delete the User

        ```bash
        sudo deluser --remove-home {user}
        ls /home
        ```

        ---

        ## Setup Completed Successfully
    """)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nFile created successfully: {filename}")


if __name__ == "__main__":
    main()