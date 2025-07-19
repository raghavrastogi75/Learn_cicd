# ☸️ Kubernetes Deployment Guide

## Overview

This guide will help you deploy your Calculator API to Kubernetes with **production-grade features**:
- **Horizontal Pod Autoscaling** (HPA)
- **Load Balancing** across multiple replicas
- **Persistent Storage** for databases
- **Health Checks** and monitoring
- **Resource Management** and limits
- **Ingress** for external access

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ingress       │    │   Load Balancer │    │   API Pods      │
│   (nginx)       │───▶│   (Service)     │───▶│   (3-10 replicas)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                       ┌─────────────────┐            │
                       │   PostgreSQL    │◀───────────┘
                       │   (StatefulSet) │
                       └─────────────────┘
                                                       │
                       ┌─────────────────┐            │
                       │   Redis         │◀───────────┘
                       │   (Deployment)  │
                       └─────────────────┘
```

## 📋 Prerequisites

### 1. Install Required Tools
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Docker Desktop (includes Kubernetes)
# Download from: https://www.docker.com/products/docker-desktop

# Install Minikube (alternative)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### 2. Start Kubernetes Cluster
```bash
# Option 1: Docker Desktop Kubernetes
# Enable Kubernetes in Docker Desktop settings

# Option 2: Minikube
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Option 3: Kind (Kubernetes in Docker)
kind create cluster --name calculator-cluster
```

## 🚀 Quick Deployment

### 1. Build and Deploy
```bash
# Make script executable
chmod +x scripts/deploy-to-k8s.sh

# Run deployment
./scripts/deploy-to-k8s.sh
```

### 2. Verify Deployment
```bash
# Check all resources
kubectl get all -n calculator-app

# Check pods status
kubectl get pods -n calculator-app

# Check services
kubectl get services -n calculator-app

# Check ingress
kubectl get ingress -n calculator-app
```

## 📊 Scaling Features

### 1. Horizontal Pod Autoscaling (HPA)
Your API automatically scales based on:
- **CPU Usage**: Scales up when >70% CPU
- **Memory Usage**: Scales up when >80% memory
- **Min Replicas**: 2 (for high availability)
- **Max Replicas**: 10 (to control costs)

```bash
# Check HPA status
kubectl get hpa -n calculator-app

# View HPA details
kubectl describe hpa calculator-api-hpa -n calculator-app
```

### 2. Manual Scaling
```bash
# Scale to 5 replicas
kubectl scale deployment calculator-api --replicas=5 -n calculator-app

# Scale to 1 replica
kubectl scale deployment calculator-api --replicas=1 -n calculator-app
```

### 3. Load Testing
```bash
# Generate traffic to test scaling
python scripts/generate_traffic.py

# Monitor scaling in real-time
kubectl get pods -n calculator-app -w
```

## 🔍 Monitoring and Access

### 1. Port Forwarding
```bash
# Access Grafana
kubectl port-forward -n calculator-app svc/grafana 3000:3000

# Access Prometheus
kubectl port-forward -n calculator-app svc/prometheus 9090:9090

# Access API directly
kubectl port-forward -n calculator-app svc/calculator-api 8080:80
```

### 2. Ingress Access
```bash
# Add to /etc/hosts (Linux/Mac)
echo "127.0.0.1 calculator-api.local" | sudo tee -a /etc/hosts

# Windows: Edit C:\Windows\System32\drivers\etc\hosts
# Add: 127.0.0.1 calculator-api.local
```

### 3. API Testing
```bash
# Test API health
curl http://calculator-api.local/health

# Test calculator endpoint
curl -X POST http://calculator-api.local/api/calculator/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 5, "b": 3}'
```

## 🛠️ Advanced Operations

### 1. Rolling Updates
```bash
# Update image
kubectl set image deployment/calculator-api api=calculator-api:v2 -n calculator-app

# Check rollout status
kubectl rollout status deployment/calculator-api -n calculator-app

# Rollback if needed
kubectl rollout undo deployment/calculator-api -n calculator-app
```

### 2. Resource Management
```bash
# Check resource usage
kubectl top pods -n calculator-app

# Check node resources
kubectl top nodes

# View resource limits
kubectl describe deployment calculator-api -n calculator-app
```

### 3. Logs and Debugging
```bash
# View API logs
kubectl logs -f deployment/calculator-api -n calculator-app

# View specific pod logs
kubectl logs -f <pod-name> -n calculator-app

# Execute commands in pods
kubectl exec -it <pod-name> -n calculator-app -- /bin/bash
```

## 🔧 Configuration Management

### 1. Environment Variables
```bash
# Update ConfigMap
kubectl edit configmap calculator-config -n calculator-app

# Update Secrets
kubectl edit secret calculator-secrets -n calculator-app
```

### 2. Scaling Policies
```bash
# Edit HPA behavior
kubectl edit hpa calculator-api-hpa -n calculator-app
```

### 3. Resource Limits
```bash
# Edit deployment resource limits
kubectl edit deployment calculator-api -n calculator-app
```

## 📈 Performance Optimization

### 1. Resource Tuning
```yaml
# Recommended resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### 2. Scaling Behavior
```yaml
# Aggressive scale-up, conservative scale-down
behavior:
  scaleUp:
    stabilizationWindowSeconds: 60
    policies:
    - type: Percent
      value: 100
      periodSeconds: 15
  scaleDown:
    stabilizationWindowSeconds: 300
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60
```

### 3. Health Check Optimization
```yaml
# Fast startup, reliable health checks
startupProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 30
```

## 🚨 Troubleshooting

### 1. Common Issues
```bash
# Pods not starting
kubectl describe pod <pod-name> -n calculator-app

# Services not accessible
kubectl describe service calculator-api -n calculator-app

# Ingress not working
kubectl describe ingress calculator-ingress -n calculator-app
```

### 2. Database Issues
```bash
# Check PostgreSQL logs
kubectl logs -f deployment/calculator-postgres -n calculator-app

# Connect to database
kubectl exec -it <postgres-pod> -n calculator-app -- psql -U postgres -d calculator_db
```

### 3. Scaling Issues
```bash
# Check HPA events
kubectl describe hpa calculator-api-hpa -n calculator-app

# Check metrics server
kubectl get apiservice v1beta1.metrics.k8s.io
```

## 🧹 Cleanup

### 1. Remove Application
```bash
# Delete all resources
kubectl delete namespace calculator-app

# Or delete individually
kubectl delete -f infrastructure/kubernetes/
```

### 2. Clean Docker Images
```bash
# Remove local images
docker rmi calculator-api:latest

# Clean up unused resources
docker system prune -a
```

## 🎯 Production Considerations

### 1. Security
- Use **RBAC** for access control
- Implement **Network Policies**
- Use **Pod Security Standards**
- Enable **Audit Logging**

### 2. Monitoring
- Set up **AlertManager** for notifications
- Configure **Service Mesh** (Istio/Linkerd)
- Implement **Distributed Tracing**
- Use **Centralized Logging** (ELK Stack)

### 3. Backup and Recovery
- Regular **Database Backups**
- **Volume Snapshots**
- **Disaster Recovery** plan
- **Multi-region** deployment

## 🎉 Congratulations!

You now have a **production-ready Kubernetes deployment** with:
- ✅ **Auto-scaling** based on load
- ✅ **High availability** with multiple replicas
- ✅ **Persistent storage** for data
- ✅ **Health monitoring** and alerts
- ✅ **Load balancing** across pods
- ✅ **Resource management** and limits

This is exactly how **enterprise applications** are deployed and scaled in production! 🚀

## 🚀 Next Steps

1. **Set up CI/CD Pipeline** - Automate deployments
2. **Add Service Mesh** - Advanced networking
3. **Implement Security** - RBAC and policies
4. **Multi-cluster** - High availability across regions 