#!/usr/bin/env pwsh

Write-Host "🎯 Grafana Access & Configuration Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Check if Grafana is running
Write-Host "`n📊 Checking Grafana status..." -ForegroundColor Yellow
$grafanaPod = kubectl get pods -n calculator-app -l app=grafana --no-headers -o custom-columns=":metadata.name" 2>$null

if ($grafanaPod) {
    $status = kubectl get pods -n calculator-app -l app=grafana --no-headers -o custom-columns=":status.phase"
    if ($status -eq "Running") {
        Write-Host "✅ Grafana is running!" -ForegroundColor Green
        
        # Check if port forwarding is already running
        $portForward = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
        if ($portForward) {
            Write-Host "✅ Port forwarding already active on port 3000" -ForegroundColor Green
        } else {
            Write-Host "🔄 Starting port forwarding..." -ForegroundColor Yellow
            Start-Process powershell -ArgumentList "-Command", "kubectl port-forward -n calculator-app svc/grafana 3000:3000" -WindowStyle Hidden
            Start-Sleep -Seconds 3
        }
        
        Write-Host "`n🌐 Grafana Access Information:" -ForegroundColor Cyan
        Write-Host "   URL: http://localhost:3000" -ForegroundColor White
        Write-Host "   Username: admin" -ForegroundColor White
        Write-Host "   Password: admin" -ForegroundColor White
        
        Write-Host "`n📋 Configuration Steps:" -ForegroundColor Cyan
        Write-Host "1. Open http://localhost:3000 in your browser" -ForegroundColor White
        Write-Host "2. Login with admin/admin" -ForegroundColor White
        Write-Host "3. The Prometheus datasource should be auto-configured" -ForegroundColor White
        Write-Host "4. Check 'Data Sources' in Configuration menu" -ForegroundColor White
        Write-Host "5. Import the Calculator API dashboard" -ForegroundColor White
        
        Write-Host "`n🔍 Quick Prometheus Queries to Test:" -ForegroundColor Cyan
        Write-Host "   • up{job='calculator-api'}" -ForegroundColor Gray
        Write-Host "   • rate(http_requests_total{job='calculator-api'}[5m])" -ForegroundColor Gray
        Write-Host "   • rate(http_requests_total{job='calculator-api', status=~'4..|5..'}[5m])" -ForegroundColor Gray
        
        Write-Host "`n🚀 Opening Grafana in browser..." -ForegroundColor Yellow
        Start-Process "http://localhost:3000"
        
    } else {
        Write-Host "❌ Grafana is not running. Status: $status" -ForegroundColor Red
        Write-Host "`n🔧 Troubleshooting:" -ForegroundColor Yellow
        Write-Host "1. Check pod logs: kubectl logs -n calculator-app -l app=grafana" -ForegroundColor Gray
        Write-Host "2. Check pod events: kubectl describe pod -n calculator-app -l app=grafana" -ForegroundColor Gray
        Write-Host "3. Restart deployment: kubectl rollout restart deployment/grafana -n calculator-app" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ Grafana pod not found!" -ForegroundColor Red
    Write-Host "`n🔧 Deploy Grafana:" -ForegroundColor Yellow
    Write-Host "kubectl apply -f infrastructure/kubernetes/monitoring.yml" -ForegroundColor Gray
}

Write-Host "`n📚 Useful Commands:" -ForegroundColor Cyan
Write-Host "   • kubectl get pods -n calculator-app -l app=grafana" -ForegroundColor Gray
Write-Host "   • kubectl logs -n calculator-app -l app=grafana" -ForegroundColor Gray
Write-Host "   • kubectl port-forward -n calculator-app svc/grafana 3000:3000" -ForegroundColor Gray
Write-Host "   • kubectl get configmaps -n calculator-app" -ForegroundColor Gray 