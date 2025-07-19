@echo off
REM Kubernetes Deployment Script for Calculator API (Windows)
REM This script deploys the entire application stack to Kubernetes

echo 🚀 Deploying Calculator API to Kubernetes
echo ==========================================

REM Check if kubectl is installed
kubectl version --client --short >nul 2>&1
if errorlevel 1 (
    echo ❌ kubectl is not installed. Please install kubectl first.
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Build the Docker image
echo 📦 Building Docker image...
docker build -t calculator-api:latest .
if errorlevel 1 (
    echo ❌ Docker build failed
    exit /b 1
)

echo ✅ Docker image built successfully

REM Create namespace
echo 📁 Creating namespace...
kubectl apply -f infrastructure/kubernetes/namespace.yml

REM Apply ConfigMaps and Secrets
echo 🔧 Applying ConfigMaps and Secrets...
kubectl apply -f infrastructure/kubernetes/configmap.yml
kubectl apply -f infrastructure/kubernetes/secret.yml

REM Create PostgreSQL init script ConfigMap
echo 📝 Creating PostgreSQL init script...
kubectl create configmap postgres-init-script --from-file=app/database/init.sql --namespace=calculator-app --dry-run=client -o yaml | kubectl apply -f -

REM Deploy database and cache
echo 🗄️ Deploying PostgreSQL...
kubectl apply -f infrastructure/kubernetes/postgres-deployment.yml

echo 🔴 Deploying Redis...
kubectl apply -f infrastructure/kubernetes/redis-deployment.yml

REM Wait for database to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
kubectl wait --for=condition=ready pod -l app=calculator-postgres -n calculator-app --timeout=300s

echo ⏳ Waiting for Redis to be ready...
kubectl wait --for=condition=ready pod -l app=calculator-redis -n calculator-app --timeout=300s

REM Deploy the API
echo 🚀 Deploying Calculator API...
kubectl apply -f infrastructure/kubernetes/api-deployment.yml

REM Wait for API to be ready
echo ⏳ Waiting for API to be ready...
kubectl wait --for=condition=ready pod -l app=calculator-api -n calculator-app --timeout=300s

REM Deploy monitoring stack
echo 📊 Deploying monitoring stack...
kubectl apply -f infrastructure/kubernetes/monitoring.yml

REM Create Prometheus config
echo 📈 Creating Prometheus configuration...
kubectl create configmap prometheus-config --from-file=monitoring/prometheus/pprometheus.yml --namespace=calculator-app --dry-run=client -o yaml | kubectl apply -f -

REM Create Grafana provisioning
echo 📊 Creating Grafana provisioning...
kubectl create configmap grafana-provisioning --from-file=monitoring/grafana/provisioning/ --namespace=calculator-app --dry-run=client -o yaml | kubectl apply -f -

REM Deploy ingress (optional - requires ingress controller)
echo 🌐 Deploying ingress...
kubectl apply -f infrastructure/kubernetes/ingress.yml

REM Show deployment status
echo 📋 Deployment completed! Checking status...
echo.
kubectl get pods -n calculator-app
echo.
kubectl get services -n calculator-app
echo.
kubectl get ingress -n calculator-app

echo.
echo 🎉 Calculator API deployed to Kubernetes successfully!
echo.
echo 📍 Access URLs:
echo   - API: http://calculator-api.local
echo   - Grafana: http://localhost:3000 (port-forward)
echo   - Prometheus: http://localhost:9090 (port-forward)
echo.
echo 🔗 To port-forward services:
echo   kubectl port-forward -n calculator-app svc/grafana 3000:3000
echo   kubectl port-forward -n calculator-app svc/prometheus 9090:9090
echo.
echo 📈 To check scaling:
echo   kubectl get hpa -n calculator-app
echo   kubectl scale deployment calculator-api --replicas=5 -n calculator-app
echo.
echo 🧪 To test scaling:
echo   powershell -ExecutionPolicy Bypass -File scripts/test-k8s-scaling.ps1 