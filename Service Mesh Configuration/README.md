# ☸️ Service Mesh Configuration (Istio on Kubernetes)

![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-blue?style=for-the-badge\&logo=kubernetes)
![Istio](https://img.shields.io/badge/Istio-Service_Mesh-1A1A1A?style=for-the-badge\&logo=istio)
![Minikube](https://img.shields.io/badge/Minikube-Local_Cluster-orange?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu)

---

# 🚀 Service Mesh Configuration (Istio Lab)

## 📖 Overview

A **service mesh** is a dedicated infrastructure layer that manages service-to-service communication in microservices architectures.

In this lab, you will install **Istio on Kubernetes (Minikube)** and configure advanced traffic routing features such as:

* Sidecar injection
* VirtualServices
* DestinationRules
* Traffic splitting
* Header-based routing

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

✔ Install and configure Istio on Kubernetes
✔ Enable automatic sidecar injection
✔ Deploy microservices with Istio proxies
✔ Configure traffic routing using VirtualServices
✔ Implement canary-style traffic splitting
✔ Apply header-based routing rules

---

# 📋 Prerequisites

Before starting, ensure you have:

* Basic Kubernetes knowledge (Pods, Services, Deployments)
* YAML configuration experience
* Linux command-line familiarity
* Understanding of microservices architecture
* Minimum system requirements:

  * 4GB RAM
  * 2 CPU cores

---

# 🛠️ Environment Setup

---

## 🔧 Step 1: Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s \
https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

---

## 🧪 Step 2: Install Minikube

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## 🧭 Step 3: Install Istioctl

```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
cd ..
```

---

## 🚀 Step 4: Start Kubernetes Cluster

```bash
minikube start --memory=4096 --cpus=2 --driver=docker
```

Verify cluster:

```bash
kubectl cluster-info
kubectl get nodes
```

---

# 🧩 Task 1: Install and Configure Istio

---

## ⚙️ Step 1: Install Istio

```bash
istioctl install --set profile=demo -y
```

Verify:

```bash
kubectl get pods -n istio-system
```

---

## 📦 Step 2: Enable Sidecar Injection

```bash
kubectl create namespace microservices
kubectl label namespace microservices istio-injection=enabled
```

Verify:

```bash
kubectl get namespace microservices --show-labels
```

---

## 🚀 Step 3: Deploy Microservices (v1)

### 📄 app-v1.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: microservices
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-v1
  namespace: microservices
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
      version: v1
  template:
    metadata:
      labels:
        app: frontend
        version: v1
    spec:
      containers:
      - name: frontend
        image: hashicorp/http-echo
        args:
        - "-text=Frontend v1"
        - "-listen=:8080"
        ports:
        - containerPort: 8080
```

Apply:

```bash
kubectl apply -f app-v1.yaml
```

---

## 🔍 Verify Pods

```bash
kubectl get pods -n microservices
```

Check sidecars:

```bash
kubectl get pods -n microservices \
-o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
```

---

## 🚀 Step 4: Deploy Backend v2

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-v2
  namespace: microservices
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
      version: v2
  template:
    metadata:
      labels:
        app: backend
        version: v2
    spec:
      containers:
      - name: backend
        image: hashicorp/http-echo
        args:
        - "-text=Backend v2 - New Features!"
        - "-listen=:8080"
        ports:
        - containerPort: 8080
```

---

# 🌐 Task 2: Traffic Routing Configuration

---

## 🚪 Step 1: Gateway

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: microservices-gateway
  namespace: microservices
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
```

---

## 📦 Step 2: Destination Rules

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: backend-destination
  namespace: microservices
spec:
  host: backend
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

---

## 🔀 Step 3: Virtual Service (Traffic Splitting)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend-route
  namespace: microservices
spec:
  hosts:
  - backend
  http:

  - match:
    - headers:
        user-type:
          exact: premium
    route:
    - destination:
        host: backend
        subset: v2

  - route:
    - destination:
        host: backend
        subset: v1
      weight: 90
    - destination:
        host: backend
        subset: v2
      weight: 10
```

Apply:

```bash
kubectl apply -f virtual-service.yaml
```

---

# 🧪 Step 4: Test Traffic Routing

## 🌍 Get Gateway URL

```bash
export INGRESS_HOST=$(minikube ip)
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway \
-o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')

export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
echo "Gateway: http://$GATEWAY_URL"
```

---

## 🔁 Test Load Balancing

```bash
for i in {1..10}; do curl -s http://$GATEWAY_URL; echo ""; done
```

---

## 🎯 Header Routing Test

```bash
curl -H "user-type: premium" http://$GATEWAY_URL
```

---

# 🧪 Advanced Routing Exercise

## 🧠 Task: Create Advanced VirtualService

Implement:

* `/api/v1` → backend-v1
* `/api/v2` → backend-v2
* Default → 50/50 split

---

### Template

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend-advanced-route
  namespace: microservices
spec:
  hosts:
  - backend
  http:

  - match:
    - uri:
        prefix: /api/v1
    route:
    - destination:
        host: backend
        subset: v1

  - match:
    - uri:
        prefix: /api/v2
    route:
    - destination:
        host: backend
        subset: v2

  - route:
    - destination:
        host: backend
        subset: v1
      weight: 50
    - destination:
        host: backend
        subset: v2
      weight: 50
```

---

# ✅ Verification

---

## ✔ Check Istio System

```bash
kubectl get pods -n istio-system
istioctl version
```

---

## ✔ Check Sidecars

```bash
kubectl get pods -n microservices
```

Expected:
✔ app container + istio-proxy container

---

## ✔ Validate Traffic Split

```bash
for i in {1..20}; do curl -s http://$GATEWAY_URL; done
```

---

## ✔ Analyze Configuration

```bash
istioctl analyze -n microservices
```

---

# ⚠️ Troubleshooting

---

## ❌ Pods Not Running

```bash
minikube status
kubectl describe pod <pod-name>
```

---

## ❌ Sidecar Not Injected

```bash
kubectl get namespace microservices --show-labels
kubectl rollout restart deployment -n microservices
```

---

## ❌ Traffic Not Routing

```bash
kubectl get virtualservice -n microservices
kubectl get gateway -n microservices
```

---

## ❌ Gateway Not Accessible

```bash
kubectl get svc -n istio-system
kubectl get pods -n istio-system
```

---

# 🎓 Conclusion

You have successfully:

✔ Installed Istio service mesh
✔ Deployed microservices on Kubernetes
✔ Enabled automatic sidecar injection
✔ Configured VirtualService and DestinationRules
✔ Implemented traffic splitting and routing

---

# 💡 Key Takeaways

✔ Service mesh enables **transparent traffic management**
✔ Istio decouples networking logic from application code
✔ VirtualService enables powerful routing rules
✔ Sidecars provide observability and control

---

# 🚀 Next Steps

* Implement circuit breaking
* Add retries and timeouts
* Enable mTLS security
* Explore Istio observability (Kiali, Prometheus)
* Try canary deployments in production-like setup

---

# 🧹 Cleanup

```bash
kubectl delete namespace microservices
istioctl uninstall --purge -y
minikube stop
minikube delete
```

---

## 🎯 Lab Completed Successfully

**Istio Service Mesh Configuration Mastery**
