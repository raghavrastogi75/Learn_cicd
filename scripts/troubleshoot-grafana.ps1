#!/usr/bin/env pwsh

Write-Host "🔧 Grafana Troubleshooting Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

Write-Host "`n📊 Step 1: Check Grafana Pod Status" -ForegroundColor Yellow
kubectl get pods -n calculator-app -l app=grafana

Write-Host "`n📋 Step 2: Check Grafana Service" -ForegroundColor Yellow
kubectl get svc -n calculator-app -l app=grafana

Write-Host "`n🔍 Step 3: Check Grafana Logs" -ForegroundColor Yellow
kubectl logs -n calculator-app -l app=grafana --tail=5

Write-Host "`n🛠️ Step 4: Kill Existing Port Forwarding" -ForegroundColor Yellow
$processes = Get-Process | Where-Object {$_.ProcessName -eq "kubectl" -and $_.CommandLine -like "*port-forward*"}
if ($processes) {
    Write-Host "Found existing kubectl port-forward processes. Stopping them..." -ForegroundColor Red
    $processes | Stop-Process -Force
    Start-Sleep -Seconds 2
} else {
    Write-Host "No existing port-forward processes found." -ForegroundColor Green
}

Write-Host "`n🚀 Step 5: Start Fresh Port Forwarding" -ForegroundColor Yellow
Write-Host "Starting port forwarding in background..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-Command", "kubectl port-forward -n calculator-app svc/grafana 3000:3000" -WindowStyle Hidden

Write-Host "`n⏳ Step 6: Wait for Connection" -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`n🌐 Step 7: Test Connection" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Grafana is accessible! Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Grafana is not accessible. Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n📋 Manual Steps:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "2. Login with admin/admin" -ForegroundColor White
Write-Host "3. If still not working, try restarting Grafana:" -ForegroundColor White
Write-Host "   kubectl rollout restart deployment/grafana -n calculator-app" -ForegroundColor Gray

Write-Host "`n🔧 Alternative: Use Different Port" -ForegroundColor Yellow
Write-Host "If port 3000 is busy, try:" -ForegroundColor White
Write-Host "kubectl port-forward -n calculator-app svc/grafana 3001:3000" -ForegroundColor Gray
Write-Host "Then access: http://localhost:3001" -ForegroundColor Gray 