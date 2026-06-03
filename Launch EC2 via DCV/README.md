# 🚀 Launch EC2 via NICE DCV

<p align="center">

![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![NICE%20DCV](https://img.shields.io/badge/NICE-DCV-0066CC?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Terminal-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Remote Desktop](https://img.shields.io/badge/Remote-Desktop-success?style=for-the-badge)

</p>

---

# 📖 Overview

This lab demonstrates how to deploy a cloud-hosted Linux desktop environment using **Amazon EC2** and **NICE DCV**.

NICE DCV provides a secure, high-performance remote desktop solution that allows users to access graphical Linux desktops hosted in AWS.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Launch an EC2 instance on AWS

✅ Configure Security Groups

✅ Install NICE DCV Server

✅ Create and manage DCV sessions

✅ Connect remotely using DCV Client

✅ Verify graphical desktop functionality

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

- Basic Linux command-line knowledge
- Understanding of SSH connections
- Familiarity with nano or vim editors
- AWS Account with EC2 permissions
- NICE DCV Client installed locally

---

# 🏗️ Architecture Overview

```text
┌──────────────────┐
│ Local Computer   │
│ NICE DCV Client  │
└────────┬─────────┘
         │ TCP/UDP 8443
         │
         ▼
┌─────────────────────────┐
│ AWS EC2 Ubuntu Server   │
│ NICE DCV Server         │
│ Ubuntu Desktop          │
└─────────────────────────┘
```

---

# ⚙️ Environment Requirements

| Component | Requirement |
|------------|------------|
| Cloud Provider | AWS |
| OS | Ubuntu 22.04 LTS |
| Instance Type | t2.medium |
| Storage | 30 GB gp3 |
| DCV Port | 8443 |
| SSH Port | 22 |

---

# 🧪 Task 1: Launch EC2 Instance

---

## 🔹 Step 1.1 Create EC2 Instance

Login to AWS Console.

Navigate:

```text
AWS Console
 └── EC2 Dashboard
      └── Launch Instance
```

Configure:

| Setting | Value |
|----------|---------|
| Name | dcv-lab-instance |
| AMI | Ubuntu Server 22.04 LTS |
| Instance Type | t2.medium |
| Key Pair | Existing or New |

⚠️ Save the `.pem` file securely.

---

## 🔹 Step 1.2 Configure Storage

Set:

```text
Root Volume = 30 GB gp3
```

Keep all other options default.

---

## 🔹 Step 1.3 Launch Instance

Click:

```text
Launch Instance
```

Wait until status becomes:

```text
Running
```

Record:

```text
Public IPv4 Address
```

---

# 🔐 Task 2: Configure Security Groups

---

## 🔹 Step 2.1 Edit Inbound Rules

Navigate:

```text
EC2
 └── Instance
      └── Security
           └── Security Group
```

Add:

### SSH

| Property | Value |
|------------|---------|
| Protocol | TCP |
| Port | 22 |
| Source | My IP |

---

### NICE DCV TCP

| Property | Value |
|------------|---------|
| Protocol | TCP |
| Port | 8443 |
| Source | My IP |

---

### NICE DCV UDP

| Property | Value |
|------------|---------|
| Protocol | UDP |
| Port | 8443 |
| Source | My IP |

---

✅ Save Rules

---

# 🖥️ Task 3: Install NICE DCV Server

---

## 🔹 Step 3.1 Connect via SSH

### Secure Key

```bash
chmod 400 your-key-pair.pem
```

### Connect

```bash
ssh -i your-key-pair.pem ubuntu@YOUR_PUBLIC_IP
```

---

## 🔹 Step 3.2 Install Desktop Environment

### Update Packages

```bash
sudo apt update
```

### Install Ubuntu Desktop

```bash
sudo apt install -y ubuntu-desktop
```

### Install Graphics Dependencies

```bash
sudo apt install -y mesa-utils
```

---

## 🔹 Step 3.3 Download NICE DCV

### Download Package

```bash
wget https://d1uj6qtbmh3dt5.cloudfront.net/2023.0/Servers/nice-dcv-2023.0-15065-ubuntu2204-x86_64.tgz
```

### Extract

```bash
tar -xvzf nice-dcv-2023.0-15065-ubuntu2204-x86_64.tgz
```

### Enter Directory

```bash
cd nice-dcv-2023.0-15065-ubuntu2204-x86_64
```

---

## 🔹 Step 3.4 Install DCV Server

```bash
sudo apt install -y ./nice-dcv-server_2023.0.15065-1_amd64.ubuntu2204.deb
```

### Install Web Viewer

```bash
sudo apt install -y ./nice-dcv-web-viewer_2023.0.15065-1_amd64.ubuntu2204.deb
```

---

## 🔹 Step 3.5 Configure NICE DCV

Create configuration directory:

```bash
sudo mkdir -p /etc/dcv
```

Set Ubuntu password:

```bash
sudo passwd ubuntu
```

Enable service:

```bash
sudo systemctl enable dcvserver
```

Start service:

```bash
sudo systemctl start dcvserver
```

---

# 🖥️ Task 4: Create DCV Session

---

## 🔹 Create Session

```bash
sudo dcv create-session --type=console --owner ubuntu my-session
```

---

## 🔹 Verify Session

```bash
sudo dcv list-sessions
```

Expected:

```text
Session: my-session
Owner: ubuntu
Type: console
```

---

# 🌐 Task 5: Install NICE DCV Client

---

## Windows / macOS

Download:

```text
https://download.nice-dcv.com
```

---

## Linux

```bash
wget https://d1uj6qtbmh3dt5.cloudfront.net/2023.0/Clients/nice-dcv-viewer_2023.0.5483-1_amd64.ubuntu2204.deb
```

Install:

```bash
sudo apt install -y ./nice-dcv-viewer_2023.0.5483-1_amd64.ubuntu2204.deb
```

---

# 🔗 Task 6: Connect to NICE DCV

---

## Open NICE DCV Viewer

Connection String:

```text
YOUR_PUBLIC_IP:8443
```

Example:

```text
54.123.45.67:8443
```

---

## Login

Username:

```text
ubuntu
```

Password:

```text
Your Ubuntu Password
```

---

## Trust Certificate

Click:

```text
Trust & Connect
```

---

# ✅ Verification

---

## Verify DCV Service

```bash
sudo systemctl status dcvserver
```

---

## Verify Sessions

```bash
sudo dcv list-sessions
```

---

## Verify Version

```bash
dcv version
```

---

## Verify Display

Inside remote terminal:

```bash
echo $DISPLAY
```

Expected:

```text
:0
```

---

## Verify OpenGL

```bash
glxinfo | grep OpenGL
```

Expected:

```text
OpenGL renderer string ...
```

---

## Verify User Session

```bash
who
```

Expected:

```text
ubuntu pts/0 ...
```

---

# 🧪 Desktop Functionality Test

Perform the following:

✅ Open Firefox

✅ Open Files Application

✅ Create Text File

✅ Move Windows Around

✅ Test Clipboard

✅ Verify Keyboard Input

✅ Verify Mouse Input

---

# 🛠️ Troubleshooting Guide

---

## ❌ SSH Connection Failed

### Verify Security Group

```text
Port 22 Open
```

### Verify Key Permissions

```bash
chmod 400 your-key.pem
```

### Verify Instance Running

```text
EC2 Status = Running
```

---

## ❌ DCV Connection Failed

Check service:

```bash
sudo systemctl status dcvserver
```

Verify session:

```bash
sudo dcv list-sessions
```

Check security group:

```text
TCP 8443 Open
UDP 8443 Open
```

---

## ❌ Black Screen

Verify desktop installation:

```bash
dpkg -l | grep ubuntu-desktop
```

Restart DCV:

```bash
sudo systemctl restart dcvserver
```

Reconnect after 2 minutes.

---

## ❌ Session Not Found

Create new session:

```bash
sudo dcv create-session --type=console --owner ubuntu my-session
```

Verify:

```bash
sudo dcv list-sessions
```

---

# 🧹 Cleanup

To avoid AWS charges:

Terminate EC2 Instance:

```text
EC2 Dashboard
 └── Instance
      └── Terminate
```

Delete:

- Security Groups
- Key Pairs
- Snapshots (optional)

---

# 🎉 Conclusion

You have successfully:

✅ Launched an AWS EC2 instance

✅ Installed Ubuntu Desktop

✅ Installed NICE DCV Server

✅ Configured Security Groups

✅ Created Remote Desktop Sessions

✅ Connected Using NICE DCV Client

✅ Verified Full Remote Desktop Functionality

---

# 🌟 Real-World Applications

🔹 Cloud Development Workstations

🔹 Remote Linux Desktops

🔹 GPU-Based Workstations

🔹 CAD & 3D Rendering Environments

🔹 Scientific Computing Desktops

🔹 Secure Enterprise VDI Solutions

---

# 📚 Key Takeaway

**NICE DCV enables secure, high-performance remote desktop access to cloud-hosted Linux environments, making AWS EC2 instances function like powerful virtual workstations accessible from anywhere in the world.**

---
⭐ Lab Completed Successfully
⭐ AWS + Ubuntu + NICE DCV Remote Desktop Environment Ready
