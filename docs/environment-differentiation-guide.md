# 🌍 Environment Differentiation Guide

## Overview

This guide demonstrates how to properly differentiate between **Development**, **Staging**, and **Production** environments in a CI/CD pipeline. We'll show you how to implement environment-specific configurations, deployment strategies, and safety measures.

## 🏗️ Environment Architecture

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

## 📋 Environment Comparison

| Aspect | Development | Staging | Production |
|--------|-------------|---------|------------|
| **Purpose** | Local development & testing | Integration testing & validation | Live user traffic |
| **Debug** | ✅ Enabled | ❌ Disabled | ❌ Disabled |
| **Log Level** | DEBUG | INFO | WARNING |
| **Rate Limit** | 1000/min | 100/min | 60/min |
| **Database** | calculator_dev | calculator_staging | calculator_prod |
| **Namespace** | calculator-dev | calculator-staging | calculator-prod |
| **Port** | 8080 | 8081 | 8082 |
| **Safety Checks** | Minimal | Moderate | Maximum |

## 🔧 Configuration Management

### Environment-Specific ConfigMaps

Each environment has its own Kubernetes ConfigMap with environment-specific settings:

#### Development (`infrastructure/kubernetes/namespace-dev.yml`)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: calculator-config-dev
  namespace: calculator-dev
data:
  ENVIRONMENT: "development"
  DEBUG: "true"
  LOG_LEVEL: "DEBUG"
  RATE_LIMIT_PER_MINUTE: "1000"
  ENABLE_METRICS: "true"
  ENABLE_ABS_DIFF: "true"
  ENABLE_HISTORY: "true"
```

#### Staging (`infrastructure/kubernetes/namespace-staging.yml`)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: calculator-config-staging
  namespace: calculator-staging
data:
  ENVIRONMENT: "staging"
  DEBUG: "false"
  LOG_LEVEL: "INFO"
  RATE_LIMIT_PER_MINUTE: "100"
  ENABLE_METRICS: "true"
  ENABLE_ABS_DIFF: "true"
  ENABLE_HISTORY: "true"
```

#### Production (`infrastructure/kubernetes/namespace-prod.yml`)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: calculator-config-prod
  namespace: calculator-prod
data:
  ENVIRONMENT: "production"
  DEBUG: "false"
  LOG_LEVEL: "WARNING"
  RATE_LIMIT_PER_MINUTE: "60"
  ENABLE_METRICS: "true"
  ENABLE_ABS_DIFF: "true"
  ENABLE_HISTORY: "true"
```

### Application Configuration (`app/api/utils/config.py`)

The application automatically detects the environment and applies appropriate settings:

```python
class Config:
    """Application configuration with environment-specific settings"""
    
    # Environment detection
    ENVIRONMENT: Environment = Environment(
        os.getenv("ENVIRONMENT", "development").lower()
    )
    
    @classmethod
    def get_environment_specific_config(cls) -> dict:
        """Get environment-specific configuration"""
        if cls.ENVIRONMENT == Environment.DEVELOPMENT:
            return {
                "debug": True,
                "log_level": "DEBUG",
                "rate_limit": 1000,
                "enable_metrics": True,
            }
        elif cls.ENVIRONMENT == Environment.STAGING:
            return {
                "debug": False,
                "log_level": "INFO",
                "rate_limit": 100,
                "enable_metrics": True,
            }
        elif cls.ENVIRONMENT == Environment.PRODUCTION:
            return {
                "debug": False,
                "log_level": "WARNING",
                "rate_limit": 60,
                "enable_metrics": True,
            }
```

## 🚀 Deployment Pipeline

### 1. Development Phase
```bash
# Feature development
git checkout -b feature/add-abs-diff

# Local testing
python -m pytest tests/ -v

# Code review and merge
git push origin feature/add-abs-diff
# Create PR → Merge to main
```

### 2. CI/CD Pipeline (GitHub Actions)
```yaml
# ci-cd/github-actions/ci.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: python -m pytest tests/ -v
      - name: Build Docker image
        run: docker build -t calculator-api:${{ github.sha }} .
```

### 3. Staging Deployment
```bash
# Deploy to staging
./scripts/deploy-staging.sh

# Run integration tests against staging
python -m pytest tests/integration/ -v

# Performance testing
# Load testing against staging environment
```

### 4. Production Deployment
```bash
# Deploy to production (with safety checks)
./scripts/deploy-prod.sh

# Manual confirmation required
# Type 'PRODUCTION' to confirm deployment
```

## 🔒 Security Measures

### Environment-Specific Security

| Environment | Debug Mode | Rate Limits | Safety Checks | Approval Required |
|-------------|------------|-------------|---------------|-------------------|
| **Development** | ✅ Enabled | 1000/min | Minimal | ❌ No |
| **Staging** | ❌ Disabled | 100/min | Moderate | ❌ No |
| **Production** | ❌ Disabled | 60/min | Maximum | ✅ Yes |

### Production Safety Checks

The production deployment script includes comprehensive safety measures:

```bash
# Check if on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "❌ Must be on main branch for production deployment"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ There are uncommitted changes"
    exit 1
fi

# Manual confirmation
echo "⚠️  Are you sure you want to deploy to PRODUCTION?"
read -p "Type 'PRODUCTION' to confirm: " confirmation

# Run all tests before deployment
python -m pytest tests/ -v
```

## 📊 Monitoring & Observability

### Environment-Specific Monitoring

| Environment | Log Level | Metrics | Alerts | Dashboard |
|-------------|-----------|---------|--------|-----------|
| **Development** | DEBUG | Development metrics | Basic | Development dashboard |
| **Staging** | INFO | Performance metrics | Moderate | Staging dashboard |
| **Production** | WARNING | Production metrics | Critical | Production dashboard |

### Prometheus Queries by Environment

```promql
# Development metrics
rate(http_requests_total{environment="development"}[5m])

# Staging metrics  
rate(http_requests_total{environment="staging"}[5m])

# Production metrics
rate(http_requests_total{environment="production"}[5m])
```

## 🛠️ Deployment Scripts

### Development Deployment (`scripts/deploy-dev.ps1`)
```powershell
# Quick deployment for development
Write-Host "🚀 Deploying to Development Environment..."
docker build -t calculator-api:dev .
kubectl apply -f infrastructure/kubernetes/namespace-dev.yml
kubectl apply -f infrastructure/kubernetes/ -n calculator-dev
```

### Staging Deployment (`scripts/deploy-staging.ps1`)
```powershell
# Automated deployment with testing
Write-Host "🚀 Deploying to Staging Environment..."
docker build -t calculator-api:staging .
kubectl apply -f infrastructure/kubernetes/namespace-staging.yml
kubectl apply -f infrastructure/kubernetes/ -n calculator-staging
# Run integration tests against staging
```

### Production Deployment (`scripts/deploy-prod.ps1`)
```powershell
# Production deployment with safety checks
Write-Host "🚀 Deploying to Production Environment..."
# Safety checks
# Manual confirmation
# Test execution
# Rolling deployment
# Health monitoring
```

## 🔍 Environment Comparison Tools

### Compare Environments (`scripts/compare-environments.py`)
```bash
# Compare all environments
python scripts/compare-environments.py compare

# Get detailed config for specific environment
python scripts/compare-environments.py detail production

# Test connectivity to environment
python scripts/compare-environments.py test staging
```

### Environment Demonstration (`scripts/show-environments.py`)
```bash
# Show complete environment overview
python scripts/show-environments.py
```

## 📈 Best Practices

### ✅ Environment Isolation
- **Separate namespaces** for each environment
- **Isolated databases** (dev/staging/prod)
- **Different ports** to avoid conflicts
- **Environment-specific secrets**

### ✅ Configuration Management
- **ConfigMaps** for environment variables
- **Secrets** for sensitive data
- **Feature flags** for gradual rollouts
- **Environment detection** in application code

### ✅ Progressive Deployment
- **Development** → **Staging** → **Production**
- **Automated testing** at each stage
- **Manual approval** for production
- **Rollback capability** at each stage

### ✅ Safety Measures
- **Increasing safety checks** per environment
- **Branch protection** for production
- **Test requirements** before deployment
- **Health monitoring** post-deployment

### ✅ Monitoring & Observability
- **Environment-appropriate logging**
- **Separate metrics** per environment
- **Environment-specific dashboards**
- **Alerting based on environment**

## 🎯 Key Takeaways

1. **Environment Isolation**: Each environment has its own namespace, database, and configuration
2. **Progressive Safety**: Safety measures increase as you move toward production
3. **Configuration Management**: Environment-specific settings via ConfigMaps and environment variables
4. **Automated Testing**: Comprehensive testing at each stage of the pipeline
5. **Manual Oversight**: Production deployments require manual approval and comprehensive checks
6. **Monitoring**: Environment-appropriate logging and metrics for each stage

## 🚀 Next Steps

1. **Deploy to Development**: `./scripts/deploy-dev.ps1`
2. **Test in Staging**: `./scripts/deploy-staging.ps1`
3. **Deploy to Production**: `./scripts/deploy-prod.ps1`
4. **Monitor Environments**: Use the comparison tools to track differences
5. **Customize Configurations**: Modify ConfigMaps for your specific needs

This environment differentiation setup ensures that your CI/CD pipeline is robust, safe, and follows industry best practices for multi-environment deployments. 