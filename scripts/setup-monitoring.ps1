# Setup Monitoring Access Script
# This script sets up port forwarding for Prometheus and Grafana

Write-Host "🔧 Setting up Monitoring Access" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if pods are running
Write-Host "`n📊 Checking pod status..." -ForegroundColor Yellow
kubectl get pods -n calculator-app

# Wait for Prometheus to be ready
Write-Host "`n⏳ Waiting for Prometheus..." -ForegroundColor Yellow
try {
    kubectl wait --for=condition=ready pod -l app=prometheus -n calculator-app --timeout=60s
    Write-Host "✅ Prometheus is ready!" -ForegroundColor Green
} catch {
    Write-Host "❌ Prometheus is not ready yet" -ForegroundColor Red
}

# Wait for Grafana to be ready
Write-Host "`n⏳ Waiting for Grafana..." -ForegroundColor Yellow
try {
    kubectl wait --for=condition=ready pod -l app=grafana -n calculator-app --timeout=60s
    Write-Host "✅ Grafana is ready!" -ForegroundColor Green
} catch {
    Write-Host "❌ Grafana is not ready yet" -ForegroundColor Red
}

# Check services
Write-Host "`n🌐 Checking services..." -ForegroundColor Yellow
kubectl get services -n calculator-app

Write-Host "`n🚀 Starting port forwarding..." -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "`n📊 Prometheus will be available at: http://localhost:9090" -ForegroundColor Cyan
Write-Host "📈 Grafana will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor Yellow
Write-Host "   Password: admin" -ForegroundColor Yellow

Write-Host "`n🔗 Starting port forwarding in background..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red

# Start Prometheus port forwarding
Start-Job -ScriptBlock {
    kubectl port-forward -n calculator-app svc/prometheus 9090:9090
} -Name "prometheus-forward"

# Start Grafana port forwarding
Start-Job -ScriptBlock {
    kubectl port-forward -n calculator-app svc/grafana 3000:3000
} -Name "grafana-forward"

Write-Host "`n✅ Port forwarding started!" -ForegroundColor Green
Write-Host "`n📋 Monitoring URLs:" -ForegroundColor Cyan
Write-Host "   Prometheus: http://localhost:9090" -ForegroundColor White
Write-Host "   Grafana:    http://localhost:3000" -ForegroundColor White

Write-Host "`n🔍 To check if services are working:" -ForegroundColor Yellow
Write-Host "   Test Prometheus: curl http://localhost:9090/api/v1/query?query=up" -ForegroundColor Gray
Write-Host "   Test Grafana:   curl http://localhost:3000/api/health" -ForegroundColor Gray

Write-Host "`n⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Test connections
Write-Host "`n🧪 Testing connections..." -ForegroundColor Yellow

try {
    $prometheusTest = Invoke-RestMethod -Uri "http://localhost:9090/api/v1/query?query=up" -Method Get -TimeoutSec 5
    Write-Host "✅ Prometheus is responding!" -ForegroundColor Green
} catch {
    Write-Host "❌ Prometheus is not responding yet" -ForegroundColor Red
}

try {
    $grafanaTest = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -Method Get -TimeoutSec 5
    Write-Host "✅ Grafana is responding!" -ForegroundColor Green
} catch {
    Write-Host "❌ Grafana is not responding yet" -ForegroundColor Red
}

Write-Host "`n🎉 Setup complete! Open your browser to access the dashboards." -ForegroundColor Green
Write-Host "`nTo stop port forwarding, run:" -ForegroundColor Yellow
Write-Host "   Get-Job | Stop-Job" -ForegroundColor Gray
Write-Host "   Get-Job | Remove-Job" -ForegroundColor Gray 