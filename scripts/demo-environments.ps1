# Environment Demonstration Script
# Shows how to differentiate between development, staging, and production environments

Write-Host "🌍 Multi-Environment CI/CD Pipeline Demonstration" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Function to display environment info
function Show-EnvironmentInfo {
    param(
        [string]$Environment,
        [string]$Color
    )
    
    Write-Host "`n📋 $Environment Environment" -ForegroundColor $Color
    Write-Host "-" * 40 -ForegroundColor $Color
    
    if ($Environment.ToLower() -eq "development") {
        Write-Host "🔧 Purpose: Local development and testing" -ForegroundColor White
        Write-Host "🔧 Debug: Enabled" -ForegroundColor White
        Write-Host "🔧 Log Level: DEBUG" -ForegroundColor White
        Write-Host "🔧 Rate Limit: 1000/min" -ForegroundColor White
        Write-Host "🔧 Database: calculator_dev" -ForegroundColor White
        Write-Host "🔧 Namespace: calculator-dev" -ForegroundColor White
        Write-Host "🔧 Port: 8080" -ForegroundColor White
    }
    elseif ($Environment.ToLower() -eq "staging") {
        Write-Host "🔧 Purpose: Integration testing and validation" -ForegroundColor White
        Write-Host "🔧 Debug: Disabled" -ForegroundColor White
        Write-Host "🔧 Log Level: INFO" -ForegroundColor White
        Write-Host "🔧 Rate Limit: 100/min" -ForegroundColor White
        Write-Host "🔧 Database: calculator_staging" -ForegroundColor White
        Write-Host "🔧 Namespace: calculator-staging" -ForegroundColor White
        Write-Host "🔧 Port: 8081" -ForegroundColor White
    }
    elseif ($Environment.ToLower() -eq "production") {
        Write-Host "🔧 Purpose: Live user traffic" -ForegroundColor White
        Write-Host "🔧 Debug: Disabled" -ForegroundColor White
        Write-Host "🔧 Log Level: WARNING" -ForegroundColor White
        Write-Host "🔧 Rate Limit: 60/min" -ForegroundColor White
        Write-Host "🔧 Database: calculator_prod" -ForegroundColor White
        Write-Host "🔧 Namespace: calculator-prod" -ForegroundColor White
        Write-Host "🔧 Port: 8082" -ForegroundColor White
    }
}

# Show environment differences
Show-EnvironmentInfo "Development" "Green"
Show-EnvironmentInfo "Staging" "Yellow"
Show-EnvironmentInfo "Production" "Red"

Write-Host "`n🚀 Deployment Pipeline Simulation" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Simulate the deployment process
Write-Host "`n1️⃣ Development Phase" -ForegroundColor Green
Write-Host "   - Feature development (abs_diff)" -ForegroundColor White
Write-Host "   - Unit tests" -ForegroundColor White
Write-Host "   - Local testing" -ForegroundColor White
Write-Host "   - Code review" -ForegroundColor White

Write-Host "`n2️⃣ CI/CD Pipeline" -ForegroundColor Yellow
Write-Host "   - GitHub Actions triggers" -ForegroundColor White
Write-Host "   - Code quality checks" -ForegroundColor White
Write-Host "   - Security scanning" -ForegroundColor White
Write-Host "   - Integration tests" -ForegroundColor White
Write-Host "   - Docker image build" -ForegroundColor White

Write-Host "`n3️⃣ Staging Deployment" -ForegroundColor Yellow
Write-Host "   - Deploy to staging environment" -ForegroundColor White
Write-Host "   - Integration testing" -ForegroundColor White
Write-Host "   - Performance testing" -ForegroundColor White
Write-Host "   - User acceptance testing" -ForegroundColor White

Write-Host "`n4️⃣ Production Deployment" -ForegroundColor Red
Write-Host "   - Safety checks" -ForegroundColor White
Write-Host "   - Final testing" -ForegroundColor White
Write-Host "   - Rolling deployment" -ForegroundColor White
Write-Host "   - Health monitoring" -ForegroundColor White

Write-Host "`n🔧 Environment-Specific Configurations" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Show configuration differences
$configs = @{
    "Development" = @{
        "DEBUG" = "true"
        "LOG_LEVEL" = "DEBUG"
        "RATE_LIMIT" = "1000"
        "FEATURES" = "All enabled"
        "SAFETY_CHECKS" = "Minimal"
    }
    "Staging" = @{
        "DEBUG" = "false"
        "LOG_LEVEL" = "INFO"
        "RATE_LIMIT" = "100"
        "FEATURES" = "All enabled"
        "SAFETY_CHECKS" = "Moderate"
    }
    "Production" = @{
        "DEBUG" = "false"
        "LOG_LEVEL" = "WARNING"
        "RATE_LIMIT" = "60"
        "FEATURES" = "All enabled"
        "SAFETY_CHECKS" = "Maximum"
    }
}

foreach ($env in $configs.Keys) {
    Write-Host "`n📋 $env Configuration:" -ForegroundColor Blue
    foreach ($key in $configs[$env].Keys) {
        Write-Host "   $key`: $($configs[$env][$key])" -ForegroundColor White
    }
}

Write-Host "`n🎯 Key Differences Summary" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan

Write-Host "🔒 Security:" -ForegroundColor Yellow
Write-Host "   - Dev: Debug enabled, loose rate limits" -ForegroundColor White
Write-Host "   - Staging: Debug disabled, moderate limits" -ForegroundColor White
Write-Host "   - Prod: Debug disabled, strict limits" -ForegroundColor White

Write-Host "`n📊 Monitoring:" -ForegroundColor Yellow
Write-Host "   - Dev: Detailed logging, development metrics" -ForegroundColor White
Write-Host "   - Staging: Standard logging, performance metrics" -ForegroundColor White
Write-Host "   - Prod: Minimal logging, production metrics" -ForegroundColor White

Write-Host "`n🚀 Deployment:" -ForegroundColor Yellow
Write-Host "   - Dev: Quick deployment, no safety checks" -ForegroundColor White
Write-Host "   - Staging: Automated deployment, basic checks" -ForegroundColor White
Write-Host "   - Prod: Manual approval, comprehensive checks" -ForegroundColor White

Write-Host "`n💡 Best Practices Demonstrated:" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

Write-Host "✅ Environment Isolation" -ForegroundColor Green
Write-Host "   - Separate namespaces and databases" -ForegroundColor White

Write-Host "✅ Configuration Management" -ForegroundColor Green
Write-Host "   - Environment-specific ConfigMaps and Secrets" -ForegroundColor White

Write-Host "✅ Progressive Deployment" -ForegroundColor Green
Write-Host "   - Dev → Staging → Production pipeline" -ForegroundColor White

Write-Host "✅ Safety Measures" -ForegroundColor Green
Write-Host "   - Increasing safety checks per environment" -ForegroundColor White

Write-Host "✅ Monitoring & Observability" -ForegroundColor Green
Write-Host "   - Environment-appropriate logging and metrics" -ForegroundColor White

Write-Host "`n🎉 Environment differentiation is now complete!" -ForegroundColor Green
Write-Host "   You can deploy to different environments using:" -ForegroundColor White
Write-Host "   - scripts/deploy-dev.ps1" -ForegroundColor Blue
Write-Host "   - scripts/deploy-staging.ps1" -ForegroundColor Blue
Write-Host "   - scripts/deploy-prod.ps1" -ForegroundColor Blue 