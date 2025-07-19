# Simple Kubernetes Pod Monitor
# Monitors all pods in the calculator-app namespace

param(
    [int]$RefreshInterval = 5
)

Clear-Host
Write-Host "Kubernetes Pod Monitoring Dashboard" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host "Namespace: calculator-app" -ForegroundColor Cyan
Write-Host "Refresh Interval: $RefreshInterval seconds" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to exit" -ForegroundColor Red
Write-Host ""

function Show-PodStatus {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "`nPod Status - $timestamp" -ForegroundColor Magenta
    Write-Host "====================================" -ForegroundColor Magenta
    
    # Get all pods
    kubectl get pods -n calculator-app
}

function Show-ResourceUsage {
    Write-Host "`nResource Usage:" -ForegroundColor Magenta
    Write-Host "====================================" -ForegroundColor Magenta
    
    # Get resource usage
    kubectl top pods -n calculator-app
}

function Show-HPAStatus {
    Write-Host "`nAuto-Scaling Status:" -ForegroundColor Magenta
    Write-Host "====================================" -ForegroundColor Magenta
    
    # Get HPA status
    kubectl get hpa -n calculator-app
}

function Show-ServiceStatus {
    Write-Host "`nService Status:" -ForegroundColor Magenta
    Write-Host "====================================" -ForegroundColor Magenta
    
    # Get services
    kubectl get services -n calculator-app
}

function Show-NodeStatus {
    Write-Host "`nNode Resources:" -ForegroundColor Magenta
    Write-Host "====================================" -ForegroundColor Magenta
    
    # Get node resources
    kubectl top nodes
}

# Main monitoring loop
do {
    try {
        Show-PodStatus
        Show-ResourceUsage
        Show-HPAStatus
        Show-ServiceStatus
        Show-NodeStatus
        
        Write-Host "`n" + ("=" * 50) -ForegroundColor Gray
        Write-Host "Next refresh in $RefreshInterval seconds... (Ctrl+C to exit)" -ForegroundColor Gray
        
        Start-Sleep -Seconds $RefreshInterval
        Clear-Host
    } catch {
        Write-Host "Error during monitoring: $($_.Exception.Message)" -ForegroundColor Red
        Start-Sleep -Seconds 2
    }
} while ($true)

Write-Host "`nMonitoring completed!" -ForegroundColor Green 