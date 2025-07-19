# PowerShell Traffic Generator for Calculator API
# Run this script to generate continuous traffic

param(
    [int]$RequestsPerSecond = 5,
    [int]$Duration = 300  # 5 minutes default
)

Write-Host "🚀 Starting Traffic Generator" -ForegroundColor Green
Write-Host "Requests per second: $RequestsPerSecond" -ForegroundColor Yellow
Write-Host "Duration: $Duration seconds" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host ""

$operations = @('add', 'subtract', 'multiply', 'divide', 'power', 'sqrt')
$startTime = Get-Date
$requestCount = 0
$delay = 1.0 / $RequestsPerSecond

try {
    while ((Get-Date) - $startTime).TotalSeconds -lt $Duration) {
        $operation = $operations | Get-Random
        
        if ($operation -eq 'sqrt') {
            $a = Get-Random -Minimum 1 -Maximum 1000
            $body = @{operation=$operation; a=$a} | ConvertTo-Json
        } else {
            $a = Get-Random -Minimum -1000 -Maximum 1000
            $b = Get-Random -Minimum -1000 -Maximum 1000
            
            # Avoid division by zero
            if ($operation -eq 'divide' -and [Math]::Abs($b) -lt 0.001) {
                $b = if ($b -ge 0) { Get-Random -Minimum 1 -Maximum 100 } else { Get-Random -Minimum -100 -Maximum -1 }
            }
            
            $body = @{operation=$operation; a=$a; b=$b} | ConvertTo-Json
        }
        
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8000/api/calculator/calculate" -Method Post -Body $body -ContentType "application/json"
            $requestCount++
            Write-Host "Request $requestCount`: $operation" -ForegroundColor Green
        } catch {
            Write-Host "Request $requestCount`: Failed" -ForegroundColor Red
        }
        
        Start-Sleep -Seconds $delay
    }
} catch {
    Write-Host "`n🛑 Traffic generation stopped" -ForegroundColor Yellow
}

Write-Host "`n✅ Traffic generation completed!" -ForegroundColor Green
Write-Host "Total requests: $requestCount" -ForegroundColor Cyan
Write-Host "Average RPS: $([Math]::Round($requestCount / ((Get-Date) - $startTime).TotalSeconds, 2))" -ForegroundColor Cyan 