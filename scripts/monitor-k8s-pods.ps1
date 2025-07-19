# Kubernetes Pod Monitoring Dashboard
# Monitors all pods in the calculator-app namespace with real-time metrics

param(
    [int]$RefreshInterval = 5,  # Refresh every 5 seconds
    [switch]$Continuous = $true
)

Clear-Host
Write-Host "🚀 Kubernetes Pod Monitoring Dashboard" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Namespace: calculator-app" -ForegroundColor Cyan
Write-Host "Refresh Interval: $RefreshInterval seconds" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to exit" -ForegroundColor Red
Write-Host ""

function Show-PodMetrics {
    param()
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "`n📊 Pod Status - $timestamp" -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
    
    # Get all pods with detailed info
    $pods = kubectl get pods -n calculator-app -o json | ConvertFrom-Json
    
    # Get resource usage
    $metrics = kubectl top pods -n calculator-app --no-headers 2>$null | ForEach-Object {
        $parts = $_ -split '\s+'
        @{
            Name = $parts[0]
            CPU = $parts[1]
            Memory = $parts[2]
        }
    }
    
    # Create metrics lookup
    $metricsLookup = @{}
    $metrics | ForEach-Object { $metricsLookup[$_.Name] = $_ }
    
    # Display API pods first
    $apiPods = $pods.items | Where-Object { $_.metadata.labels.app -eq "calculator-api" }
    $otherPods = $pods.items | Where-Object { $_.metadata.labels.app -ne "calculator-api" }
    
    Write-Host "`nAPI Pods ($($apiPods.Count) replicas):" -ForegroundColor Yellow
    Write-Host "Name".PadRight(35) + "Status".PadRight(10) + "CPU".PadRight(10) + "Memory".PadRight(12) + "Age".PadRight(10) + "IP" -ForegroundColor Cyan
    Write-Host ("-" * 35) + ("-" * 10) + ("-" * 10) + ("-" * 12) + ("-" * 10) + ("-" * 15) -ForegroundColor Gray
    
    foreach ($pod in $apiPods | Sort-Object metadata.name) {
        $name = $pod.metadata.name
        $status = $pod.status.phase
        $ready = "$($pod.status.containerStatuses.ready | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count)/$($pod.status.containerStatuses.Count)"
        $age = $pod.metadata.creationTimestamp
        $ip = $pod.status.podIP
        
        # Get metrics
        $metric = $metricsLookup[$name]
        $cpu = if ($metric) { $metric.CPU } else { "N/A" }
        $memory = if ($metric) { $metric.Memory } else { "N/A" }
        
        # Color coding
        $statusColor = if ($status -eq "Running") { "Green" } else { "Red" }
        $readyColor = if ($ready -like "*/1") { "Green" } else { "Red" }
        
        Write-Host $name.PadRight(35) -NoNewline -ForegroundColor White
        Write-Host $ready.PadRight(10) -NoNewline -ForegroundColor $readyColor
        Write-Host $cpu.PadRight(10) -NoNewline -ForegroundColor Yellow
        Write-Host $memory.PadRight(12) -NoNewline -ForegroundColor Yellow
        Write-Host $age.PadRight(10) -NoNewline -ForegroundColor Gray
        Write-Host $ip -ForegroundColor Cyan
    }
    
    # Display other pods
    Write-Host "`nDatabase and Cache Pods:" -ForegroundColor Yellow
    Write-Host "Name".PadRight(35) + "Status".PadRight(10) + "CPU".PadRight(10) + "Memory".PadRight(12) + "Age".PadRight(10) + "IP" -ForegroundColor Cyan
    Write-Host ("-" * 35) + ("-" * 10) + ("-" * 10) + ("-" * 12) + ("-" * 10) + ("-" * 15) -ForegroundColor Gray
    
    foreach ($pod in $otherPods | Sort-Object metadata.name) {
        $name = $pod.metadata.name
        $status = $pod.status.phase
        $ready = "$($pod.status.containerStatuses.ready | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count)/$($pod.status.containerStatuses.Count)"
        $age = $pod.metadata.creationTimestamp
        $ip = $pod.status.podIP
        
        # Get metrics
        $metric = $metricsLookup[$name]
        $cpu = if ($metric) { $metric.CPU } else { "N/A" }
        $memory = if ($metric) { $metric.Memory } else { "N/A" }
        
        # Color coding
        $statusColor = if ($status -eq "Running") { "Green" } else { "Red" }
        $readyColor = if ($ready -like "*/1") { "Green" } else { "Red" }
        
        Write-Host $name.PadRight(35) -NoNewline -ForegroundColor White
        Write-Host $ready.PadRight(10) -NoNewline -ForegroundColor $readyColor
        Write-Host $cpu.PadRight(10) -NoNewline -ForegroundColor Yellow
        Write-Host $memory.PadRight(12) -NoNewline -ForegroundColor Yellow
        Write-Host $age.PadRight(10) -NoNewline -ForegroundColor Gray
        Write-Host $ip -ForegroundColor Cyan
    }
}

function Show-HPAMetrics {
    param()
    
    Write-Host "`n📈 Auto-Scaling Status:" -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
    
    try {
        $hpa = kubectl get hpa calculator-api-hpa -n calculator-app -o json | ConvertFrom-Json
        
        $currentReplicas = $hpa.status.currentReplicas
        $desiredReplicas = $hpa.status.desiredReplicas
        $minReplicas = $hpa.spec.minReplicas
        $maxReplicas = $hpa.spec.maxReplicas
        
        Write-Host "Current Replicas: $currentReplicas" -ForegroundColor Cyan
        Write-Host "Desired Replicas: $desiredReplicas" -ForegroundColor Cyan
        Write-Host "Min Replicas: $minReplicas" -ForegroundColor Green
        Write-Host "Max Replicas: $maxReplicas" -ForegroundColor Red
        
        # Show metrics
        if ($hpa.status.currentMetrics) {
            Write-Host "`nMetrics:" -ForegroundColor Yellow
            foreach ($metric in $hpa.status.currentMetrics) {
                $resource = $metric.resource.name
                $current = $metric.resource.current.averageUtilization
                $target = $metric.resource.target.averageUtilization
                $status = if ($current -gt $target) { "Above Target" } else { "Normal" }
                $color = if ($current -gt $target) { "Red" } else { "Green" }
                
                Write-Host "  $resource`: $current% / $target% $status" -ForegroundColor $color
            }
        }
    } catch {
        Write-Host "Unable to get HPA metrics" -ForegroundColor Red
    }
}

function Show-ServiceMetrics {
    param()
    
    Write-Host "`n🌐 Service Status:" -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
    
    try {
        $services = kubectl get services -n calculator-app -o json | ConvertFrom-Json
        
        Write-Host "Name".PadRight(20) + "Type".PadRight(10) + "Cluster-IP".PadRight(15) + "Ports" -ForegroundColor Cyan
        Write-Host ("-" * 20) + ("-" * 10) + ("-" * 15) + ("-" * 20) -ForegroundColor Gray
        
        foreach ($svc in $services.items) {
            $name = $svc.metadata.name
            $type = $svc.spec.type
            $clusterIP = $svc.spec.clusterIP
            $ports = ($svc.spec.ports | ForEach-Object { "$($_.port):$($_.targetPort)" }) -join ", "
            
            Write-Host $name.PadRight(20) -NoNewline -ForegroundColor White
            Write-Host $type.PadRight(10) -NoNewline -ForegroundColor Yellow
            Write-Host $clusterIP.PadRight(15) -NoNewline -ForegroundColor Cyan
            Write-Host $ports -ForegroundColor Gray
        }
    } catch {
        Write-Host "Unable to get service metrics" -ForegroundColor Red
    }
}

function Show-NodeMetrics {
    param()
    
    Write-Host "`n🖥️ Node Resources:" -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
    
    try {
        $nodes = kubectl top nodes --no-headers 2>$null | ForEach-Object {
            $parts = $_ -split '\s+'
            @{
                Name = $parts[0]
                CPU = $parts[1]
                Memory = $parts[2]
                CPUPercent = $parts[3]
                MemoryPercent = $parts[4]
            }
        }
        
        Write-Host "Node".PadRight(20) + "CPU".PadRight(10) + "Memory".PadRight(12) + "CPU%".PadRight(8) + "Memory%" -ForegroundColor Cyan
        Write-Host ("-" * 20) + ("-" * 10) + ("-" * 12) + ("-" * 8) + ("-" * 10) -ForegroundColor Gray
        
        foreach ($node in $nodes) {
            $cpuColor = if ([int]$node.CPUPercent -gt 80) { "Red" } elseif ([int]$node.CPUPercent -gt 60) { "Yellow" } else { "Green" }
            $memColor = if ([int]$node.MemoryPercent -gt 80) { "Red" } elseif ([int]$node.MemoryPercent -gt 60) { "Yellow" } else { "Green" }
            
            Write-Host $node.Name.PadRight(20) -NoNewline -ForegroundColor White
            Write-Host $node.CPU.PadRight(10) -NoNewline -ForegroundColor $cpuColor
            Write-Host $node.Memory.PadRight(12) -NoNewline -ForegroundColor $memColor
            Write-Host $node.CPUPercent.PadRight(8) -NoNewline -ForegroundColor $cpuColor
            Write-Host $node.MemoryPercent -ForegroundColor $memColor
        }
    } catch {
        Write-Host "Unable to get node metrics" -ForegroundColor Red
    }
}

# Main monitoring loop
do {
    try {
        Show-PodMetrics
        Show-HPAMetrics
        Show-ServiceMetrics
        Show-NodeMetrics
        
        Write-Host "`n" + ("=" * 60) -ForegroundColor Gray
        Write-Host "Next refresh in $RefreshInterval seconds... (Ctrl+C to exit)" -ForegroundColor Gray
        
        if ($Continuous) {
            Start-Sleep -Seconds $RefreshInterval
            Clear-Host
        } else {
            break
        }
    } catch {
        Write-Host "Error during monitoring: $($_.Exception.Message)" -ForegroundColor Red
        Start-Sleep -Seconds 2
    }
} while ($Continuous)

Write-Host "`n🎉 Monitoring completed!" -ForegroundColor Green 