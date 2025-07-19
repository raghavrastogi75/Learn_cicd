#!/bin/bash

# Staging Environment Deployment Script
set -e

echo "🚀 Deploying to Staging Environment..."

# Environment variables
export ENVIRONMENT="staging"
export NAMESPACE="calculator-staging"
export IMAGE_TAG="staging"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Environment: Staging${NC}"
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

echo -e "${YELLOW}🔧 Building Docker image for staging...${NC}"
docker build -t calculator-api:staging .

echo -e "${YELLOW}🔧 Creating staging namespace and configs...${NC}"
kubectl apply -f infrastructure/kubernetes/namespace-staging.yml

echo -e "${YELLOW}🔧 Deploying staging environment...${NC}"
kubectl apply -f infrastructure/kubernetes/ -n $NAMESPACE

echo -e "${YELLOW}🔧 Waiting for deployment to be ready...${NC}"
kubectl rollout status deployment/calculator-api -n $NAMESPACE --timeout=300s

echo -e "${GREEN}✅ Staging deployment completed successfully!${NC}"

# Run integration tests against staging
echo -e "${YELLOW}🧪 Running integration tests against staging...${NC}"
# Note: In real scenario, you'd point tests to staging URLs
echo -e "${BLUE}   Integration tests would run against staging environment${NC}"

# Performance testing
echo -e "${YELLOW}📊 Running performance tests...${NC}"
echo -e "${BLUE}   Load testing would be performed against staging${NC}"

# Get service URLs
echo -e "${BLUE}📋 Service Information:${NC}"
echo -e "${BLUE}   API: http://localhost:8081${NC}"
echo -e "${BLUE}   Prometheus: http://localhost:9091${NC}"
echo -e "${BLUE}   Grafana: http://localhost:3001${NC}"

# Port forwarding for staging
echo -e "${YELLOW}🔧 Setting up port forwarding...${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/calculator-api 8081:80${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/prometheus 9091:9090${NC}"
echo -e "${BLUE}   Run: kubectl port-forward -n $NAMESPACE svc/grafana 3001:3000${NC}"

echo -e "${GREEN}🎉 Staging environment is ready for testing!${NC}" 