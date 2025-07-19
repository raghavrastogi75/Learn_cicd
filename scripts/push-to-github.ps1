#!/usr/bin/env pwsh

Write-Host "🚀 Push to GitHub Script" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan

Write-Host "`n📋 Steps to Push to GitHub:" -ForegroundColor Yellow

Write-Host "`n1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   • Go to https://github.com/new" -ForegroundColor Gray
Write-Host "   • Repository name: calculator-api-k8s" -ForegroundColor Gray
Write-Host "   • Description: Calculator API with Kubernetes deployment and monitoring" -ForegroundColor Gray
Write-Host "   • Make it Public or Private (your choice)" -ForegroundColor Gray
Write-Host "   • Don't initialize with README (we already have one)" -ForegroundColor Gray
Write-Host "   • Click 'Create repository'" -ForegroundColor Gray

Write-Host "`n2. Add the remote origin:" -ForegroundColor White
Write-Host "   Replace YOUR_USERNAME with your GitHub username:" -ForegroundColor Gray
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/calculator-api-k8s.git" -ForegroundColor Cyan

Write-Host "`n3. Push to GitHub:" -ForegroundColor White
Write-Host "   git push -u origin master" -ForegroundColor Cyan

Write-Host "`n4. Verify the push:" -ForegroundColor White
Write-Host "   • Go to your GitHub repository" -ForegroundColor Gray
Write-Host "   • You should see all 55 files uploaded" -ForegroundColor Gray
Write-Host "   • The README.md should display nicely" -ForegroundColor Gray

Write-Host "`n📊 What's Being Pushed:" -ForegroundColor Yellow
Write-Host "   • 55 files total" -ForegroundColor Gray
Write-Host "   • Calculator API with FastAPI" -ForegroundColor Gray
Write-Host "   • Kubernetes deployment manifests" -ForegroundColor Gray
Write-Host "   • Prometheus & Grafana monitoring" -ForegroundColor Gray
Write-Host "   • CI/CD pipeline configuration" -ForegroundColor Gray
Write-Host "   • Comprehensive documentation" -ForegroundColor Gray
Write-Host "   • Test suites and scripts" -ForegroundColor Gray

Write-Host "`n🎯 Repository Features:" -ForegroundColor Yellow
Write-Host "   ✅ Production-ready Calculator API" -ForegroundColor Green
Write-Host "   ✅ Kubernetes auto-scaling (3-10 pods)" -ForegroundColor Green
Write-Host "   ✅ Prometheus metrics collection" -ForegroundColor Green
Write-Host "   ✅ Grafana dashboards" -ForegroundColor Green
Write-Host "   ✅ PostgreSQL database" -ForegroundColor Green
Write-Host "   ✅ Redis caching" -ForegroundColor Green
Write-Host "   ✅ Traffic generation for testing" -ForegroundColor Green
Write-Host "   ✅ Comprehensive documentation" -ForegroundColor Green

Write-Host "`n🔧 After Pushing:" -ForegroundColor Yellow
Write-Host "   • Enable GitHub Actions in your repository" -ForegroundColor Gray
Write-Host "   • Set up branch protection rules" -ForegroundColor Gray
Write-Host "   • Configure deployment secrets if needed" -ForegroundColor Gray
Write-Host "   • Share the repository URL with others!" -ForegroundColor Gray

Write-Host "`n💡 Pro Tips:" -ForegroundColor Cyan
Write-Host "   • Add topics to your repository: kubernetes, fastapi, prometheus, grafana, monitoring" -ForegroundColor Gray
Write-Host "   • Create issues for future enhancements" -ForegroundColor Gray
Write-Host "   • Set up GitHub Pages for documentation" -ForegroundColor Gray
Write-Host "   • Add a LICENSE file if needed" -ForegroundColor Gray

Write-Host "`n🚀 Ready to push? Run these commands:" -ForegroundColor Green
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/calculator-api-k8s.git" -ForegroundColor Cyan
Write-Host "   git push -u origin master" -ForegroundColor Cyan 