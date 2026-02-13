# Complete Deployment Script for Windows

This script automates the entire deployment process for the Todo App on Windows with Minikube.

## Prerequisites Check

```powershell
# Check if required tools are installed
Write-Host "Checking prerequisites..." -ForegroundColor Green

# Check for Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✓ Docker is installed" -ForegroundColor Green
    docker --version
} else {
    Write-Host "✗ Docker is not installed" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check for kubectl
if (Get-Command kubectl -ErrorAction SilentlyContinue) {
    Write-Host "✓ kubectl is installed" -ForegroundColor Green
    kubectl version --client
} else {
    Write-Host "✗ kubectl is not installed" -ForegroundColor Red
    Write-Host "Please install kubectl from https://kubernetes.io/docs/tasks/tools/" -ForegroundColor Yellow
    exit 1
}

# Check for minikube
if (Get-Command minikube -ErrorAction SilentlyContinue) {
    Write-Host "✓ minikube is installed" -ForegroundColor Green
    minikube version
} else {
    Write-Host "✗ minikube is not installed" -ForegroundColor Red
    Write-Host "Please install minikube from https://minikube.sigs.k8s.io/docs/start/" -ForegroundColor Yellow
    exit 1
}

# Check for Helm
if (Get-Command helm -ErrorAction SilentlyContinue) {
    Write-Host "✓ Helm is installed" -ForegroundColor Green
    helm version
} else {
    Write-Host "✗ Helm is not installed" -ForegroundColor Red
    Write-Host "Please install Helm from https://helm.sh/docs/intro/install/" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nAll prerequisites are installed!" -ForegroundColor Green
```

## Start Minikube

```powershell
Write-Host "`nStarting Minikube cluster..." -ForegroundColor Green

# Start minikube with sufficient resources
minikube start --memory='4000mb' --cpus=2 --disk-size=10g

# Enable required addons
Write-Host "Enabling required addons..." -ForegroundColor Green
minikube addons enable ingress
minikube addons enable metrics-server

Write-Host "Minikube cluster is ready!" -ForegroundColor Green
```

## Set Docker Environment

```powershell
Write-Host "`nSetting Docker environment to use Minikube..." -ForegroundColor Green

# Set Docker environment to use Minikube's Docker daemon
minikube docker-env | Invoke-Expression
```

## Build Docker Images

```powershell
# Navigate to project root
Set-Location C:\Users\anas0\Desktop\phase_04_kubernetes_todo\todos-app-complete-project\phase_03

Write-Host "`nBuilding Docker images..." -ForegroundColor Green

# Build frontend image
Write-Host "Building frontend image..." -ForegroundColor Cyan
Set-Location .\frontend
docker build -t todo-frontend:latest .

# Build backend image
Write-Host "Building backend image..." -ForegroundColor Cyan
Set-Location ..\backend
docker build -t todo-backend:latest .

# Build agent image
Write-Host "Building agent image..." -ForegroundColor Cyan
Set-Location ..\agent-service
docker build -t todo-agent:latest .

# Return to project root
Set-Location ..

Write-Host "All Docker images built successfully!" -ForegroundColor Green
```

## Deploy Using Kubernetes Manifests

```powershell
Write-Host "`nDeploying to Kubernetes..." -ForegroundColor Green

# Apply secrets first
Write-Host "Applying secrets..." -ForegroundColor Cyan
kubectl apply -f k8s/secrets.yaml

# Apply configmap
Write-Host "Applying configmap..." -ForegroundColor Cyan
kubectl apply -f k8s/configmap.yaml

# Apply PostgreSQL
Write-Host "Applying PostgreSQL..." -ForegroundColor Cyan
kubectl apply -f k8s/postgres-statefulset.yaml

# Wait for PostgreSQL to be ready
Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s

# Apply backend
Write-Host "Applying backend..." -ForegroundColor Cyan
kubectl apply -f k8s/backend-deployment.yaml

# Wait for backend to be ready
Write-Host "Waiting for backend to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=backend --timeout=120s

# Apply agent
Write-Host "Applying agent service..." -ForegroundColor Cyan
kubectl apply -f k8s/agent-deployment.yaml

# Apply frontend
Write-Host "Applying frontend..." -ForegroundColor Cyan
kubectl apply -f k8s/frontend-deployment.yaml

Write-Host "All services deployed successfully!" -ForegroundColor Green
```

## Deploy Using Helm (Alternative Method)

```powershell
Write-Host "`nAlternatively, deploying using Helm..." -ForegroundColor Green

# Navigate to helm directory
Set-Location .\helm

# Install the chart
Write-Host "Installing Helm chart..." -ForegroundColor Cyan
helm install todo-app todo-app/ --values todo-app/values.yaml

Write-Host "Helm deployment completed!" -ForegroundColor Green

# Return to project root
Set-Location ..
```

## Verification

```powershell
Write-Host "`nVerifying deployment..." -ForegroundColor Green

# Check all pods
Write-Host "Checking pods..." -ForegroundColor Cyan
kubectl get pods

# Check all services
Write-Host "Checking services..." -ForegroundColor Cyan
kubectl get services

# Check backend logs
Write-Host "Checking backend logs..." -ForegroundColor Cyan
kubectl logs deployment/backend

Write-Host "`nDeployment verification complete!" -ForegroundColor Green
```

## Access the Application

```powershell
Write-Host "`nAccessing the application..." -ForegroundColor Green

# Get frontend service URL
Write-Host "Frontend URL:" -ForegroundColor Cyan
minikube service frontend --url

Write-Host "`nApplication is now accessible!" -ForegroundColor Green
Write-Host "Frontend: Open the URL shown above in your browser" -ForegroundColor Yellow
Write-Host "Backend: Available at the same domain on port 8000" -ForegroundColor Yellow
Write-Host "Agent: Available internally in the cluster on port 8002" -ForegroundColor Yellow
```

## Troubleshooting Commands

```powershell
# If you encounter issues, try these commands:

# Check cluster status
kubectl cluster-info

# Describe a pod for detailed information
# kubectl describe pod <pod-name>

# Get detailed service information
# kubectl describe service <service-name>

# Tail logs continuously
# kubectl logs deployment/backend -f

# Execute commands in a running pod
# kubectl exec -it <pod-name> -- sh

# Check events for issues
kubectl get events --sort-by='.lastTimestamp'
```

## Cleanup (Optional)

```powershell
# To clean up the deployment:
# 
# Uninstall Helm release
# helm uninstall todo-app
# 
# Or delete all resources manually
# kubectl delete -f k8s/
# 
# Stop minikube
# minikube stop
# 
# Delete minikube cluster (to start fresh)
# minikube delete
```

Write-Host "`nDeployment script completed!" -ForegroundColor Green
Write-Host "Your Todo App is now running on Kubernetes!" -ForegroundColor Magenta
```