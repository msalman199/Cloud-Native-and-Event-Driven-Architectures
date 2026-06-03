# 🚀 Upload Logs to S3 Using MinIO

<p align="center">

![MinIO](https://img.shields.io/badge/MinIO-S3_Compatible-C72E49?style=for-the-badge\&logo=minio\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)
![Object Storage](https://img.shields.io/badge/Object-Storage-blue?style=for-the-badge)
![CLI](https://img.shields.io/badge/MinIO_Client-mc-success?style=for-the-badge)
![Storage](https://img.shields.io/badge/S3-Compatible-orange?style=for-the-badge)

</p>

---

# 📖 Overview

This lab demonstrates how to build a local **S3-compatible object storage environment** using **MinIO**.

You will install and configure a MinIO server, create storage buckets, generate sample application logs, upload files through both the web interface and command-line tools, and verify successful storage operations.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Deploy a local S3-compatible storage system using MinIO

✅ Create and manage storage buckets

✅ Configure MinIO Client (mc)

✅ Upload files via Web Console

✅ Upload files via Command Line Interface

✅ Verify stored objects and bucket contents

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

* Basic Linux command-line knowledge
* Understanding of file operations
* Familiarity with nano or vim
* Ubuntu Linux environment
* Internet connectivity

---

# 🏗️ Architecture Overview

```text
                    ┌─────────────────────┐
                    │   Application Logs  │
                    │ app.log / error.log │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      MinIO Server   │
                    │  S3 Compatible API  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
      ┌─────────────────┐       ┌─────────────────┐
      │ Web Console     │       │ MinIO Client mc │
      │ Port 9001       │       │ CLI Uploads     │
      └─────────────────┘       └─────────────────┘
```

---

# ⚙️ Environment Setup

---

## 🔹 Step 1: Update System

```bash
sudo apt update
```

---

## 🔹 Step 2: Install MinIO Server

### Download Server

```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio
```

### Make Executable

```bash
chmod +x minio
```

### Move Binary

```bash
sudo mv minio /usr/local/bin/
```

---

## 🔹 Step 3: Install MinIO Client

### Download Client

```bash
wget https://dl.min.io/client/mc/release/linux-amd64/mc
```

### Make Executable

```bash
chmod +x mc
```

### Move Binary

```bash
sudo mv mc /usr/local/bin/
```

---

## 🔹 Step 4: Verify Installation

```bash
minio --version
```

```bash
mc --version
```

Expected:

```text
minio version RELEASE.x.x.x
mc version RELEASE.x.x.x
```

---

# 🧪 Task 1: Configure MinIO Storage

---

## 🔹 Step 1.1 Create Data Directory

```bash
mkdir -p ~/minio-data
```

---

## 🔹 Step 1.2 Start MinIO Server

```bash
minio server ~/minio-data --console-address ":9001"
```

Expected Output:

```text
MinIO Object Storage Server

API: http://localhost:9000
Console: http://localhost:9001

RootUser: minioadmin
RootPass: minioadmin
```

⚠️ Leave this terminal running.

---

## 🔹 Step 1.3 Access Web Console

Open browser:

```text
http://localhost:9001
```

Login Credentials:

```text
Username: minioadmin
Password: minioadmin
```

---

## 🔹 Step 1.4 Create Bucket Using Web Console

Navigate:

```text
Buckets
 └── Create Bucket
```

Bucket Name:

```text
application-logs
```

Click:

```text
Create Bucket
```

Verification:

```text
application-logs
```

appears in bucket list.

---

## 🔹 Step 1.5 Configure MinIO Client

Add MinIO Alias:

```bash
mc alias set myminio http://localhost:9000 minioadmin minioadmin
```

Expected:

```text
Added 'myminio' successfully.
```

Verify Connection:

```bash
mc admin info myminio
```

---

## 🔹 Step 1.6 Create Bucket via CLI

```bash
mc mb myminio/backup-logs
```

Expected:

```text
Bucket created successfully.
```

List Buckets:

```bash
mc ls myminio
```

Expected:

```text
application-logs
backup-logs
```

---

# 🧪 Task 2: Generate Sample Log Files

---

## 🔹 Step 2.1 Create Log Directory

```bash
mkdir -p ~/app-logs
cd ~/app-logs
```

---

## 🔹 Step 2.2 Create Application Log

```bash
cat > app.log << 'EOF'
2024-01-15 10:23:45 INFO Application started successfully
2024-01-15 10:23:46 INFO Database connection established
2024-01-15 10:24:12 WARN High memory usage detected: 85%
2024-01-15 10:25:33 INFO User login: user123
2024-01-15 10:26:01 ERROR Failed to process request: timeout
2024-01-15 10:26:02 INFO Retry attempt 1/3
2024-01-15 10:26:05 INFO Request processed successfully
2024-01-15 10:30:15 INFO User logout: user123
EOF
```

---

## 🔹 Step 2.3 Create Error Log

```bash
cat > error.log << 'EOF'
2024-01-15 10:26:01 ERROR Connection timeout to external API
2024-01-15 10:26:01 ERROR Stack trace: api.service.line45
2024-01-15 11:15:22 ERROR Database query failed: syntax error
2024-01-15 11:15:22 ERROR Query: SELECT * FROM users WHERE
EOF
```

---

## 🔹 Step 2.4 Verify Logs

```bash
ls -lh
```

```bash
cat app.log
```

Expected Files:

```text
app.log
error.log
```

---

# 📤 Task 3: Upload Logs Using Web Console

---

## 🔹 Step 3.1 Open Bucket

Navigate:

```text
Buckets
 └── application-logs
```

---

## 🔹 Step 3.2 Upload File

Click:

```text
Upload
 └── Upload File
```

Select:

```text
~/app-logs/app.log
```

Upload file.

Verification:

```text
app.log
```

appears in bucket.

---

# 📤 Task 4: Upload Logs Using CLI

---

## 🔹 Step 4.1 Upload Single File

```bash
mc cp ~/app-logs/error.log myminio/application-logs/
```

Expected:

```text
error.log uploaded successfully
```

---

## 🔹 Step 4.2 Upload Entire Directory

```bash
mc cp --recursive ~/app-logs myminio/backup-logs/
```

---

## 🔹 Step 4.3 Verify Uploaded Objects

List Files:

```bash
mc ls myminio/application-logs
```

Expected:

```text
app.log
error.log
```

---

List Backup Bucket:

```bash
mc ls myminio/backup-logs
```

Expected:

```text
app.log
error.log
```

---

# 🔍 Task 5: Verify Object Storage

---

## Verify Buckets

```bash
mc ls myminio
```

Expected:

```text
application-logs
backup-logs
```

---

## Verify Objects

```bash
mc ls myminio/application-logs
```

---

## Verify Object Details

```bash
mc stat myminio/application-logs/app.log
```

Expected:

```text
Name
Size
ETag
Content-Type
Last Modified
```

---

## Download File Test

```bash
mc cp myminio/application-logs/app.log .
```

Verify:

```bash
cat app.log
```

---

# ✅ Verification Checklist

| Check              | Status |
| ------------------ | ------ |
| MinIO Installed    | ✅      |
| MinIO Running      | ✅      |
| Console Accessible | ✅      |
| Bucket Created     | ✅      |
| Client Configured  | ✅      |
| Logs Generated     | ✅      |
| Files Uploaded     | ✅      |
| Files Retrieved    | ✅      |

---

# 🛠️ Troubleshooting Guide

---

## ❌ MinIO Not Starting

Check Port Usage:

```bash
sudo ss -tulpn | grep 9000
```

Kill Conflicting Process:

```bash
sudo kill -9 PID
```

Restart MinIO.

---

## ❌ Cannot Access Console

Verify Service:

```bash
curl http://localhost:9001
```

Check Firewall:

```bash
sudo ufw status
```

Allow Ports:

```bash
sudo ufw allow 9000
sudo ufw allow 9001
```

---

## ❌ mc Cannot Connect

Verify Alias:

```bash
mc alias list
```

Reconfigure:

```bash
mc alias set myminio http://localhost:9000 minioadmin minioadmin
```

---

## ❌ Upload Fails

Check Bucket Exists:

```bash
mc ls myminio
```

Verify File Exists:

```bash
ls -lh ~/app-logs
```

---

## ❌ Permission Errors

Check Ownership:

```bash
ls -ld ~/minio-data
```

Fix Permissions:

```bash
chmod -R 755 ~/minio-data
```

---

# 📊 Useful MinIO Commands

## List Buckets

```bash
mc ls myminio
```

## Create Bucket

```bash
mc mb myminio/new-bucket
```

## Upload File

```bash
mc cp file.txt myminio/bucket/
```

## Download File

```bash
mc cp myminio/bucket/file.txt .
```

## Remove Object

```bash
mc rm myminio/bucket/file.txt
```

## Remove Bucket

```bash
mc rb myminio/bucket
```

---

# 🧹 Cleanup

Stop MinIO:

```bash
CTRL + C
```

Remove Data:

```bash
rm -rf ~/minio-data
```

Remove Logs:

```bash
rm -rf ~/app-logs
```

Remove Aliases:

```bash
mc alias remove myminio
```

---

# 🎉 Conclusion

You have successfully:

✅ Installed MinIO Server

✅ Installed MinIO Client (mc)

✅ Created S3-Compatible Buckets

✅ Uploaded Log Files via Web Interface

✅ Uploaded Log Files via CLI

✅ Verified Stored Objects

✅ Retrieved Files from Object Storage

---

# 🌟 Real-World Applications

🔹 Centralized Log Storage

🔹 Backup and Archiving Systems

🔹 CI/CD Artifact Storage

🔹 Application Data Lakes

🔹 Kubernetes Object Storage

🔹 Cloud-Native Storage Platforms

---

# 📚 Key Takeaway

**MinIO provides a lightweight, high-performance, S3-compatible object storage platform that can be deployed locally or in production environments, making it ideal for log storage, backups, and cloud-native applications.**

---

⭐ Lab Completed Successfully

⭐ MinIO Object Storage Ready

⭐ Logs Uploaded and Verified
