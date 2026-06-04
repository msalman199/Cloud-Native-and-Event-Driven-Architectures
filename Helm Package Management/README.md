# 🚀 Helm Package Management 

<p align="center">

![Helm](https://img.shields.io/badge/Helm-v3-blue?style=for-the-badge&logo=helm)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Cluster-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-Configuration-red?style=for-the-badge&logo=yaml)
![Linux](https://img.shields.io/badge/Linux-Terminal-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![kubectl](https://img.shields.io/badge/kubectl-CLI-326CE5?style=for-the-badge&logo=kubernetes)

</p>

---

# 📦 Helm Package Management

## 📖 Overview

Helm is the package manager for Kubernetes. It simplifies application deployment by providing reusable templates, versioning, configuration management, and release lifecycle operations.

In this lab, you will learn how to create, deploy, manage, upgrade, rollback, and package Helm charts.

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

✅ Basic understanding of Kubernetes concepts (Pods, Services, Deployments)

✅ Familiarity with YAML syntax

✅ Linux command-line experience

✅ Running Kubernetes cluster (Minikube or Kind)

✅ kubectl installed and configured

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

✅ Understand Helm chart structure and components

✅ Create a custom Helm chart from scratch

✅ Deploy applications using Helm releases

✅ Manage Helm releases (Install, Upgrade, Rollback)

✅ Use Helm templating features

---

# 🛠️ Environment Setup

---

## 🔹 Step 1: Install Helm

### Install Helm

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Verify Installation

```bash
helm version
```

Expected Output:

```bash
version.BuildInfo{Version:"v3.x.x"}
```

---

## 🔹 Step 2: Start Kubernetes Cluster

### Using Minikube

```bash
minikube start --driver=docker
```

### Using Kind

```bash
kind create cluster --name helm-lab
```

### Verify Cluster

```bash
kubectl cluster-info
kubectl get nodes
```

---

## 🔹 Step 3: Add Helm Repository (Optional)

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update
```

Verify repositories:

```bash
helm repo list
```

---

# 🧪 Task 1: Create a Custom Helm Chart

---

## 🔹 Step 1: Generate Chart Structure

Create a new chart:

```bash
helm create mywebapp
```

Navigate to chart:

```bash
cd mywebapp
```

View structure:

```bash
tree .
```

Expected Structure:

```text
mywebapp/
├── Chart.yaml
├── values.yaml
├── charts/
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── _helpers.tpl
    └── tests/
```

---

## 🔹 Step 2: Modify Chart Metadata

Edit:

```bash
vim Chart.yaml
```

Replace contents:

```yaml
apiVersion: v2
name: mywebapp
description: A simple web application Helm chart
type: application
version: 0.1.0
appVersion: "1.0"

maintainers:
  - name: Your Name
    email: your.email@example.com
```

---

## 🔹 Step 3: Configure values.yaml

Edit:

```bash
vim values.yaml
```

Configuration:

```yaml
replicaCount: 2

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.25-alpine"

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi

# TODO:
# Environment Variables
# ConfigMap Data
# Additional Labels
```

---

## 🔹 Step 4: Customize Deployment Template

Edit:

```bash
vim templates/deployment.yaml
```

Example:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: {{ include "mywebapp.fullname" . }}

  labels:
    {{- include "mywebapp.labels" . | nindent 4 }}

spec:
  replicas: {{ .Values.replicaCount }}

  selector:
    matchLabels:
      {{- include "mywebapp.selectorLabels" . | nindent 6 }}

  template:
    metadata:
      labels:
        {{- include "mywebapp.selectorLabels" . | nindent 8 }}

    spec:
      containers:
      - name: {{ .Chart.Name }}

        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"

        imagePullPolicy: {{ .Values.image.pullPolicy }}

        ports:
        - name: http
          containerPort: 80
          protocol: TCP

        # TODO:
        # Environment Variables
        # Resource Limits
        # Readiness Probes
        # Liveness Probes
```

---

## 🔹 Step 5: Create ConfigMap Template

Create file:

```bash
touch templates/configmap.yaml
```

Contents:

```yaml
apiVersion: v1
kind: ConfigMap

metadata:
  name: {{ include "mywebapp.fullname" . }}-config

  labels:
    {{- include "mywebapp.labels" . | nindent 4 }}

data:

  index.html: |
    <!DOCTYPE html>
    <html>
    <head>
      <title>{{ .Chart.Name }}</title>
    </head>

    <body>
      <h1>Welcome to {{ .Chart.Name }}</h1>
      <p>Version: {{ .Chart.AppVersion }}</p>
    </body>
    </html>
```

---

## 🔹 Step 6: Validate Chart

Lint Chart:

```bash
helm lint .
```

Dry Run:

```bash
helm install mywebapp . --dry-run --debug
```

Render Templates:

```bash
helm template mywebapp .
```

---

# 🚀 Task 2: Deploy and Manage Helm Releases

---

## 🔹 Step 1: Install Release

```bash
helm install mywebapp-release ./mywebapp
```

List Releases:

```bash
helm list
```

Check Deployment:

```bash
kubectl get all -l app.kubernetes.io/name=mywebapp
```

---

## 🔹 Step 2: Verify Deployment

Release Status:

```bash
helm status mywebapp-release
```

Release Values:

```bash
helm get values mywebapp-release
```

View Manifest:

```bash
helm get manifest mywebapp-release
```

Check Resources:

```bash
kubectl get pods
kubectl get svc
```

Port Forward:

```bash
kubectl port-forward svc/mywebapp-release 8080:80
```

Open:

```text
http://localhost:8080
```

---

## 🔹 Step 3: Upgrade Release

Modify values.yaml:

```yaml
replicaCount: 3
```

Upgrade:

```bash
helm upgrade mywebapp-release ./mywebapp
```

View History:

```bash
helm history mywebapp-release
```

Verify:

```bash
kubectl get pods -l app.kubernetes.io/name=mywebapp
```

---

## 🔹 Step 4: Rollback Release

Rollback:

```bash
helm rollback mywebapp-release 1
```

Verify:

```bash
helm history mywebapp-release

kubectl get pods -l app.kubernetes.io/name=mywebapp
```

---

## 🔹 Step 5: Override Values During Install

Create custom values:

```bash
cat > custom-values.yaml <<EOF
replicaCount: 4

image:
  tag: "1.24-alpine"

service:
  type: NodePort
  port: 8080
EOF
```

Install:

```bash
helm install mywebapp-custom ./mywebapp -f custom-values.yaml
```

Inline Values:

```bash
helm install mywebapp-inline ./mywebapp \
--set replicaCount=5
```

---

## 🔹 Step 6: Package and Share Chart

Package Chart:

```bash
helm package ./mywebapp
```

Generated Package:

```text
mywebapp-0.1.0.tgz
```

Install Package:

```bash
helm install mywebapp-from-pkg ./mywebapp-0.1.0.tgz
```

Generate Repository Index:

```bash
helm repo index .
```

---

# ✅ Verification

---

## 🔍 Verify Chart Creation

```bash
ls -la mywebapp/

helm lint mywebapp/
```

Expected:

```text
No errors or warnings
```

---

## 🔍 Verify Deployment

```bash
helm list --all-namespaces
```

```bash
kubectl get pods \
-l app.kubernetes.io/name=mywebapp
```

```bash
kubectl get svc \
-l app.kubernetes.io/name=mywebapp
```

```bash
helm get all mywebapp-release
```

---

## 🔍 Verify Upgrade & Rollback

```bash
helm history mywebapp-release
```

Expected:

```text
REVISION STATUS DESCRIPTION
1        deployed Install complete
2        deployed Upgrade complete
3        deployed Rollback complete
```

---

## 🔍 Test Application Access

```bash
kubectl port-forward svc/mywebapp-release 8080:80 &
```

```bash
curl http://localhost:8080
```

Expected Output:

```html
<!DOCTYPE html>
<html>
...
Welcome to mywebapp
...
</html>
```

---

# 🛠️ Troubleshooting

---

## ❌ Chart Validation Fails

```bash
helm lint mywebapp/ --debug
```

Validate Templates:

```bash
helm template mywebapp mywebapp/ --debug
```

---

## ❌ Release Installation Fails

Detailed Logs:

```bash
helm install mywebapp-release ./mywebapp --debug
```

Kubernetes Events:

```bash
kubectl get events --sort-by='.lastTimestamp'
```

---

## ❌ Pods Not Starting

View Logs:

```bash
kubectl logs -l app.kubernetes.io/name=mywebapp
```

Describe Pod:

```bash
kubectl describe pod <pod-name>
```

---

## ❌ Template Rendering Issues

```bash
helm template mywebapp ./mywebapp \
--set replicaCount=3 \
--debug
```

---

# 🧹 Cleanup

Remove Releases:

```bash
helm uninstall mywebapp-release

helm uninstall mywebapp-custom

helm uninstall mywebapp-inline

helm uninstall mywebapp-from-pkg
```

Verify:

```bash
helm list

kubectl get all
```

Stop Cluster:

### Minikube

```bash
minikube stop
```

### Kind

```bash
kind delete cluster --name helm-lab
```

---

# 🎓 Conclusion

In this lab you successfully:

✅ Created a custom Helm chart

✅ Configured chart metadata and values

✅ Used Helm templating

✅ Installed Helm releases

✅ Upgraded applications

✅ Rolled back releases

✅ Packaged charts for distribution

✅ Managed application lifecycle using Helm

Helm provides a powerful way to deploy, version, configure, and manage Kubernetes applications. Mastering Helm is an essential skill for Kubernetes administrators, DevOps engineers, Cloud engineers, and Platform engineers.

---

# 🚀 Next Steps

### 🔹 Helm Hooks

Learn pre-install and post-install automation.

### 🔹 Chart Dependencies

Manage subcharts and complex applications.

### 🔹 Chart Repositories

Publish and distribute internal charts.

### 🔹 Advanced Templating

Use:

- if conditions
- loops
- variables
- functions

### 🔹 Helm Security

Study:

- Signed charts
- Secrets management
- RBAC best practices
- Supply chain security

---

# 🏆 Lab Completed Successfully

```text
✔ Helm Installed
✔ Kubernetes Cluster Running
✔ Chart Created
✔ Release Installed
✔ Upgrade Tested
✔ Rollback Tested
✔ Package Generated
✔ Cleanup Completed
```

🎉 Congratulations! You have completed the Helm Package Management Lab.
