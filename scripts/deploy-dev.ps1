# Development Environment Deployment Script
param(
    [switch]$SkipTests
)

Write-Host "🚀 Deploying to Development Environment..." -ForegroundColor Green

# Environment variables
$env:ENVIRONMENT = "development"
$env:NAMESPACE = "calculator-dev"
$env:IMAGE_TAG = "latest"

Write-Host "📋 Environment: Development" -ForegroundColor Blue
Write-Host "📋 Namespace: $env:NAMESPACE" -ForegroundColor Blue
Write-Host "📋 Image Tag: $env:IMAGE_TAG" -ForegroundColor Blue

# Check if kubectl is available
try {
    kubectl version --client | Out-Null
    Write-Host "✅ kubectl is available" -ForegroundColor Green
} catch {
    Write-Host "❌ kubectl is not installed" -ForegroundColor Red
    exit 1
}

# Check if Docker is available
try {
    docker version | Out-Null
    Write-Host "✅ Docker is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed" -ForegroundColor Red
    exit 1
}

Write-Host "🔧 Building Docker image..." -ForegroundColor Yellow
docker build -t calculator-api:dev .

Write-Host "🔧 Creating development namespace and configs..." -ForegroundColor Yellow
kubectl apply -f infrastructure/kubernetes/namespace-dev.yml

Write-Host "🔧 Deploying development environment..." -ForegroundColor Yellow
kubectl apply -f infrastructure/kubernetes/ -n $env:NAMESPACE

Write-Host "🔧 Waiting for deployment to be ready..." -ForegroundColor Yellow
kubectl rollout status deployment/calculator-api -n $env:NAMESPACE --timeout=300s

Write-Host "✅ Development deployment completed successfully!" -ForegroundColor Green

# Get service URLs
Write-Host "📋 Service Information:" -ForegroundColor Blue
Write-Host "   API: http://localhost:8080" -ForegroundColor Blue
Write-Host "   Prometheus: http://localhost:9090" -ForegroundColor Blue
Write-Host "   Grafana: http://localhost:3000" -ForegroundColor Blue

# Port forwarding for development
Write-Host "🔧 Setting up port forwarding..." -ForegroundColor Yellow
Write-Host "   Run: kubectl port-forward -n $env:NAMESPACE svc/calculator-api 8080:80" -ForegroundColor Blue
Write-Host "   Run: kubectl port-forward -n $env:NAMESPACE svc/prometheus 9090:9090" -ForegroundColor Blue
Write-Host "   Run: kubectl port-forward -n $env:NAMESPACE svc/grafana 3000:3000" -ForegroundColor Blue

Write-Host "🎉 Development environment is ready!" -ForegroundColor Green 