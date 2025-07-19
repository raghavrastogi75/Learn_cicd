#!/usr/bin/env python3
"""
Production Deployment Test Script

This script helps you understand and test the production deployment process.
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def check_current_status():
    """Check current git and workflow status"""
    print_section("Current Status Check")
    
    # Check current branch
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        print(f"Current Branch: {current_branch}")
    except subprocess.CalledProcessError:
        print("❌ Could not determine current branch")
        return False
    
    # Check for uncommitted changes
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  There are uncommitted changes")
            print("   Please commit or stash changes before deployment")
            return False
        else:
            print("✅ No uncommitted changes")
    except subprocess.CalledProcessError:
        print("❌ Could not check git status")
        return False
    
    return True

def explain_production_deployment():
    """Explain the production deployment process"""
    print_section("Production Deployment Process")
    
    print("""
🎯 Production Deployment Flow:

1. 📝 Manual Trigger Required
   - Go to GitHub repository → Actions tab
   - Click "CI/CD Pipeline" workflow
   - Click "Run workflow" button
   - Select "production" from environment dropdown
   - Click "Run workflow"

2. 🔄 Workflow Execution Order:
   - Lint & Format Check ✅
   - Unit Tests ✅
   - Integration Tests ✅
   - Security Scan ✅
   - Build Docker Image ✅ (Now supports manual trigger)
   - Production Deployment ✅

3. 🚀 Production Deployment:
   - Environment: Production
   - Database: calculator_prod
   - Port: 8082
   - Debug: Disabled
   - Rate Limit: 60/min
   - Safety Checks: Maximum
    """)

def show_manual_deployment_steps():
    """Show step-by-step manual deployment instructions"""
    print_section("Manual Production Deployment Steps")
    
    print("""
📋 Step-by-Step Instructions:

1. 🌐 Open GitHub Repository
   - Go to: https://github.com/raghavrastogi75/Learn_cicd

2. 📊 Navigate to Actions
   - Click on "Actions" tab in the repository

3. 🔧 Select Workflow
   - Click on "CI/CD Pipeline" workflow

4. ▶️ Run Workflow
   - Click "Run workflow" button (blue button on the right)

5. ⚙️ Configure Deployment
   - Environment: Select "production" from dropdown
   - Branch: Leave as "master" (default)
   - Click "Run workflow" button

6. 📈 Monitor Progress
   - Watch the workflow execution
   - Check each job status
   - Verify production deployment completes

7. ✅ Verify Deployment
   - Check deployment logs
   - Verify environment differences
   - Test production functionality
    """)

def check_workflow_conditions():
    """Check if workflow conditions are met"""
    print_section("Workflow Conditions Check")
    
    # Check if we're on a valid branch
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        
        print(f"Current Branch: {current_branch}")
        
        if current_branch in ['master', 'develop']:
            print("✅ Valid branch for deployment")
        else:
            print("⚠️  Consider switching to master or develop branch")
            
    except subprocess.CalledProcessError:
        print("❌ Could not determine current branch")
    
    # Check if we have the latest changes
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("❌ Uncommitted changes detected")
            print("   Please commit changes before deployment")
        else:
            print("✅ No uncommitted changes")
            
    except subprocess.CalledProcessError:
        print("❌ Could not check git status")

def show_troubleshooting_tips():
    """Show troubleshooting tips"""
    print_section("Troubleshooting Tips")
    
    print("""
🔧 Common Issues and Solutions:

1. ❌ Build Job Skipped
   - Issue: Build job doesn't run on manual trigger
   - Solution: ✅ Fixed - Build now supports workflow_dispatch

2. ❌ Production Deployment Skipped
   - Issue: Production deployment doesn't run
   - Solution: Make sure to select "production" in environment dropdown

3. ❌ Permission Denied
   - Issue: GHCR access denied
   - Solution: ✅ Fixed - Added proper permissions

4. ❌ Environment Not Found
   - Issue: GitHub environment not configured
   - Solution: Check repository settings → Environments

5. ❌ Tests Failing
   - Issue: Unit or integration tests failing
   - Solution: Fix tests before deployment
    """)

def main():
    """Main function"""
    print_header("Production Deployment Test")
    
    # Check current status
    if not check_current_status():
        print("\n❌ Status check failed. Please fix issues before deployment.")
        return
    
    # Explain the process
    explain_production_deployment()
    
    # Show manual steps
    show_manual_deployment_steps()
    
    # Check conditions
    check_workflow_conditions()
    
    # Show troubleshooting
    show_troubleshooting_tips()
    
    print("\n" + "="*60)
    print("✅ Production deployment test completed!")
    print("🚀 Ready to deploy to production!")
    print("="*60)

if __name__ == "__main__":
    main() 