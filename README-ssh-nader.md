
# SSH Key Setup for Secure Server and GitHub Access

This guide provides instructions for setting up SSH keys for:

1. Connecting from your Windows machine to the server (nader)
2. Allowing the server to access GitHub

---

## SSH Keys Used

| Device           | Connects To           | Key Name           | Private Key Location             | Public Key Destination            |
|------------------|------------------------|---------------------|----------------------------------|----------------------------------|
| Windows Machine  | Server (nader)        | id_mystro         | C:\Users\<User>\.ssh\           | /home/nader/.ssh/authorized_keys  |
| Server (nader)  | GitHub (repo access)   | id_git_nystro        | /home/nader/.ssh/               | GitHub → Settings → SSH Keys     |

---

## 1. Setup SSH Access from Windows to Server

### On the server (as root or sudo user):

```bash
sudo adduser nader
sudo usermod -aG sudo nader
sudo mkdir -p /home/nader/.ssh
sudo chown nader:nader /home/nader/.ssh
sudo chmod 700 /home/nader/.ssh
```

### On your Windows machine:

```powershell
ssh-keygen -t ed25519 -C "nader-server" -f ${env:USERPROFILE}\.ssh\id_mystro
Get-Content ${env:USERPROFILE}\.ssh\id_mystro.pub | Set-Clipboard
```

### Paste the key on the server:

```bash
sudo nano /home/nader/.ssh/authorized_keys
sudo chmod 600 /home/nader/.ssh/authorized_keys
sudo chown nader:nader /home/nader/.ssh/authorized_keys
```

### Test the connection:

```powershell
ssh -i ${env:USERPROFILE}\.ssh\id_mystro -p 13976 nader@78.47.205.8
```

---

## 2. Setup SSH Key for Server to GitHub Access

### On the server (as user nader):

```bash
ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/id_git_nystro
cat ~/.ssh/id_git_nystro.pub
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
git clone git@github.com:TamerOnLine/TamerOnLine.git
```

---

## Optional: Delete the User

```bash
sudo deluser --remove-home nader
ls /home
```

---

## Setup Completed Successfully
