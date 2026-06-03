# 🚀 Multi-Container Applications with Docker Compose

![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-Orchestration-1488C6?logo=docker)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask)
![Redis](https://img.shields.io/badge/Redis-Database-DC382D?logo=redis)
![Nginx](https://img.shields.io/badge/Nginx-Frontend-009639?logo=nginx)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?logo=ubuntu)

---

# 📖 Overview

In this lab, you will build and deploy a complete **multi-container application** using **Docker Compose**.

The application consists of three services:

| Service | Purpose |
|----------|----------|
| 🌐 Frontend | Nginx web server serving HTML UI |
| ⚙️ Backend | Python Flask REST API |
| 🗄️ Database | Redis data store |

You will learn how containers communicate, share networks, manage dependencies, and work together as a complete application stack.

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

✅ Create custom Dockerfiles for different application components

✅ Configure multi-container applications using Docker Compose

✅ Establish container networking and inter-service communication

✅ Manage application dependencies and startup order

✅ Deploy and verify a complete multi-tier application stack

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

- Basic understanding of Docker containers and images
- Familiarity with Dockerfile syntax
- Command-line proficiency in Linux
- Understanding of frontend/backend architecture
- Previous Docker experience

---

# 🛠️ Environment Setup

## Step 1: Start Lab Environment

Click **Start Lab** and connect to your Linux machine.

---

## Step 2: Install Docker

```bash
sudo apt update
sudo apt install -y docker.io
```

Start Docker:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

---

## Step 3: Configure Docker Permissions

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## Step 4: Install Docker Compose

```bash
sudo apt install -y docker-compose
```

Verify installation:

```bash
docker --version
docker-compose --version
```

Expected Output:

```text
Docker version xx.x.x
docker-compose version xx.x.x
```

---

# 🏗️ Task 1: Build a Multi-Container Application

---

## 📁 Step 1: Create Project Structure

```bash
mkdir ~/multi-container-app
cd ~/multi-container-app

mkdir frontend backend

touch docker-compose.yml

touch frontend/Dockerfile
touch frontend/index.html
touch frontend/nginx.conf

touch backend/Dockerfile
touch backend/app.py
touch backend/requirements.txt
```

Verify:

```bash
tree .
```

Expected Structure:

```text
multi-container-app/
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
└── backend
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

---

# ⚙️ Step 2: Build Backend Service

## Create Flask Application

File:

```bash
nano backend/app.py
```

Add:

```python
from flask import Flask, jsonify, request
import redis
import os

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

@app.route('/api/visits', methods=['GET'])
def get_visits():
    visits = redis_client.incr('visits')
    return jsonify({"visits": visits})

@app.route('/api/message', methods=['POST'])
def set_message():
    data = request.get_json()
    redis_client.set('message', data['message'])
    return jsonify({"status": "saved"})

@app.route('/api/message', methods=['GET'])
def get_message():
    msg = redis_client.get('message')
    return jsonify({"message": msg})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## Create Requirements File

```bash
nano backend/requirements.txt
```

```text
flask==2.3.0
redis==4.5.0
```

---

## Create Backend Dockerfile

```bash
nano backend/Dockerfile
```

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# 🌐 Step 3: Build Frontend Service

## Create HTML Interface

```bash
nano frontend/index.html
```

```html
<!DOCTYPE html>
<html>
<head>
<title>Multi-Container App</title>
</head>
<body>

<h1>Docker Compose Demo</h1>

<button onclick="getVisits()">Visits</button>
<button onclick="setMessage()">Set Message</button>
<button onclick="getMessage()">Get Message</button>

<div id="result"></div>

<script>

async function getVisits() {
    const response = await fetch('/api/visits');
    const data = await response.json();
    document.getElementById('result').innerText =
        JSON.stringify(data);
}

async function setMessage() {
    const message = prompt("Enter Message");

    await fetch('/api/message', {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({message})
    });

    document.getElementById('result').innerText =
        "Message Saved";
}

async function getMessage() {
    const response = await fetch('/api/message');
    const data = await response.json();

    document.getElementById('result').innerText =
        JSON.stringify(data);
}

</script>

</body>
</html>
```

---

## Create Nginx Configuration

```bash
nano frontend/nginx.conf
```

```nginx
server {

    listen 80;

    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    location /api/ {

        proxy_pass http://backend:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    }
}
```

---

## Create Frontend Dockerfile

```bash
nano frontend/Dockerfile
```

```dockerfile
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html /usr/share/nginx/html/

EXPOSE 80
```

---

# 🐳 Task 2: Configure Docker Compose

---

## Step 1: Create docker-compose.yml

```bash
nano docker-compose.yml
```

```yaml
version: '3.8'

services:

  redis:
    image: redis:alpine
    container_name: redis
    networks:
      - app-network

  backend:
    build: ./backend
    container_name: backend

    ports:
      - "5000:5000"

    environment:
      REDIS_HOST: redis

    depends_on:
      - redis

    networks:
      - app-network

  frontend:
    build: ./frontend
    container_name: frontend

    ports:
      - "8080:80"

    depends_on:
      - backend

    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

---

## Step 2: Build Images

```bash
docker-compose build
```

Expected Output:

```text
Successfully built image
Successfully tagged frontend
Successfully tagged backend
```

---

## Step 3: Start Application Stack

```bash
docker-compose up -d
```

Verify:

```bash
docker-compose ps
```

Expected:

```text
frontend   Up
backend    Up
redis      Up
```

---

# 🔍 Verification

---

## Verify Containers

```bash
docker-compose ps
```

Expected:

```text
3 containers running
```

---

## Verify Network

```bash
docker network ls
```

Inspect:

```bash
docker network inspect multi-container-app_app-network
```

---

## Verify Backend API

### Visit Counter

```bash
curl http://localhost:5000/api/visits
```

Example:

```json
{
  "visits": 1
}
```

---

### Store Message

```bash
curl -X POST http://localhost:5000/api/message \
-H "Content-Type: application/json" \
-d '{"message":"Hello Docker"}'
```

---

### Retrieve Message

```bash
curl http://localhost:5000/api/message
```

Expected:

```json
{
  "message":"Hello Docker"
}
```

---

## Verify Frontend

```bash
curl http://localhost:8080
```

Or open browser:

```text
http://localhost:8080
```

You should see:

✅ Docker Compose Demo page

✅ Working buttons

✅ Backend communication

---

## Verify Inter-Container Communication

Ping Redis from Backend:

```bash
docker-compose exec backend ping redis -c 3
```

Expected:

```text
3 packets transmitted
3 packets received
```

---

## Verify Redis Data

List keys:

```bash
docker-compose exec redis redis-cli KEYS '*'
```

Expected:

```text
visits
message
```

Read visit count:

```bash
docker-compose exec redis redis-cli GET visits
```

---

# 📈 Application Scaling

Scale backend service:

```bash
docker-compose up -d --scale backend=2
```

Verify:

```bash
docker-compose ps
```

Expected:

```text
backend_1
backend_2
frontend
redis
```

---

# 🧪 Troubleshooting Guide

## Containers Fail to Start

View logs:

```bash
docker-compose logs
```

Single service:

```bash
docker-compose logs backend
```

---

## Port Already In Use

Check:

```bash
sudo netstat -tulpn | grep 8080
```

Change port mapping if necessary.

---

## Redis Connection Problems

Check Redis:

```bash
docker-compose ps redis
```

Test connectivity:

```bash
docker-compose exec backend ping redis
```

Check environment variables:

```bash
docker-compose exec backend env | grep REDIS
```

---

## Changes Not Reflected

Rebuild images:

```bash
docker-compose build --no-cache
docker-compose up -d
```

Force recreate:

```bash
docker-compose up -d --force-recreate
```

---

# 🧹 Cleanup

Stop containers:

```bash
docker-compose down
```

Remove volumes:

```bash
docker-compose down -v
```

Remove images:

```bash
docker-compose down --rmi all
```

Delete project:

```bash
cd ~
rm -rf multi-container-app
```

---

# 📊 Expected Outcomes

After completing this lab you should have:

✅ Custom Dockerfiles for frontend and backend

✅ Redis database container

✅ Docker Compose orchestration

✅ Container networking

✅ Inter-service communication

✅ Application scaling capability

✅ Multi-tier architecture deployment

---

# 🎓 Key Takeaways

### Docker Compose Benefits

- Simplifies multi-container deployments
- Manages service dependencies
- Creates isolated networks automatically
- Supports scaling and orchestration

### Container Networking

Containers communicate using:

```text
service-name:port
```

Example:

```text
backend → redis:6379
frontend → backend:5000
```

### Modern Application Architecture

```text
┌─────────────┐
│   Frontend  │
│   Nginx     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │
│   Flask API │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Redis    │
│  Database   │
└─────────────┘
```

---

# 🏁 Conclusion

Congratulations! 🎉

You successfully built a complete **multi-container application stack** using Docker Compose.

You learned how to:

- Build custom Docker images
- Configure multi-service applications
- Create container networks
- Enable inter-container communication
- Manage dependencies and startup order
- Scale application services

These skills form the foundation of modern **microservices**, **cloud-native applications**, **DevOps workflows**, and **Kubernetes-based deployments**.

🚀 You're now ready to move toward container orchestration, Kubernetes, CI/CD pipelines, and production-grade cloud-native architectures.
