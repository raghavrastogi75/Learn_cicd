# Test Kubernetes Scaling Script
# This script tests the auto-scaling capabilities of your Kubernetes deployment

param(
    [int]$Duration = 300,  # 5 minutes default
    [int]$MaxRPS = 50      # Maximum requests per second
)

Write-Host "🚀 Testing Kubernetes Auto-Scaling" -ForegroundColor Green
Write-Host "Duration: $Duration seconds" -ForegroundColor Yellow
Write-Host "Max RPS: $MaxRPS" -ForegroundColor Yellow
Write-Host ""

# Check if kubectl is available
try {
    $kubectlVersion = kubectl version --client --short
    Write-Host "✅ kubectl found: $kubectlVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ kubectl not found. Please install kubectl first." -ForegroundColor Red
    exit 1
}

# Check if namespace exists
try {
    $namespace = kubectl get namespace calculator-app --no-headers -o custom-columns=":metadata.name" 2>$null
    if ($namespace -eq "calculator-app") {
        Write-Host "✅ calculator-app namespace found" -ForegroundColor Green
    } else {
        Write-Host "❌ calculator-app namespace not found. Please deploy first." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error checking namespace" -ForegroundColor Red
    exit 1
}

# Function to get current replica count
function Get-ReplicaCount {
    $replicas = kubectl get deployment calculator-api -n calculator-app -o jsonpath='{.spec.replicas}' 2>$null
    return $replicas
}

# Function to get HPA status
function Get-HPAStatus {
    $hpa = kubectl get hpa calculator-api-hpa -n calculator-app -o jsonpath='{.status.currentReplicas}' 2>$null
    return $hpa
}

# Function to generate traffic
function Start-TrafficGeneration {
    param([int]$RPS, [int]$Duration)
    
    Write-Host "🔥 Generating traffic at $RPS RPS for $Duration seconds..." -ForegroundColor Yellow
    
    $operations = @('add', 'subtract', 'multiply', 'divide', 'power', 'sqrt')
    $delay = 1.0 / $RPS
    $endTime = (Get-Date).AddSeconds($Duration)
    $requestCount = 0
    
    while ((Get-Date) -lt $endTime) {
        $operation = $operations | Get-Random
        
        if ($operation -eq 'sqrt') {
            $a = Get-Random -Minimum 1 -Maximum 1000
            $body = @{operation=$operation; a=$a} | ConvertTo-Json
        } else {
            $a = Get-Random -Minimum -1000 -Maximum 1000
            $b = Get-Random -Minimum -1000 -Maximum 1000
            $body = @{operation=$operation; a=$a; b=$b} | ConvertTo-Json
        }
        
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8080/api/calculator/calculate" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 5
            $requestCount++
            if ($requestCount % 10 -eq 0) {
                Write-Host "  Request $requestCount`: $operation" -ForegroundColor Gray
            }
        } catch {
            Write-Host "  Request failed: $($_.Exception.Message)" -ForegroundColor Red
        }
        
        Start-Sleep -Seconds $delay
    }
    
    return $requestCount
}

# Function to monitor scaling
function Start-ScalingMonitor {
    param([int]$Duration)
    
    Write-Host "📊 Monitoring scaling for $Duration seconds..." -ForegroundColor Cyan
    
    $endTime = (Get-Date).AddSeconds($Duration)
    $lastReplicas = 0
    
    while ((Get-Date) -lt $endTime) {
        $currentReplicas = Get-ReplicaCount
        $hpaReplicas = Get-HPAStatus
        
        if ($currentReplicas -ne $lastReplicas) {
            Write-Host "$(Get-Date -Format 'HH:mm:ss'): Replicas changed from $lastReplicas to $currentReplicas (HPA: $hpaReplicas)" -ForegroundColor Green
            $lastReplicas = $currentReplicas
        }
        
        Start-Sleep -Seconds 5
    }
}

# Main execution
Write-Host "📈 Starting scaling test..." -ForegroundColor Green

# Get initial state
$initialReplicas = Get-ReplicaCount
Write-Host "Initial replicas: $initialReplicas" -ForegroundColor Cyan

# Start monitoring in background
$monitorJob = Start-Job -ScriptBlock {
    param($Duration)
    $endTime = (Get-Date).AddSeconds($Duration)
    while ((Get-Date) -lt $endTime) {
        $replicas = kubectl get deployment calculator-api -n calculator-app -o jsonpath='{.spec.replicas}' 2>$null
        $hpa = kubectl get hpa calculator-api-hpa -n calculator-app -o jsonpath='{.status.currentReplicas}' 2>$null
        Write-Output "$(Get-Date -Format 'HH:mm:ss'): Replicas=$replicas, HPA=$hpa"
        Start-Sleep -Seconds 5
    }
} -ArgumentList $Duration

# Phase 1: Low traffic (should not scale)
Write-Host "`n🌱 Phase 1: Low traffic (5 RPS)" -ForegroundColor Yellow
$lowTrafficCount = Start-TrafficGeneration -RPS 5 -Duration 60

# Phase 2: Medium traffic (should scale up)
Write-Host "`n🔥 Phase 2: Medium traffic (20 RPS)" -ForegroundColor Yellow
$mediumTrafficCount = Start-TrafficGeneration -RPS 20 -Duration 60

# Phase 3: High traffic (should scale up more)
Write-Host "`n💥 Phase 3: High traffic (40 RPS)" -ForegroundColor Yellow
$highTrafficCount = Start-TrafficGeneration -RPS 40 -Duration 60

# Phase 4: Burst traffic (maximum scaling)
Write-Host "`n🚀 Phase 4: Burst traffic ($MaxRPS RPS)" -ForegroundColor Yellow
$burstTrafficCount = Start-TrafficGeneration -RPS $MaxRPS -Duration 60

# Wait for monitoring to complete
Wait-Job $monitorJob
$monitoringResults = Receive-Job $monitorJob
Remove-Job $monitorJob

# Get final state
$finalReplicas = Get-ReplicaCount
$finalHPA = Get-HPAStatus

# Display results
Write-Host "`n📊 Scaling Test Results" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green
Write-Host "Initial replicas: $initialReplicas" -ForegroundColor Cyan
Write-Host "Final replicas: $finalReplicas" -ForegroundColor Cyan
Write-Host "Final HPA replicas: $finalHPA" -ForegroundColor Cyan
Write-Host ""
Write-Host "Traffic generated:" -ForegroundColor Yellow
Write-Host "  Low traffic: $lowTrafficCount requests" -ForegroundColor White
Write-Host "  Medium traffic: $mediumTrafficCount requests" -ForegroundColor White
Write-Host "  High traffic: $highTrafficCount requests" -ForegroundColor White
Write-Host "  Burst traffic: $burstTrafficCount requests" -ForegroundColor White
Write-Host "  Total: $($lowTrafficCount + $mediumTrafficCount + $highTrafficCount + $burstTrafficCount) requests" -ForegroundColor Green

Write-Host "`n📈 Scaling Timeline:" -ForegroundColor Cyan
$monitoringResults | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }

# Check if scaling worked
if ($finalReplicas -gt $initialReplicas) {
    Write-Host "`n✅ Auto-scaling test PASSED!" -ForegroundColor Green
    Write-Host "   Replicas increased from $initialReplicas to $finalReplicas" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ Auto-scaling test INCONCLUSIVE" -ForegroundColor Yellow
    Write-Host "   Replicas remained at $initialReplicas" -ForegroundColor Yellow
    Write-Host "   This might be normal if load wasn't high enough" -ForegroundColor Yellow
}

Write-Host "`n🎉 Scaling test completed!" -ForegroundColor Green 