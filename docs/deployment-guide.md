# Deployment Guide - Calculator CI/CD Learning Project

This guide will walk you through the complete CI/CD pipeline, from development to production deployment, including monitoring and advanced deployment strategies.

## 🏗️ Architecture Overview

### Application Stack
- **Backend**: FastAPI with Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions + ArgoCD
- **Monitoring**: Prometheus + Grafana

### Environment Strategy
1. **Development**: Local development with hot reload
2. **Staging**: Pre-production testing environment
3. **Production**: Live production environment

## 🚀 Local Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git

### Quick Start
```bash
# Clone the repository
git clone <your-repo>
cd Learn_cicd

# Start all services
docker-compose up -d

# The application will be available at:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Grafana: http://localhost:3001 (admin/admin)
# - Prometheus: http://localhost:9090
```

### Manual Setup (Alternative)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://postgres:password@localhost:5432/calculator_db"
export REDIS_URL="redis://localhost:6379"

# Run the application
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Testing Strategy

### Test Types
1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test API endpoints and database interactions
3. **End-to-End Tests**: Test complete user workflows

### Running Tests
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# All tests with coverage
pytest --cov=app tests/ --cov-report=html

# Test specific file
pytest tests/unit/test_calculator_service.py -v
```

### Test Coverage
- Aim for >80% code coverage
- Focus on critical business logic
- Test error conditions and edge cases

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline consists of several stages:

1. **Lint & Format Check**
   - Black code formatting
   - isort import sorting
   - flake8 linting
   - mypy type checking

2. **Unit Tests**
   - Run unit tests with pytest
   - Generate coverage reports
   - Upload to Codecov

3. **Integration Tests**
   - Test with real PostgreSQL and Redis
   - API endpoint testing
   - Database interaction testing

4. **Security Scan**
   - Bandit security analysis
   - Safety dependency check

5. **Build Docker Image**
   - Multi-stage Docker build
   - Push to GitHub Container Registry
   - Cache optimization

6. **Deploy to Environments**
   - Development: Auto-deploy on develop branch
   - Staging: Auto-deploy on main branch
   - Production: Manual deployment

### Pipeline Triggers
- **Push to develop**: Runs tests and deploys to development
- **Push to main**: Runs tests and deploys to staging
- **Manual trigger**: Deploy to production

## 🐳 Containerization

### Docker Strategy
- **Multi-stage builds**: Separate development and production images
- **Security**: Non-root user, minimal base images
- **Optimization**: Layer caching, minimal dependencies

### Docker Commands
```bash
# Build development image
docker build --target development -t calculator-api:dev .

# Build production image
docker build --target production -t calculator-api:prod .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api
```

## ☸️ Kubernetes Deployment

### Deployment Strategy
1. **Blue-Green Deployment**: Zero-downtime deployments
2. **Canary Deployment**: Gradual traffic shifting
3. **Rolling Updates**: Controlled version updates

### Kubernetes Manifests
```bash
# Apply to development
kubectl apply -f infrastructure/kubernetes/dev/

# Apply to staging
kubectl apply -f infrastructure/kubernetes/staging/

# Apply to production
kubectl apply -f infrastructure/kubernetes/production/
```

### Health Checks
- **Liveness Probe**: `/health/live` - Is the app running?
- **Readiness Probe**: `/health/ready` - Is the app ready to serve traffic?
- **Startup Probe**: `/health` - Is the app starting up?

## 📊 Monitoring & Observability

### Metrics Collection
- **Application Metrics**: Request rate, response time, error rate
- **Business Metrics**: Calculation operations, usage patterns
- **Infrastructure Metrics**: CPU, memory, disk usage

### Prometheus Configuration
```yaml
# Scrape calculator API metrics
- job_name: 'calculator-api'
  static_configs:
    - targets: ['api:8000']
  metrics_path: '/metrics'
  scrape_interval: 10s
```

### Grafana Dashboards
- **Application Dashboard**: API performance and errors
- **Business Dashboard**: Calculator usage and trends
- **Infrastructure Dashboard**: System resources

### Alerting Rules
```yaml
# High error rate alert
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
  for: 2m
  labels:
    severity: warning
  annotations:
    summary: "High error rate detected"
```

## 🚀 Deployment Strategies

### 1. Blue-Green Deployment
```bash
# Deploy new version (green)
kubectl apply -f k8s/calculator-v2.yml

# Wait for green to be ready
kubectl rollout status deployment/calculator-api-v2

# Switch traffic to green
kubectl patch service calculator-service -p '{"spec":{"selector":{"version":"v2"}}}'

# Remove old version (blue)
kubectl delete deployment calculator-api-v1
```

### 2. Canary Deployment
```bash
# Deploy canary with 10% traffic
kubectl apply -f k8s/calculator-canary.yml

# Monitor canary performance
kubectl get pods -l app=calculator-api,version=canary

# Gradually increase traffic
kubectl patch service calculator-service -p '{"spec":{"selector":{"version":"canary"}}}'
```

### 3. Rolling Update
```bash
# Update deployment
kubectl set image deployment/calculator-api calculator-api=ghcr.io/username/calculator-api:v2

# Monitor rollout
kubectl rollout status deployment/calculator-api

# Rollback if needed
kubectl rollout undo deployment/calculator-api
```

## 🔒 Security Considerations

### Container Security
- Non-root user execution
- Read-only root filesystem
- Minimal base images
- Regular security updates

### Network Security
- TLS/SSL encryption
- Network policies
- Ingress controllers
- Service mesh (optional)

### Secrets Management
```bash
# Create Kubernetes secrets
kubectl create secret generic calculator-secrets \
  --from-literal=database-url="postgresql://..." \
  --from-literal=redis-url="redis://..." \
  --from-literal=secret-key="your-secret-key"
```

## 📈 Performance Optimization

### Application Level
- Database connection pooling
- Redis caching
- Async operations
- Response compression

### Infrastructure Level
- Horizontal pod autoscaling
- Resource limits and requests
- Node affinity and anti-affinity
- Pod disruption budgets

### Monitoring Performance
```bash
# Check resource usage
kubectl top pods

# Monitor application metrics
curl http://localhost:8000/metrics

# View Grafana dashboards
open http://localhost:3001
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database connectivity
   kubectl exec -it <pod-name> -- pg_isready -h postgres -p 5432
   ```

2. **High Memory Usage**
   ```bash
   # Check memory usage
   kubectl top pods
   kubectl describe pod <pod-name>
   ```

3. **Slow Response Times**
   ```bash
   # Check application logs
   kubectl logs -f deployment/calculator-api
   
   # Check Prometheus metrics
   curl http://localhost:9090/api/v1/query?query=rate(http_request_duration_seconds_sum[5m])
   ```

### Debug Commands
```bash
# Get pod details
kubectl describe pod <pod-name>

# View logs
kubectl logs -f <pod-name>

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/bash

# Port forward for debugging
kubectl port-forward <pod-name> 8000:8000
```

## 📚 Next Steps

1. **Advanced Monitoring**: Set up distributed tracing with Jaeger
2. **Service Mesh**: Implement Istio for advanced traffic management
3. **GitOps**: Use ArgoCD for declarative deployments
4. **Chaos Engineering**: Implement failure testing
5. **Cost Optimization**: Monitor and optimize resource usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the troubleshooting section
- Review the monitoring dashboards
- Consult the application logs 