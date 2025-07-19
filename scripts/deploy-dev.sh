#!/bin/bash

# Development Environment Deployment Script
set -e

echo "🚀 Deploying to Development Environment..."

# Environment variables
export ENVIRONMENT="development"
export NAMESPACE="calculator-dev"
export IMAGE_TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Environment: Development${NC}"
echo -e "${BLUE}📋 Namespace: $NAMESPACE${NC}"
echo -e "${BLUE}📋 Image Tag: $IMAGE_TAG${NC}"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed${NC}"
    exit 1
fi

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

echo -e "${YELLOW}🔧 Building Docker image...${NC}"
docker build -t calculator-api:dev .

echo -e "${YELLOW}🔧 Creating development namespace and configs...${NC}"
kubectl apply -f infrastructure/kubernetes/namespace-dev.yml

echo -e "${YELLOW}🔧 Deploying development environment...${NC}"
kubectl apply -f infrastructure/kubernetes/ -n $NAMESPACE

echo -e "${YELLOW}🔧 Waiting for deployment to be ready...${NC}"
kubectl rollout status deployment/calculator-api -n $NAMESPACE --timeout=300s

echo -e "${GREEN}✅ Development deployment completed successfully!${NC}"

# Get service URLs
echo -e "${BLUE}📋 Service Information:${NC}"
echo -e "${BLUE}   API: http://localhost:8080${NC}"
echo -e "${BLUE}   Prometheus: http://localhost:9090${NC}"
echo -e "${BLUE}   Grafana: http://localhost:3000${NC}"

# Port forwarding for development
echo -e "${YELLOW}🔧 Setting up port forwarding...${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/calculator-api 8080:80${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/prometheus 9090:9090${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/grafana 3000:3000${NC}"

echo -e "${GREEN}🎉 Development environment is ready!${NC}" 