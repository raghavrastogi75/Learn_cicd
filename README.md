# 🧮 Calculator API with Kubernetes & Monitoring

A production-ready Calculator API deployed on Kubernetes with comprehensive monitoring, auto-scaling, and CI/CD pipeline.

## 🚀 Features

- **FastAPI-based Calculator API** with mathematical operations
- **Kubernetes Deployment** with auto-scaling (HPA)
- **Prometheus & Grafana Monitoring** with custom dashboards
- **PostgreSQL Database** for calculation history
- **Redis Caching** for performance optimization
- **Traffic Generation** for load testing
- **Comprehensive Testing** (unit & integration)
- **CI/CD Pipeline** with GitHub Actions
- **Production-ready** with health checks and metrics

## 📊 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Prometheus    │    │     Grafana     │
│   (Ingress)     │    │   (Monitoring)  │    │   (Dashboard)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Calculator API │    │   PostgreSQL    │    │      Redis      │
│  (10 Pods)      │    │   (Database)    │    │    (Cache)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Container**: Docker
- **Orchestration**: Kubernetes
- **Monitoring**: Prometheus, Grafana
- **CI/CD**: GitHub Actions
- **Testing**: pytest, coverage
- **Code Quality**: black, flake8, mypy

## 📁 Project Structure

```
Learn_cicd/
├── app/                          # Application code
│   ├── api/                      # FastAPI application
│   │   ├── database/             # Database models & connection
│   │   ├── models/               # Pydantic models
│   │   ├── routes/               # API endpoints
│   │   ├── services/             # Business logic
│   │   └── utils/                # Utilities (config, logger, metrics)
│   └── database/                 # Database initialization
├── ci-cd/                        # CI/CD configuration
│   └── github-actions/           # GitHub Actions workflows
├── infrastructure/               # Infrastructure as Code
│   └── kubernetes/               # Kubernetes manifests
├── monitoring/                   # Monitoring configuration
│   ├── grafana/                  # Grafana dashboards & configs
│   └── prometheus/               # Prometheus configuration
├── scripts/                      # Utility scripts
├── tests/                        # Test suite
│   ├── integration/              # Integration tests
│   └── unit/                     # Unit tests
├── docs/                         # Documentation
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Local development
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop with Kubernetes enabled
- kubectl CLI tool
- Python 3.11+
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Learn_cicd
```

### 2. Set Up Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally with Docker Compose
docker-compose up -d
```

### 3. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f infrastructure/kubernetes/namespace.yml

# Deploy database and cache
kubectl apply -f infrastructure/kubernetes/postgres-deployment.yml
kubectl apply -f infrastructure/kubernetes/redis-deployment.yml

# Deploy the API
kubectl apply -f infrastructure/kubernetes/api-deployment.yml

# Deploy monitoring
kubectl apply -f infrastructure/kubernetes/monitoring.yml
kubectl apply -f infrastructure/kubernetes/prometheus-config.yml
kubectl apply -f infrastructure/kubernetes/prometheus-deployment.yml
kubectl apply -f infrastructure/kubernetes/grafana-provisioning.yml
```

### 4. Access the Services

```bash
# API (Calculator)
kubectl port-forward -n calculator-app svc/calculator-api 8080:80
# Access: http://localhost:8080

# Prometheus (Monitoring)
kubectl port-forward -n calculator-app svc/prometheus 9090:9090
# Access: http://localhost:9090

# Grafana (Dashboards)
kubectl port-forward -n calculator-app svc/grafana 3001:3000
# Access: http://localhost:3001 (admin/admin)
```

## 📊 Monitoring & Observability

### Prometheus Metrics

The API exposes comprehensive metrics:

- **HTTP Metrics**: Request rate, response times, error rates
- **Business Metrics**: Calculator operations, success rates
- **System Metrics**: Memory usage, CPU, garbage collection
- **Custom Metrics**: Operation-specific counters

### Grafana Dashboards

Pre-configured dashboards include:

- **Calculator API Production Dashboard**: Real-time performance metrics
- **Request Rate Analysis**: Traffic patterns and load distribution
- **Error Rate Monitoring**: 4xx/5xx error tracking
- **Response Time Distribution**: 50th, 95th, 99th percentiles
- **Calculator Operations**: Add, subtract, multiply, divide rates

### Key Metrics to Monitor

```promql
# API Health
up{job="calculator-api"}

# Request Rate
rate(http_requests_total{job="calculator-api"}[5m])

# Error Rate
rate(http_requests_total{job="calculator-api", status=~"4..|5.."}[5m])

# Response Time (95th percentile)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="calculator-api"}[5m]))

# Calculator Operations
rate(calculator_operations_total{job="calculator-api"}[5m])
```

## 🔄 Auto-Scaling

The API uses Horizontal Pod Autoscaler (HPA) with:

- **Minimum Pods**: 3
- **Maximum Pods**: 10
- **Target CPU**: 70%
- **Scale Up Cooldown**: 60s
- **Scale Down Cooldown**: 300s

### Load Testing

Use the included traffic generator:

```bash
python scripts/generate_traffic.py
```

Options:
1. Continuous traffic at 5 RPS
2. Simulate traffic patterns
3. Custom traffic burst
4. Exit

## 🧪 Testing

### Run Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# With coverage
pytest --cov=app tests/ -v
```

### Test Coverage

The project includes comprehensive test coverage for:
- API endpoints
- Business logic
- Database operations
- Error handling
- Integration scenarios

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/calculator

# Redis
REDIS_URL=redis://redis:6379

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Kubernetes Configuration

All Kubernetes resources are configured via YAML manifests in `infrastructure/kubernetes/`:

- **Deployments**: Application, database, monitoring
- **Services**: Load balancing and service discovery
- **ConfigMaps**: Application configuration
- **Secrets**: Sensitive data (database passwords, etc.)
- **PersistentVolumeClaims**: Data persistence
- **HorizontalPodAutoscaler**: Auto-scaling configuration

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline includes:

1. **Code Quality Checks**
   - Linting (flake8)
   - Code formatting (black)
   - Type checking (mypy)

2. **Testing**
   - Unit tests
   - Integration tests
   - Coverage reporting

3. **Security Scanning**
   - Dependency vulnerability scanning
   - Container image scanning

4. **Build & Deploy**
   - Docker image building
   - Kubernetes deployment
   - Health checks

### Pipeline Stages

```yaml
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Python
      - Install dependencies
      - Run linting
      - Run tests
      - Generate coverage report

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - Build Docker image
      - Push to registry
      - Deploy to Kubernetes
```

## 📈 Performance

### Current Metrics (Example)

- **Request Rate**: 5+ RPS sustained
- **Response Time**: <100ms (95th percentile)
- **Success Rate**: 99.5%+
- **Auto-scaling**: 3-10 pods based on load
- **Memory Usage**: ~50MB per pod
- **CPU Usage**: ~10% per pod under normal load

### Scaling Behavior

- **Scale Up**: Triggers at 70% CPU usage
- **Scale Down**: Occurs after 5 minutes of low usage
- **Pod Startup Time**: ~30 seconds
- **Health Check**: 5-second intervals

## 🔍 Troubleshooting

### Common Issues

1. **Grafana Not Accessible**
   ```bash
   kubectl get pods -n calculator-app -l app=grafana
   kubectl logs -n calculator-app -l app=grafana
   ```

2. **Prometheus Connection Issues**
   ```bash
   kubectl get svc -n calculator-app prometheus
   kubectl describe pod -n calculator-app -l app=prometheus
   ```

3. **API Scaling Issues**
   ```bash
   kubectl get hpa -n calculator-app
   kubectl describe hpa calculator-api -n calculator-app
   ```

### Useful Commands

```bash
# Check all resources
kubectl get all -n calculator-app

# View logs
kubectl logs -n calculator-app -l app=calculator-api

# Monitor pods
kubectl get pods -n calculator-app -w

# Check metrics
kubectl top pods -n calculator-app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Kubernetes for container orchestration
- Prometheus & Grafana for monitoring
- The open-source community for inspiration

---

**Happy Calculating! 🧮✨** 