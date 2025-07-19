# Live Metrics Viewer for Calculator API
# Shows real-time metrics in the terminal

Write-Host "🚀 Live Metrics Viewer for Calculator API" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host ""

while ($true) {
    try {
        Clear-Host
        Write-Host "=== LIVE METRICS - $(Get-Date) ===" -ForegroundColor Green
        
        # Get metrics
        $metrics = Invoke-RestMethod -Uri "http://localhost:8000/metrics" -Method Get
        
        # HTTP Requests
        Write-Host "`n📊 HTTP REQUESTS:" -ForegroundColor Yellow
        $httpRequests = $metrics | Select-String "http_requests_total" | Select-Object -Last 3
        foreach ($request in $httpRequests) {
            Write-Host "  $($request.Line)" -ForegroundColor White
        }
        
        # Calculator Operations
        Write-Host "`n🧮 CALCULATOR OPERATIONS:" -ForegroundColor Yellow
        $operations = $metrics | Select-String "calculator_operations_total" | Select-Object -Last 6
        foreach ($op in $operations) {
            Write-Host "  $($op.Line)" -ForegroundColor White
        }
        
        # Response Times
        Write-Host "`n⏱️ RESPONSE TIMES:" -ForegroundColor Yellow
        $responseTimes = $metrics | Select-String "http_request_duration_seconds_count" | Select-Object -Last 2
        foreach ($time in $responseTimes) {
            Write-Host "  $($time.Line)" -ForegroundColor White
        }
        
        # Summary
        Write-Host "`n📈 SUMMARY:" -ForegroundColor Cyan
        $totalRequests = ($metrics | Select-String "http_requests_total.*status=\"200\"" | ForEach-Object { ($_ -split " ")[-1] } | Measure-Object -Sum).Sum
        $totalErrors = ($metrics | Select-String "http_requests_total.*status=\"[45]00\"" | ForEach-Object { ($_ -split " ")[-1] } | Measure-Object -Sum).Sum
        $errorRate = if ($totalRequests -gt 0) { [math]::Round(($totalErrors / ($totalRequests + $totalErrors)) * 100, 2) } else { 0 }
        
        Write-Host "  Total Requests: $totalRequests" -ForegroundColor Green
        Write-Host "  Total Errors: $totalErrors" -ForegroundColor Red
        Write-Host "  Error Rate: $errorRate%" -ForegroundColor $(if ($errorRate -gt 5) { "Red" } else { "Green" })
        
        Start-Sleep -Seconds 3
        
    } catch {
        Write-Host "❌ Error getting metrics: $($_.Exception.Message)" -ForegroundColor Red
        Start-Sleep -Seconds 5
    }
} 