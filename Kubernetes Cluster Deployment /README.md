# ☸️ Kubernetes Cluster Deployment

![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes)
![Minikube](https://img.shields.io/badge/Minikube-Local_Cluster-FF6F00)
![Docker](https://img.shields.io/badge/Docker-Container_Runtime-2496ED?logo=docker)
![kubectl](https://img.shields.io/badge/kubectl-Cluster_Management-326CE5)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?logo=ubuntu)
![YAML](https://img.shields.io/badge/YAML-Configuration-CB171E)

---

# 🚀 Overview

In this lab, you will deploy and manage applications on a local Kubernetes cluster using **Minikube**.

You will learn how to:

* Create a Kubernetes cluster
* Deploy containerized applications
* Manage pods and deployments
* Expose applications using services
* Scale workloads dynamically
* Monitor cluster health

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Set up a single-node Kubernetes cluster using Minikube

✅ Deploy containerized applications as Pods

✅ Create and manage Kubernetes Services

✅ Expose applications for external access

✅ Verify cluster health and application status

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

* Basic Linux command-line knowledge
* Understanding of Docker and containers
* Familiarity with YAML syntax
* Basic networking knowledge
* Root or sudo privileges

---

# 🛠️ Environment Setup

## System Requirements

| Resource   | Requirement                   |
| ---------- | ----------------------------- |
| CPU        | 2 Cores Minimum               |
| RAM        | 2GB Minimum (4GB Recommended) |
| Disk Space | 20GB Free                     |
| OS         | Ubuntu 20.04+                 |
| Internet   | Required                      |

---

# Step 1: Install Docker

Update package index:

```bash
sudo apt-get update
```

Install Docker:

```bash
sudo apt-get install -y docker.io
```

Start and enable Docker:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Add current user to Docker group:

```bash
sudo usermod -aG docker $USER
```

Apply group changes:

```bash
newgrp docker
```

Verify Docker:

```bash
docker --version
```

---

# Step 2: Install kubectl

Download kubectl:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

Make executable:

```bash
chmod +x kubectl
```

Move to system path:

```bash
sudo mv kubectl /usr/local/bin/
```

Verify installation:

```bash
kubectl version --client
```

Expected Output:

```text
Client Version: v1.xx.x
```

---

# Step 3: Install Minikube

Download Minikube:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
```

Install:

```bash
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Verify:

```bash
minikube version
```

Expected Output:

```text
minikube version: v1.xx.x
```

---

# ☸️ Task 1: Setup Kubernetes Cluster

---

## Step 1: Start Minikube Cluster

Start cluster using Docker driver:

```bash
minikube start --driver=docker
```

Wait 2–3 minutes for initialization.

---

## Step 2: Verify Cluster Status

Check Minikube:

```bash
minikube status
```

View cluster information:

```bash
kubectl cluster-info
```

List nodes:

```bash
kubectl get nodes
```

Check system pods:

```bash
kubectl get pods -n kube-system
```

Expected Results:

✅ Minikube Running

✅ One Node in Ready state

✅ System Pods Running

---

## Step 3: Enable Metrics Server

Enable addon:

```bash
minikube addons enable metrics-server
```

Verify:

```bash
minikube addons list
```

Expected:

```text
metrics-server | enabled
```

---

# 🚀 Task 2: Deploy Pods and Services

---

## Step 1: Create Deployment Manifest

Create workspace:

```bash
mkdir -p ~/k8s-lab
cd ~/k8s-lab
```

Create deployment file:

```bash
nano nginx-deployment.yaml
```

Paste:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: nginx-deployment

spec:
  replicas: 3

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
      - name: nginx
        image: nginx:1.21

        ports:
        - containerPort: 80

        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"

          limits:
            memory: "128Mi"
            cpu: "200m"
```

Apply deployment:

```bash
kubectl apply -f nginx-deployment.yaml
```

Watch progress:

```bash
kubectl get deployments -w
```

Expected:

```text
nginx-deployment 3/3 READY
```

---

## Step 2: Verify Pods

List pods:

```bash
kubectl get pods
```

Detailed view:

```bash
kubectl get pods -o wide
```

Describe pod:

```bash
kubectl describe pod <POD_NAME>
```

View logs:

```bash
kubectl logs <POD_NAME>
```

---

## Step 3: Create Service

Create service file:

```bash
nano nginx-service.yaml
```

Paste:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: nginx-service

spec:
  type: NodePort

  selector:
    app: nginx

  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30080
```

Apply:

```bash
kubectl apply -f nginx-service.yaml
```

Verify:

```bash
kubectl get services
```

Describe service:

```bash
kubectl describe service nginx-service
```

---

## Step 4: Access Application

Get Minikube IP:

```bash
minikube ip
```

Get service URL:

```bash
minikube service nginx-service --url
```

Test:

```bash
curl $(minikube service nginx-service --url)
```

Expected:

```html
Welcome to nginx!
```

---

## Step 5: Scale Deployment

Increase replicas:

```bash
kubectl scale deployment nginx-deployment --replicas=5
```

Watch scaling:

```bash
kubectl get pods -w
```

Verify:

```bash
kubectl get deployment nginx-deployment
```

Expected:

```text
5/5 READY
```

---

# 🌐 Deploy Custom Web Application

Create file:

```bash
nano webapp-deployment.yaml
```

Paste:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: webapp

spec:
  replicas: 2

  selector:
    matchLabels:
      app: webapp

  template:
    metadata:
      labels:
        app: webapp

    spec:
      containers:
      - name: webapp
        image: hashicorp/http-echo

        args:
        - "-text=Hello from Kubernetes Pod"
        - "-listen=:8080"

        ports:
        - containerPort: 8080

---

apiVersion: v1
kind: Service

metadata:
  name: webapp-service

spec:
  type: NodePort

  selector:
    app: webapp

  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
    nodePort: 30081
```

Deploy:

```bash
kubectl apply -f webapp-deployment.yaml
```

Wait:

```bash
kubectl wait --for=condition=ready pod -l app=webapp --timeout=60s
```

Test:

```bash
curl $(minikube service webapp-service --url)
```

Expected:

```text
Hello from Kubernetes Pod
```

---

# 🔍 Verification

## Verify Cluster

```bash
kubectl get all
```

Check node:

```bash
kubectl get nodes
```

Check components:

```bash
kubectl get componentstatuses
```

---

## Verify Deployments

```bash
kubectl get deployments
```

Expected:

```text
nginx-deployment 5/5
webapp           2/2
```

---

## Verify Services

```bash
kubectl get services
```

Test Nginx:

```bash
curl $(minikube service nginx-service --url)
```

Test WebApp:

```bash
curl $(minikube service webapp-service --url)
```

---

## Verify Pods

Count running pods:

```bash
kubectl get pods --field-selector=status.phase=Running | wc -l
```

Expected:

```text
7
```

(5 nginx + 2 webapp)

---

## Check Resource Usage

Node metrics:

```bash
kubectl top nodes
```

Pod metrics:

```bash
kubectl top pods
```

---

## View Logs

Nginx logs:

```bash
kubectl logs -l app=nginx --tail=20
```

WebApp logs:

```bash
kubectl logs -l app=webapp --tail=20
```

---

# 🛠️ Troubleshooting

## Pods Not Starting

Describe pod:

```bash
kubectl describe pod <POD_NAME>
```

Check logs:

```bash
kubectl logs <POD_NAME>
```

---

## Service Not Accessible

View endpoints:

```bash
kubectl get endpoints
```

Check service:

```bash
kubectl describe service nginx-service
```

List service URLs:

```bash
minikube service list
```

---

## Minikube Problems

Restart:

```bash
minikube stop
minikube start
```

Recreate:

```bash
minikube delete
minikube start --driver=docker
```

---

## Resource Constraints

Inspect node:

```bash
kubectl describe node minikube
```

Check usage:

```bash
kubectl top nodes
kubectl top pods
```

---

# 🧹 Cleanup

Delete deployments:

```bash
kubectl delete deployment nginx-deployment webapp
```

Delete services:

```bash
kubectl delete service nginx-service webapp-service
```

Stop Minikube:

```bash
minikube stop
```

Delete cluster:

```bash
minikube delete
```

---

# 📊 Expected Outcomes

After completing this lab, you should have:

✅ Working Minikube cluster

✅ Kubernetes node in Ready state

✅ Nginx deployment with 5 replicas

✅ WebApp deployment with 2 replicas

✅ NodePort services

✅ Accessible applications

✅ Resource monitoring enabled

---

# 🎓 Key Concepts Learned

## ☸️ Minikube

Local Kubernetes cluster for development and testing.

## 📦 Deployments

Manage pod replicas declaratively.

## 🌐 Services

Provide stable network access to pods.

## 🖥️ kubectl

Primary command-line tool for Kubernetes administration.

## 📈 Scaling

Adjust application capacity dynamically.

---

# 🏢 Real-World Applications

* Microservices Deployment
* Container Orchestration
* Cloud-Native Applications
* CI/CD Pipelines
* High Availability Systems
* Load Balancing
* Rolling Updates & Rollbacks

---

# 🏁 Conclusion

Congratulations! 🎉

You successfully:

* Installed Docker, kubectl, and Minikube
* Created a Kubernetes cluster
* Deployed containerized applications
* Exposed applications through Services
* Scaled deployments dynamically
* Monitored cluster health and resource usage

This lab provides a strong foundation for advanced Kubernetes topics such as:

* ConfigMaps
* Secrets
* Persistent Volumes
* Ingress Controllers
* Helm Charts
* Multi-Node Clusters
* Kubernetes Networking

🚀 You are now ready to continue your Kubernetes and Cloud-Native journey.
