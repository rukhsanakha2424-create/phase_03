# Kubernetes Deployment Guide for Todo App

This guide explains how to deploy the Todo App to a local Kubernetes cluster using Minikube.

## Prerequisites

Before starting, ensure you have the following installed:

- Docker Desktop (with Kubernetes disabled if using Minikube)
- Minikube
- kubectl
- Helm
- kubectl-ai (optional)
- Windows Subsystem for Linux (WSL2) recommended for Windows users

## Installation Steps

### 1. Install Minikube

For Windows:
```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install minikube using Chocolatey
choco install minikube

# Or install using the binary directly
New-Item -Path 'c:\' -Name 'temp' -ItemType Directory -Force
Invoke-WebRequest -OutFile 'c:\temp\minikube-windows-amd64.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing
Move-Item c:\temp\minikube-windows-amd64.exe c:\minikube.exe
```

### 2. Start Minikube Cluster

```bash
# Start minikube with sufficient resources
minikube start --memory='4000mb' --cpus=2

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 3. Build Docker Images

```bash
# Set Docker environment to use Minikube's Docker daemon
eval $(minikube docker-env)

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .

# Build backend image
cd ../backend
docker build -t todo-backend:latest .

# Build agent image
cd ../agent-service
docker build -t todo-agent:latest .

# Return to project root
cd ..
```

### 4. Deploy Using Kubernetes Manifests

```bash
# Apply secrets first
kubectl apply -f k8s/secrets.yaml

# Apply configmap
kubectl apply -f k8s/configmap.yaml

# Apply PostgreSQL
kubectl apply -f k8s/postgres-statefulset.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s

# Apply backend
kubectl apply -f k8s/backend-deployment.yaml

# Wait for backend to be ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=120s

# Apply agent
kubectl apply -f k8s/agent-deployment.yaml

# Apply frontend
kubectl apply -f k8s/frontend-deployment.yaml
```

### 5. Deploy Using Helm Charts

```bash
# Navigate to helm directory
cd helm

# Install the chart
helm install todo-app todo-app/ --values todo-app/values.yaml

# Or upgrade if already installed
helm upgrade todo-app todo-app/ --values todo-app/values.yaml
```

### 6. Access the Application

```bash
# Get the frontend service URL
minikube service frontend --url

# Or access via dashboard
minikube dashboard
```

## Verification Commands

```bash
# Check all pods
kubectl get pods

# Check all services
kubectl get services

# Check logs for a specific pod
kubectl logs deployment/backend

# Port forward to access locally
kubectl port-forward svc/frontend 3000:80
```

## Troubleshooting

### Common Issues:

1. **Images not found**: Make sure to run `eval $(minikube docker-env)` before building images
2. **Pods stuck in Pending state**: Check resource limits and increase Minikube resources
3. **Database connection errors**: Verify secrets are correctly applied
4. **Service not accessible**: Check if NodePort is properly configured

### Useful Commands:

```bash
# Check cluster status
kubectl cluster-info

# Describe a pod for detailed information
kubectl describe pod <pod-name>

# Get detailed service information
kubectl describe service <service-name>

# Tail logs continuously
kubectl logs deployment/backend -f

# Execute commands in a running pod
kubectl exec -it <pod-name> -- sh
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app

# Or delete all resources manually
kubectl delete -f k8s/

# Stop minikube
minikube stop

# Delete minikube cluster (to start fresh)
minikube delete
```