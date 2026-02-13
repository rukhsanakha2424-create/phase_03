# Phase 4: Kubernetes Deployment for Todo App

This project contains the complete Kubernetes deployment setup for the Todo App, including Dockerization, Minikube configuration, Helm charts, and AI tool integration.

## Project Structure

```
phase_04_kubernetes_todo/
├── frontend/                 # React/Next.js frontend
│   ├── Dockerfile           # Docker configuration for frontend
│   ├── .dockerignore        # Files to exclude from Docker image
│   └── [existing code]      # Frontend source code
├── backend/                  # FastAPI backend
│   ├── Dockerfile           # Docker configuration for backend
│   ├── .dockerignore        # Files to exclude from Docker image
│   └── [existing code]      # Backend source code
├── agent-service/            # Python agent service
│   ├── Dockerfile           # Docker configuration for agent
│   ├── .dockerignore        # Files to exclude from Docker image
│   └── [existing code]      # Agent source code
├── k8s/                      # Kubernetes manifests
│   ├── postgres-statefulset.yaml    # PostgreSQL database
│   ├── backend-deployment.yaml      # Backend service
│   ├── frontend-deployment.yaml     # Frontend service
│   ├── agent-deployment.yaml        # Agent service
│   ├── configmap.yaml              # Configuration
│   └── secrets.yaml                # Sensitive data
├── helm/                     # Helm charts
│   └── todo-app/             # Main application chart
│       ├── Chart.yaml        # Chart metadata
│       ├── values.yaml       # Default configuration values
│       └── templates/        # Kubernetes manifest templates
├── docker-compose.yml        # Local development setup
├── DEPLOYMENT_GUIDE.md       # Detailed deployment instructions
├── AI_TOOLS_GUIDE.md         # AI tools integration guide
├── DEPLOYMENT_SCRIPT.ps1     # Automated deployment script for Windows
└── README.md                 # This file
```

## Features

### ✅ Dockerization
- Multi-stage builds for optimized images
- Proper .dockerignore files
- Production-ready configurations
- Local development with docker-compose

### ✅ Kubernetes Resources
- StatefulSet for PostgreSQL with persistent storage
- Deployments for all services with health checks
- Services for internal and external communication
- ConfigMaps for configuration data
- Secrets for sensitive information
- Proper resource limits and requests

### ✅ Helm Charts
- Parameterized deployment configurations
- Easy installation and upgrades
- Multiple environment support
- Template-based resource definitions

### ✅ AI Tool Integration
- kubectl-ai for natural language Kubernetes commands
- AI-powered troubleshooting and monitoring
- Automated deployment suggestions

### ✅ Production Ready
- Health checks and readiness probes
- Proper logging and monitoring setup
- Resource optimization
- Security best practices

## Quick Start

### Prerequisites
- Docker Desktop
- Minikube
- kubectl
- Helm
- Windows PowerShell (for Windows users)

### Deployment Steps

1. **Start Minikube**
   ```powershell
   minikube start --memory='4000mb' --cpus=2
   minikube addons enable ingress
   ```

2. **Build Docker Images**
   ```powershell
   # Set Docker environment to use Minikube
   eval $(minikube docker-env)
   
   # Build all images
   cd frontend && docker build -t todo-frontend:latest . && cd ..
   cd backend && docker build -t todo-backend:latest . && cd ..
   cd agent-service && docker build -t todo-agent:latest . && cd ..
   ```

3. **Deploy with Helm**
   ```powershell
   cd helm
   helm install todo-app todo-app/
   ```

4. **Access the Application**
   ```powershell
   minikube service frontend --url
   ```

### Alternative: Automated Deployment
Run the automated deployment script:
```powershell
.\DEPLOYMENT_SCRIPT.ps1
```

## AI Tools Integration

The deployment includes support for AI-powered Kubernetes management:

1. **kubectl-ai**: Natural language Kubernetes commands
   ```bash
   kubectl ai "show me all pods in the todo app"
   kubectl ai "scale the frontend to 3 replicas"
   ```

2. **AI Troubleshooting**: Intelligent issue diagnosis
   ```bash
   kubectl ai "why are the backend pods failing?"
   ```

## Configuration

All configuration is managed through Helm values in `helm/todo-app/values.yaml`. You can override values during installation:

```bash
helm install todo-app helm/todo-app/ --set frontend.replicaCount=2 --set backend.resources.requests.memory=256Mi
```

## Scaling

The application supports horizontal pod autoscaling. Configure in `values.yaml`:

```yaml
frontend:
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 10
    targetCPUUtilizationPercentage: 80
```

## Monitoring and Logging

- View application logs: `kubectl logs deployment/backend`
- Monitor resources: `kubectl top pods`
- View events: `kubectl get events`

## Troubleshooting

Common issues and solutions:

1. **Images not found**: Run `eval $(minikube docker-env)` before building
2. **Services not accessible**: Check NodePort configuration
3. **Database connection errors**: Verify secrets are correctly applied
4. **Pods in CrashLoopBackOff**: Check application logs for errors

For detailed troubleshooting, refer to `DEPLOYMENT_GUIDE.md`.

## Cleanup

To remove the deployment:
```bash
helm uninstall todo-app
minikube delete
```

## Next Steps

1. Integrate with cloud providers (AWS EKS, GKE, AKS)
2. Set up CI/CD pipelines
3. Implement advanced monitoring with Prometheus/Grafana
4. Add service mesh with Istio
5. Implement GitOps with ArgoCD

---

**Note**: This deployment is configured for local development with Minikube. For production environments, adjust resource limits, enable TLS, and configure proper authentication.
```