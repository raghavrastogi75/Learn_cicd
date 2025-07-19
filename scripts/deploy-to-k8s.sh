#!/bin/bash

# Kubernetes Deployment Script for Calculator API
# This script deploys the entire application stack to Kubernetes

set -e

echo "🚀 Deploying Calculator API to Kubernetes"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Build the Docker image
print_status "Building Docker image..."
docker build -t calculator-api:latest .

print_success "Docker image built successfully"

# Create namespace
print_status "Creating namespace..."
kubectl apply -f infrastructure/kubernetes/namespace.yml

# Apply ConfigMaps and Secrets
print_status "Applying ConfigMaps and Secrets..."
kubectl apply -f infrastructure/kubernetes/configmap.yml
kubectl apply -f infrastructure/kubernetes/secret.yml

# Create PostgreSQL init script ConfigMap
print_status "Creating PostgreSQL init script..."
kubectl create configmap postgres-init-script \
    --from-file=app/database/init.sql \
    --namespace=calculator-app \
    --dry-run=client -o yaml | kubectl apply -f -

# Deploy database and cache
print_status "Deploying PostgreSQL..."
kubectl apply -f infrastructure/kubernetes/postgres-deployment.yml

print_status "Deploying Redis..."
kubectl apply -f infrastructure/kubernetes/redis-deployment.yml

# Wait for database to be ready
print_status "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=calculator-postgres -n calculator-app --timeout=300s

print_status "Waiting for Redis to be ready..."
kubectl wait --for=condition=ready pod -l app=calculator-redis -n calculator-app --timeout=300s

# Deploy the API
print_status "Deploying Calculator API..."
kubectl apply -f infrastructure/kubernetes/api-deployment.yml

# Wait for API to be ready
print_status "Waiting for API to be ready..."
kubectl wait --for=condition=ready pod -l app=calculator-api -n calculator-app --timeout=300s

# Deploy monitoring stack
print_status "Deploying monitoring stack..."
kubectl apply -f infrastructure/kubernetes/monitoring.yml

# Create Prometheus config
print_status "Creating Prometheus configuration..."
kubectl create configmap prometheus-config \
    --from-file=monitoring/prometheus/prometheus.yml \
    --namespace=calculator-app \
    --dry-run=client -o yaml | kubectl apply -f -

# Create Grafana provisioning
print_status "Creating Grafana provisioning..."
kubectl create configmap grafana-provisioning \
    --from-file=monitoring/grafana/provisioning/ \
    --namespace=calculator-app \
    --dry-run=client -o yaml | kubectl apply -f -

# Deploy ingress (optional - requires ingress controller)
print_status "Deploying ingress..."
kubectl apply -f infrastructure/kubernetes/ingress.yml

# Show deployment status
print_status "Deployment completed! Checking status..."
echo ""
kubectl get pods -n calculator-app
echo ""
kubectl get services -n calculator-app
echo ""
kubectl get ingress -n calculator-app

print_success "🎉 Calculator API deployed to Kubernetes successfully!"
echo ""
print_status "Access URLs:"
echo "  - API: http://calculator-api.local"
echo "  - Grafana: http://localhost:3000 (port-forward)"
echo "  - Prometheus: http://localhost:9090 (port-forward)"
echo ""
print_status "To port-forward services:"
echo "  kubectl port-forward -n calculator-app svc/grafana 3000:3000"
echo "  kubectl port-forward -n calculator-app svc/prometheus 9090:9090"
echo ""
print_status "To check scaling:"
echo "  kubectl get hpa -n calculator-app"
echo "  kubectl scale deployment calculator-api --replicas=5 -n calculator-app" 