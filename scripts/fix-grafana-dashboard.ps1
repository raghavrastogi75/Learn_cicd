#!/usr/bin/env pwsh

Write-Host "🔧 Fixing Grafana Dashboard Access" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

Write-Host "`n📊 Current Status:" -ForegroundColor Yellow
kubectl get pods -n calculator-app -l app=grafana

Write-Host "`n🌐 Access Information:" -ForegroundColor Cyan
Write-Host "   URL: http://localhost:3000" -ForegroundColor White
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin" -ForegroundColor White

Write-Host "`n📋 Step-by-Step Instructions:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "2. Login with admin/admin" -ForegroundColor White
Write-Host "3. Go to Configuration → Data Sources" -ForegroundColor White
Write-Host "4. Click on 'Prometheus' datasource" -ForegroundColor White
Write-Host "5. Verify URL is: http://prometheus:9090" -ForegroundColor White
Write-Host "6. Click 'Save and Test'" -ForegroundColor White
Write-Host "7. Go to Dashboards → Browse" -ForegroundColor White
Write-Host "8. Look for 'Calculator API - Production Dashboard'" -ForegroundColor White

Write-Host "`n🔍 If Dashboard is Missing:" -ForegroundColor Yellow
Write-Host "1. Go to Dashboards → Import" -ForegroundColor White
Write-Host "2. Upload: monitoring/grafana/dashboards/calculator-api-dashboard.json" -ForegroundColor White
Write-Host "3. Select Prometheus as datasource" -ForegroundColor White
Write-Host "4. Click 'Import'" -ForegroundColor White

Write-Host "`n🧪 Test Prometheus Connection:" -ForegroundColor Cyan
Write-Host "1. Go to Explore (compass icon)" -ForegroundColor White
Write-Host "2. Select Prometheus datasource" -ForegroundColor White
Write-Host "3. Try this query: up{job='calculator-api'}" -ForegroundColor White
Write-Host "4. Click 'Run Query'" -ForegroundColor White

Write-Host "`n🚀 Opening Grafana..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host "`n📚 Troubleshooting Commands:" -ForegroundColor Cyan
Write-Host "   • kubectl logs -n calculator-app -l app=grafana" -ForegroundColor Gray
Write-Host "   • kubectl get configmaps -n calculator-app" -ForegroundColor Gray
Write-Host "   • kubectl describe pod -n calculator-app -l app=grafana" -ForegroundColor Gray 