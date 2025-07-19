#!/bin/bash

# Production Environment Deployment Script
set -e

echo "🚀 Deploying to Production Environment..."

# Environment variables
export ENVIRONMENT="production"
export NAMESPACE="calculator-prod"
export IMAGE_TAG="v1.0.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Environment: Production${NC}"
echo -e "${BLUE}📋 Namespace: $NAMESPACE${NC}"
echo -e "${BLUE}📋 Image Tag: $IMAGE_TAG${NC}"

# Safety checks
echo -e "${YELLOW}⚠️  PRODUCTION DEPLOYMENT - Safety Checks${NC}"

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

# Check if we're on the main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${RED}❌ Must be on main branch for production deployment${NC}"
    echo -e "${RED}   Current branch: $CURRENT_BRANCH${NC}"
    exit 1
fi

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}❌ There are uncommitted changes${NC}"
    git status --short
    exit 1
fi

# Confirm deployment
echo -e "${YELLOW}⚠️  Are you sure you want to deploy to PRODUCTION?${NC}"
echo -e "${YELLOW}   This will affect live users!${NC}"
read -p "Type 'PRODUCTION' to confirm: " confirmation

if [ "$confirmation" != "PRODUCTION" ]; then
    echo -e "${RED}❌ Deployment cancelled${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Production deployment confirmed${NC}"

# Run all tests before production deployment
echo -e "${YELLOW}🧪 Running all tests before production deployment...${NC}"
python -m pytest tests/ -v

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Tests failed - aborting production deployment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All tests passed${NC}"

echo -e "${YELLOW}🔧 Building Docker image for production...${NC}"
docker build -t calculator-api:prod .

echo -e "${YELLOW}🔧 Creating production namespace and configs...${NC}"
kubectl apply -f infrastructure/kubernetes/namespace-prod.yml

echo -e "${YELLOW}🔧 Deploying production environment...${NC}"
kubectl apply -f infrastructure/kubernetes/ -n $NAMESPACE

echo -e "${YELLOW}🔧 Waiting for deployment to be ready...${NC}"
kubectl rollout status deployment/calculator-api -n $NAMESPACE --timeout=600s

echo -e "${GREEN}✅ Production deployment completed successfully!${NC}"

# Health checks
echo -e "${YELLOW}🏥 Running health checks...${NC}"
kubectl port-forward -n $NAMESPACE svc/calculator-api 8082:80 &
PF_PID=$!

sleep 5

# Test the new abs_diff feature
echo -e "${YELLOW}🧪 Testing new abs_diff feature in production...${NC}"
curl -X POST http://localhost:8082/api/calculator/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "abs_diff", "a": 10, "b": 3}' \
  -s | jq .

# Kill port forward
kill $PF_PID

# Get service URLs
echo -e "${BLUE}📋 Production Service Information:${NC}"
echo -e "${BLUE}   API: http://localhost:8082${NC}"
echo -e "${BLUE}   Prometheus: http://localhost:9092${NC}"
echo -e "${BLUE}   Grafana: http://localhost:3002${NC}"

# Port forwarding for production
echo -e "${YELLOW}🔧 Setting up port forwarding...${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/calculator-api 8082:80${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/prometheus 9092:9090${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/grafana 3002:3000${NC}"

echo -e "${GREEN}🎉 Production deployment completed successfully!${NC}"
echo -e "${GREEN}🎉 New abs_diff feature is now live in production!${NC}" 