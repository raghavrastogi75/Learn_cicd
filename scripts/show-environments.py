#!/usr/bin/env python3
"""
Environment Demonstration Script
Shows how to differentiate between development, staging, and production environments
"""

import os
import sys
from typing import Any, Dict


def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🌍 {title}")
    print(f"{'='*60}")


def print_environment_info(env_name: str, config: Dict[str, Any]):
    """Print environment information"""
    print(f"\n📋 {env_name.upper()} Environment")
    print("-" * 40)

    for key, value in config.items():
        print(f"🔧 {key}: {value}")


def main():
    """Main demonstration function"""

    print_header("Multi-Environment CI/CD Pipeline Demonstration")

    # Environment configurations
    environments = {
        "Development": {
            "Purpose": "Local development and testing",
            "Debug": "Enabled",
            "Log Level": "DEBUG",
            "Rate Limit": "1000/min",
            "Database": "calculator_dev",
            "Namespace": "calculator-dev",
            "Port": "8080",
            "Safety Checks": "Minimal",
        },
        "Staging": {
            "Purpose": "Integration testing and validation",
            "Debug": "Disabled",
            "Log Level": "INFO",
            "Rate Limit": "100/min",
            "Database": "calculator_staging",
            "Namespace": "calculator-staging",
            "Port": "8081",
            "Safety Checks": "Moderate",
        },
        "Production": {
            "Purpose": "Live user traffic",
            "Debug": "Disabled",
            "Log Level": "WARNING",
            "Rate Limit": "60/min",
            "Database": "calculator_prod",
            "Namespace": "calculator-prod",
            "Port": "8082",
            "Safety Checks": "Maximum",
        },
    }

    # Show environment differences
    for env_name, config in environments.items():
        print_environment_info(env_name, config)

    print_header("Deployment Pipeline Simulation")

    # Simulate the deployment process
    pipeline_steps = [
        (
            "1️⃣ Development Phase",
            [
                "Feature development (abs_diff)",
                "Unit tests",
                "Local testing",
                "Code review",
            ],
        ),
        (
            "2️⃣ CI/CD Pipeline",
            [
                "GitHub Actions triggers",
                "Code quality checks",
                "Security scanning",
                "Integration tests",
                "Docker image build",
            ],
        ),
        (
            "3️⃣ Staging Deployment",
            [
                "Deploy to staging environment",
                "Integration testing",
                "Performance testing",
                "User acceptance testing",
            ],
        ),
        (
            "4️⃣ Production Deployment",
            [
                "Safety checks",
                "Final testing",
                "Rolling deployment",
                "Health monitoring",
            ],
        ),
    ]

    for step_name, activities in pipeline_steps:
        print(f"\n{step_name}")
        for activity in activities:
            print(f"   - {activity}")

    print_header("Environment-Specific Configurations")

    # Show configuration differences
    configs = {
        "Development": {
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
            "RATE_LIMIT": "1000",
            "FEATURES": "All enabled",
            "SAFETY_CHECKS": "Minimal",
        },
        "Staging": {
            "DEBUG": "false",
            "LOG_LEVEL": "INFO",
            "RATE_LIMIT": "100",
            "FEATURES": "All enabled",
            "SAFETY_CHECKS": "Moderate",
        },
        "Production": {
            "DEBUG": "false",
            "LOG_LEVEL": "WARNING",
            "RATE_LIMIT": "60",
            "FEATURES": "All enabled",
            "SAFETY_CHECKS": "Maximum",
        },
    }

    for env_name, config in configs.items():
        print(f"\n📋 {env_name} Configuration:")
        for key, value in config.items():
            print(f"   {key}: {value}")

    print_header("Key Differences Summary")

    print("\n🔒 Security:")
    print("   - Dev: Debug enabled, loose rate limits")
    print("   - Staging: Debug disabled, moderate limits")
    print("   - Prod: Debug disabled, strict limits")

    print("\n📊 Monitoring:")
    print("   - Dev: Detailed logging, development metrics")
    print("   - Staging: Standard logging, performance metrics")
    print("   - Prod: Minimal logging, production metrics")

    print("\n🚀 Deployment:")
    print("   - Dev: Quick deployment, no safety checks")
    print("   - Staging: Automated deployment, basic checks")
    print("   - Prod: Manual approval, comprehensive checks")

    print_header("Best Practices Demonstrated")

    best_practices = [
        "✅ Environment Isolation - Separate namespaces and databases",
        "✅ Configuration Management - Environment-specific ConfigMaps and Secrets",
        "✅ Progressive Deployment - Dev → Staging → Production pipeline",
        "✅ Safety Measures - Increasing safety checks per environment",
        "✅ Monitoring & Observability - Environment-appropriate logging and metrics",
    ]

    for practice in best_practices:
        print(f"   {practice}")

    print_header("Deployment Commands")

    print("\n🎉 Environment differentiation is now complete!")
    print("   You can deploy to different environments using:")
    print("   - scripts/deploy-dev.ps1")
    print("   - scripts/deploy-staging.ps1")
    print("   - scripts/deploy-prod.ps1")

    print("\n📁 Files Created:")
    print("   - infrastructure/kubernetes/namespace-dev.yml")
    print("   - infrastructure/kubernetes/namespace-staging.yml")
    print("   - infrastructure/kubernetes/namespace-prod.yml")
    print("   - app/api/utils/config.py (updated)")
    print("   - scripts/deploy-dev.ps1")
    print("   - scripts/deploy-staging.ps1")
    print("   - scripts/deploy-prod.ps1")
    print("   - scripts/compare-environments.py")


if __name__ == "__main__":
    main()
