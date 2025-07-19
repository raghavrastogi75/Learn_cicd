# 🚀 Deployment Testing Guide

## Overview

This guide explains how to test different deployment scenarios in your CI/CD pipeline and understand why certain deployments might be skipped.

## 🔍 Understanding Deployment Triggers

### Automatic Deployments

| Environment | Trigger | Branch | Status |
|-------------|---------|--------|--------|
| **Development** | Push to `develop` | `develop` | Automatic |
| **Staging** | Push to `master` | `master` | Automatic |
| **Production** | Manual trigger | Any | Manual |

### Manual Deployments

| Environment | How to Trigger | When to Use |
|-------------|----------------|-------------|
| **Production** | GitHub Actions → Run workflow | After staging validation |
| **Staging** | GitHub Actions → Run workflow | For testing specific features |

## 🧪 Testing Different Scenarios

### 1. Test Development Deployment

```bash
# Create and switch to develop branch
git checkout -b develop

# Make a change
echo "# Development test" > dev-test.md
git add dev-test.md
git commit -m "Test: Development deployment"
git push origin develop
```

**Expected Result:**
- ✅ Development deployment runs
- ✅ All other jobs run normally
- ❌ Staging and Production deployments skipped

### 2. Test Staging Deployment

```bash
# Switch to master branch
git checkout master

# Make a change
echo "# Staging test" > staging-test.md
git add staging-test.md
git commit -m "Test: Staging deployment"
git push origin master
```

**Expected Result:**
- ✅ Staging deployment runs
- ✅ All other jobs run normally
- ❌ Development and Production deployments skipped

### 3. Test Production Deployment

**Manual Steps:**
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "CI/CD Pipeline" workflow
4. Click "Run workflow" button
5. Select "production" from the environment dropdown
6. Click "Run workflow"

**Expected Result:**
- ✅ Production deployment runs
- ✅ All other jobs run normally
- ❌ Development and Staging deployments skipped

## 🔧 Troubleshooting Skipped Deployments

### Common Reasons for Skipped Deployments

1. **Wrong Branch**
   - Development deployment only runs on `develop` branch
   - Staging deployment only runs on `master` branch

2. **Missing GitHub Environments**
   - If environments aren't configured, deployments might be skipped
   - Check GitHub repository settings → Environments

3. **Manual Trigger Required**
   - Production deployment requires manual workflow dispatch
   - Use GitHub Actions UI to trigger manually

### How to Check Deployment Status

```bash
# Check current branch
git branch --show-current

# Check recent commits
git log --oneline -5

# Check workflow status
# Go to GitHub → Actions → CI/CD Pipeline
```

## 📊 Monitoring Deployments

### GitHub Actions Dashboard

1. **Repository → Actions tab**
   - View all workflow runs
   - Check job status and logs
   - See which jobs were skipped and why

2. **Workflow Details**
   - Click on any workflow run
   - Expand job details to see logs
   - Check environment deployment status

### Environment-Specific Monitoring

| Environment | Log Level | Monitoring | Alerts |
|-------------|-----------|------------|--------|
| **Development** | DEBUG | Basic metrics | None |
| **Staging** | INFO | Performance metrics | Moderate |
| **Production** | WARNING | Full monitoring | Critical |

## 🎯 Best Practices

### 1. Branch Strategy
- Use `develop` for feature development
- Use `master` for staging and production releases
- Create feature branches from `develop`

### 2. Testing Strategy
- Test in development first
- Validate in staging before production
- Use manual production deployments for safety

### 3. Monitoring Strategy
- Monitor all environments
- Set up alerts for production
- Track deployment metrics

## 🚀 Quick Test Commands

```bash
# Test deployment flow locally
python scripts/test-deployment-flow.py

# Check current deployment status
git status
git branch --show-current

# Trigger staging deployment
echo "# Test $(date)" > test-$(date +%s).md
git add .
git commit -m "Test: Staging deployment $(date)"
git push origin master
```

## 📋 Deployment Checklist

### Before Deployment
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Branch strategy followed
- [ ] Environment configured

### During Deployment
- [ ] Monitor GitHub Actions
- [ ] Check deployment logs
- [ ] Verify environment differences
- [ ] Test functionality

### After Deployment
- [ ] Monitor application health
- [ ] Check metrics and logs
- [ ] Verify user experience
- [ ] Document any issues

## 🔗 Related Resources

- [Environment Differentiation Guide](environment-differentiation-guide.md)
- [Deployment Guide](deployment-guide.md)
- [Kubernetes Deployment Guide](kubernetes-deployment-guide.md)
- [Alerting Guide](alerting-guide.md)

---

**Note:** This guide assumes you have proper GitHub environments configured. If deployments are still being skipped, check your GitHub repository settings for environment configuration. 