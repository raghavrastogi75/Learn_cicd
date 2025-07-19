# 🧮 Calculator API - CI/CD Learning Project

A comprehensive calculator API project designed to demonstrate modern CI/CD practices, environment differentiation, and DevOps best practices.

## 🚀 Features

### Mathematical Operations
- **Basic Operations**: Add, Subtract, Multiply, Divide
- **Advanced Operations**: Power, Square Root, Absolute Difference
- **New Feature**: **Cubic Power** (x³) - See [Case Study](docs/cubic-feature-development-case-study.md)

### API Endpoints
- `POST /api/calculator/calculate` - Perform calculations
- `GET /api/calculator/operations` - List available operations
- `GET /api/history` - View calculation history
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Development   │    │   Staging       │    │   Production    │
│   Environment   │───▶│   Environment   │───▶│   Environment   │
│                 │    │                 │    │                 │
│ • Local testing │    │ • Integration   │    │ • Live users    │
│ • Unit tests    │    │ • E2E tests     │    │ • High traffic  │
│ • Quick deploy  │    │ • Performance   │    │ • Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📚 Documentation

- [Environment Differentiation Guide](docs/environment-differentiation-guide.md) - How environments are configured and managed
- [Cubic Feature Development Case Study](docs/cubic-feature-development-case-study.md) - Complete feature development lifecycle
- [Deployment Guide](docs/deployment-guide.md) - How to deploy to different environments
- [Kubernetes Deployment Guide](docs/kubernetes-deployment-guide.md) - K8s deployment instructions
- [Alerting Guide](docs/alerting-guide.md) - Monitoring and alerting setup

## 🎯 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Kubernetes cluster (for full deployment)

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd Learn_cicd

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Start the application
python -m uvicorn app.api.main:app --reload
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline with:

### GitHub Actions Workflow
- **Linting & Formatting**: Black, isort, flake8, mypy
- **Testing**: Unit tests, integration tests, coverage reporting
- **Security**: Bandit security scan, dependency safety check
- **Building**: Docker image build and push
- **Deployment**: Automated deployment to staging, manual production deployment

### Environment Progression
1. **Development** → Local development and testing
2. **Staging** → Integration testing and validation (deploys from master branch)
3. **Production** → Live user traffic with safety measures (manual deployment from master)

## 🧪 Feature Development Demo

### Cubic Power Feature Case Study
This project includes a complete demonstration of adding a new feature (cubic power operation) through all environments:

```bash
# Run the feature development demonstration
python scripts/feature-development-demo.py
```

The demo shows:
- ✅ Feature branch creation and development
- ✅ Unit testing and validation
- ✅ CI/CD pipeline execution
- ✅ Staging deployment and testing
- ✅ Production deployment with safety checks
- ✅ Feature verification in all environments

### What You'll Learn
- **Environment Differentiation**: How each environment is configured differently
- **Progressive Safety**: Safety measures that increase per environment
- **Testing Strategy**: Comprehensive testing at each stage
- **Deployment Process**: Blue-green deployment and rollback strategies
- **Monitoring**: Metrics collection and alerting setup

## 📊 Monitoring & Observability

### Prometheus Metrics
- Request count and latency
- Operation-specific metrics
- Error rates and status codes
- Database connection metrics

### Grafana Dashboards
- Calculator API performance dashboard
- Environment-specific monitoring
- Alerting and notification channels

### Health Checks
- Application health endpoints
- Database connectivity checks
- Third-party service monitoring

## 🛠️ Development Tools

### Scripts
- `scripts/deploy-dev.ps1` - Deploy to development
- `scripts/deploy-staging.sh` - Deploy to staging
- `scripts/deploy-prod.sh` - Deploy to production
- `scripts/compare-environments.py` - Compare environment configurations
- `scripts/show-environments.py` - Display environment overview

### Testing
- Unit tests for business logic
- Integration tests for API endpoints
- Performance and load testing
- Security vulnerability scanning

## 🔒 Security Features

- Rate limiting per environment
- Input validation and sanitization
- Secure configuration management
- Environment-specific secrets
- CORS and trusted host middleware

## 📈 Performance

- Async/await for non-blocking operations
- Database connection pooling
- Redis caching (optional)
- Prometheus metrics collection
- Structured logging with correlation IDs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest tests/ -v`
5. Commit your changes: `git commit -m 'feat: Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Learning Objectives

This project demonstrates:

1. **Modern CI/CD Practices**: Automated testing, building, and deployment
2. **Environment Management**: Proper separation and configuration of environments
3. **Infrastructure as Code**: Kubernetes manifests and deployment automation
4. **Monitoring & Observability**: Metrics, logging, and alerting
5. **Security Best Practices**: Input validation, rate limiting, and secure configuration
6. **Testing Strategies**: Unit, integration, and performance testing
7. **DevOps Tools**: Docker, Kubernetes, Prometheus, Grafana

Perfect for learning modern software development practices and DevOps methodologies! 