# AI Tools Integration Guide

This guide explains how to integrate AI-powered tools with your Kubernetes deployment.

## kubectl-ai Installation

kubectl-ai is an AI-powered plugin for kubectl that helps with Kubernetes commands using natural language.

### Installation:

```bash
# For Windows (using PowerShell as Administrator)
curl -LO https://github.com/sozercan/kubectl-ai/releases/latest/download/kubectl-ai_windows_amd64.tar.gz
tar -xzf kubectl-ai_windows_amd64.tar.gz
mv kubectl-ai.exe $HOME\.krew\bin\  # If using krew
# OR
mv kubectl-ai.exe $HOME\.kube\plugin\  # If using kubectl plugins directory
```

### Configuration:

```bash
# Set OpenAI API key (or Azure OpenAI)
export OPENAI_API_KEY="your-api-key-here"

# Or for Azure OpenAI
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_MODEL="gpt-35-turbo"  # or gpt-4
```

### Example Commands for Todo App:

```bash
# Get all pods in the todo app namespace
kubectl ai "show me all pods in the todo app"

# Describe the backend deployment
kubectl ai "describe the backend deployment"

# Find pods with high CPU usage
kubectl ai "find pods with high CPU usage in the todo app"

# Get logs from the backend
kubectl ai "get logs from the backend deployment"

# Scale the frontend deployment
kubectl ai "scale the frontend deployment to 3 replicas"

# Debug why pods are failing
kubectl ai "why are the backend pods failing?"

# Create a port forward to the frontend
kubectl ai "forward port 3000 to the frontend service"
```

## kagent Installation

kagent is a Kubernetes automation agent that can help manage your deployments.

### Installation:

```bash
# Clone the kagent repository (if available)
# Since kagent might be a custom solution, you may need to build it yourself
git clone https://github.com/your-org/kagent.git
cd kagent
make build
```

### Configuration for Todo App:

```yaml
# kagent-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kagent-config
data:
  config.yaml: |
    rules:
      - name: "auto-scale-frontend"
        condition: "cpu_usage > 70%"
        action: "scale_deployment(frontend, +1)"
      
      - name: "restart-failing-pods"
        condition: "pod_failed > 0"
        action: "restart_pods_with_label(app=frontend)"
      
      - name: "backup-database"
        schedule: "0 2 * * *"  # Daily at 2 AM
        action: "backup_postgres(postgres, /backups/tododb-$(date +%Y%m%d))"
```

## AI-Powered Monitoring

### Using AI for Log Analysis:

```bash
# Monitor logs with AI insights
kubectl ai "monitor logs from backend and alert me if there are errors"

# Analyze performance
kubectl ai "analyze the performance of the todo app and suggest optimizations"
```

## AI Troubleshooting Examples

```bash
# Diagnose common issues
kubectl ai "diagnose why the frontend can't connect to the backend"

# Resource optimization
kubectl ai "suggest optimal resource limits for the todo app deployments"

# Security recommendations
kubectl ai "review the security of my todo app deployments and suggest improvements"

# Performance tuning
kubectl ai "analyze the todo app performance and recommend scaling policies"
```

## Integration with CI/CD

You can integrate kubectl-ai into your CI/CD pipelines for automated deployments:

```yaml
# Example GitHub Actions workflow
name: Deploy with AI Assistance
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2
      
    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      
    - name: Setup kubectl-ai
      run: |
        curl -LO https://github.com/sozercan/kubectl-ai/releases/latest/download/kubectl-ai_linux_amd64.tar.gz
        tar -xzf kubectl-ai_linux_amd64.tar.gz
        sudo mv kubectl-ai /usr/local/bin/
        
    - name: Deploy with AI assistance
      run: |
        export OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
        kubectl ai "deploy the todo app from the current directory"
```

## Best Practices

1. **Secure API Keys**: Never hardcode API keys in configuration files
2. **Monitor Costs**: AI services can incur costs, monitor usage regularly
3. **Validate Outputs**: Always verify AI-generated commands before execution
4. **Combine with Traditional Tools**: Use AI tools to augment, not replace, traditional Kubernetes knowledge
5. **Document AI Usage**: Keep records of AI-assisted decisions for audit purposes
```