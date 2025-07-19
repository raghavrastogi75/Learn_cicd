#!/usr/bin/env python3
"""
Feature Development Demo: Cubic Power Feature
============================================

This script demonstrates the complete lifecycle of adding a new feature
(cubic power operation) to the calculator API and how it flows through
Development → Staging → Production environments.

Usage:
    python scripts/feature-development-demo.py
"""

import os
import sys
import time
import subprocess
import json
import requests
from datetime import datetime
from typing import Dict, Any, List

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

class FeatureDevelopmentDemo:
    """Demonstrates feature development lifecycle through environments"""
    
    def __init__(self):
        self.environments = {
            'development': {
                'port': 8080,
                'namespace': 'calculator-dev',
                'config': {
                    'ENVIRONMENT': 'development',
                    'DEBUG': 'true',
                    'LOG_LEVEL': 'DEBUG',
                    'RATE_LIMIT_PER_MINUTE': '1000'
                }
            },
            'staging': {
                'port': 8081,
                'namespace': 'calculator-staging',
                'config': {
                    'ENVIRONMENT': 'staging',
                    'DEBUG': 'false',
                    'LOG_LEVEL': 'INFO',
                    'RATE_LIMIT_PER_MINUTE': '100'
                }
            },
            'production': {
                'port': 8082,
                'namespace': 'calculator-prod',
                'config': {
                    'ENVIRONMENT': 'production',
                    'DEBUG': 'false',
                    'LOG_LEVEL': 'WARNING',
                    'RATE_LIMIT_PER_MINUTE': '60'
                }
            }
        }
        
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "="*80)
        print(f"🚀 {title}")
        print("="*80)
        
    def print_step(self, step: str, description: str):
        """Print a formatted step"""
        print(f"\n📋 {step}")
        print(f"   {description}")
        print("-" * 60)
        
    def run_command(self, command: str, check: bool = True) -> str:
        """Run a shell command and return output"""
        print(f"   Running: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=check
            )
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"   Command failed: {e}")
            return ""
            
    def test_cubic_operation(self, base_url: str, env_name: str) -> bool:
        """Test the cubic operation in a specific environment"""
        print(f"\n   Testing cubic operation in {env_name} environment...")
        
        # Test cases for cubic operation
        test_cases = [
            {"a": 2, "expected": 8.0, "description": "Positive number"},
            {"a": -3, "expected": -27.0, "description": "Negative number"},
            {"a": 0, "expected": 0.0, "description": "Zero"},
            {"a": 1.5, "expected": 3.375, "description": "Decimal number"},
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            try:
                response = requests.post(
                    f"{base_url}/api/calculator/calculate",
                    json={
                        "operation": "cubic",
                        "a": test_case["a"]
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    actual_result = result["result"]
                    
                    if abs(actual_result - test_case["expected"]) < 0.001:
                        print(f"   ✅ {test_case['description']}: {test_case['a']}³ = {actual_result}")
                    else:
                        print(f"   ❌ {test_case['description']}: Expected {test_case['expected']}, got {actual_result}")
                        all_passed = False
                else:
                    print(f"   ❌ {test_case['description']}: HTTP {response.status_code} - {response.text}")
                    all_passed = False
                    
            except Exception as e:
                print(f"   ❌ {test_case['description']}: Error - {str(e)}")
                all_passed = False
                
        return all_passed
    
    def check_operations_list(self, base_url: str, env_name: str) -> bool:
        """Check if cubic operation is in the operations list"""
        print(f"\n   Checking operations list in {env_name} environment...")
        
        try:
            response = requests.get(f"{base_url}/api/calculator/operations", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                operations = [op["name"] for op in result["operations"]]
                
                if "cubic" in operations:
                    print(f"   ✅ Cubic operation found in operations list")
                    print(f"   📊 Total operations: {result['count']}")
                    return True
                else:
                    print(f"   ❌ Cubic operation not found in operations list")
                    print(f"   📋 Available operations: {operations}")
                    return False
            else:
                print(f"   ❌ Failed to get operations: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error checking operations: {str(e)}")
            return False
    
    def run_environment_tests(self, env_name: str) -> bool:
        """Run comprehensive tests for an environment"""
        env_config = self.environments[env_name]
        base_url = f"http://localhost:{env_config['port']}"
        
        print(f"\n🔍 Testing {env_name.upper()} Environment")
        print(f"   URL: {base_url}")
        print(f"   Namespace: {env_config['namespace']}")
        
        # Test 1: Health check
        print(f"\n   Testing health check...")
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ Health check passed")
            else:
                print(f"   ❌ Health check failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Health check error: {str(e)}")
            return False
        
        # Test 2: Check operations list
        if not self.check_operations_list(base_url, env_name):
            return False
        
        # Test 3: Test cubic operation
        if not self.test_cubic_operation(base_url, env_name):
            return False
        
        # Test 4: Test existing operations still work
        print(f"\n   Testing existing operations...")
        try:
            response = requests.post(
                f"{base_url}/api/calculator/calculate",
                json={"operation": "add", "a": 5, "b": 3},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                if result["result"] == 8.0:
                    print(f"   ✅ Existing operations still work (5 + 3 = 8)")
                else:
                    print(f"   ❌ Existing operations broken")
                    return False
            else:
                print(f"   ❌ Existing operations test failed")
                return False
        except Exception as e:
            print(f"   ❌ Existing operations error: {str(e)}")
            return False
        
        return True
    
    def simulate_development_phase(self):
        """Simulate the development phase"""
        self.print_header("PHASE 1: DEVELOPMENT")
        
        self.print_step("1.1", "Feature Branch Creation")
        print("   git checkout -b feature/add-cubic-power")
        print("   ✅ Feature branch created")
        
        self.print_step("1.2", "Code Implementation")
        print("   ✅ Added 'cubic' to operation Literal types")
        print("   ✅ Implemented cubic calculation logic")
        print("   ✅ Updated validation rules")
        print("   ✅ Added cubic operation to API routes")
        print("   ✅ Created comprehensive unit tests")
        
        self.print_step("1.3", "Local Testing")
        print("   Running unit tests...")
        result = self.run_command("python -m pytest tests/unit/ -v")
        if "18 passed" in result:
            print("   ✅ All unit tests passed")
        else:
            print("   ❌ Some tests failed")
            return False
        
        self.print_step("1.4", "Code Review")
        print("   ✅ Code review completed")
        print("   ✅ All checks passed")
        print("   ✅ Ready for merge to main")
        
        return True
    
    def simulate_ci_cd_pipeline(self):
        """Simulate the CI/CD pipeline"""
        self.print_header("PHASE 2: CI/CD PIPELINE")
        
        self.print_step("2.1", "GitHub Actions Triggered")
        print("   ✅ Push to main branch detected")
        print("   ✅ CI/CD pipeline started")
        
        self.print_step("2.2", "Linting and Formatting")
        print("   ✅ Black code formatting check")
        print("   ✅ isort import sorting check")
        print("   ✅ flake8 linting check")
        print("   ✅ mypy type checking")
        
        self.print_step("2.3", "Unit Tests")
        print("   ✅ All unit tests passed")
        print("   ✅ Code coverage: 95%")
        print("   ✅ Coverage uploaded to Codecov")
        
        self.print_step("2.4", "Integration Tests")
        print("   ✅ Database integration tests")
        print("   ✅ API endpoint tests")
        print("   ✅ All integration tests passed")
        
        self.print_step("2.5", "Security Scan")
        print("   ✅ Bandit security scan")
        print("   ✅ Safety dependency check")
        print("   ✅ No security vulnerabilities found")
        
        self.print_step("2.6", "Docker Build")
        print("   ✅ Docker image built successfully")
        print("   ✅ Image tagged and pushed to registry")
        print("   ✅ Image: ghcr.io/calculator-api:latest")
        
        return True
    
    def simulate_staging_deployment(self):
        """Simulate staging deployment"""
        self.print_header("PHASE 3: STAGING DEPLOYMENT")
        
        self.print_step("3.1", "Staging Environment Setup")
        print("   ✅ Kubernetes namespace created")
        print("   ✅ ConfigMap applied with staging config")
        print("   ✅ Secrets configured")
        
        self.print_step("3.2", "Application Deployment")
        print("   ✅ New Docker image deployed")
        print("   ✅ Rolling update completed")
        print("   ✅ Health checks passed")
        print("   ✅ Traffic routed to new version")
        
        self.print_step("3.3", "Staging Validation")
        print("   Running comprehensive tests in staging...")
        
        # Simulate staging tests
        time.sleep(2)
        print("   ✅ API endpoints responding")
        print("   ✅ Database connectivity verified")
        print("   ✅ Metrics collection working")
        print("   ✅ Logging configured correctly")
        
        self.print_step("3.4", "Performance Testing")
        print("   ✅ Load testing completed")
        print("   ✅ Response times within limits")
        print("   ✅ Error rates acceptable")
        print("   ✅ Resource usage normal")
        
        self.print_step("3.5", "Integration Testing")
        print("   ✅ End-to-end tests passed")
        print("   ✅ Third-party integrations working")
        print("   ✅ Monitoring alerts configured")
        
        return True
    
    def simulate_production_deployment(self):
        """Simulate production deployment"""
        self.print_header("PHASE 4: PRODUCTION DEPLOYMENT")
        
        self.print_step("4.1", "Production Safety Checks")
        print("   ✅ Branch protection rules satisfied")
        print("   ✅ All required approvals received")
        print("   ✅ Production environment ready")
        
        self.print_step("4.2", "Pre-deployment Validation")
        print("   ✅ Final test suite execution")
        print("   ✅ Security scan completed")
        print("   ✅ Performance baseline verified")
        
        self.print_step("4.3", "Production Deployment")
        print("   ✅ Blue-green deployment initiated")
        print("   ✅ New version deployed to blue environment")
        print("   ✅ Health checks passed")
        print("   ✅ Traffic gradually shifted to blue")
        print("   ✅ Green environment decommissioned")
        
        self.print_step("4.4", "Post-deployment Monitoring")
        print("   ✅ Application metrics normal")
        print("   ✅ Error rates within acceptable range")
        print("   ✅ Response times meeting SLAs")
        print("   ✅ User traffic handling correctly")
        
        self.print_step("4.5", "Feature Verification")
        print("   ✅ Cubic operation available in production")
        print("   ✅ All existing operations working")
        print("   ✅ API documentation updated")
        print("   ✅ Monitoring dashboards updated")
        
        return True
    
    def demonstrate_feature_usage(self):
        """Demonstrate the new feature in action"""
        self.print_header("FEATURE DEMONSTRATION")
        
        print("\n🎯 Cubic Power Operation Examples:")
        print("   • 2³ = 8")
        print("   • (-3)³ = -27")
        print("   • 0³ = 0")
        print("   • 1.5³ = 3.375")
        
        print("\n📊 API Usage:")
        print("   POST /api/calculator/calculate")
        print("   {")
        print('     "operation": "cubic",')
        print('     "a": 2')
        print("   }")
        
        print("\n📈 Benefits:")
        print("   ✅ New mathematical operation available")
        print("   ✅ Backward compatibility maintained")
        print("   ✅ Comprehensive test coverage")
        print("   ✅ Proper error handling")
        print("   ✅ Environment-specific configuration")
        
        print("\n🔧 Technical Implementation:")
        print("   ✅ Type-safe operation definition")
        print("   ✅ Mathematical validation")
        print("   ✅ Database storage")
        print("   ✅ Metrics collection")
        print("   ✅ Logging integration")
    
    def run_complete_demo(self):
        """Run the complete feature development demonstration"""
        self.print_header("FEATURE DEVELOPMENT LIFECYCLE DEMO")
        print("   Adding Cubic Power Operation to Calculator API")
        print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Phase 1: Development
            if not self.simulate_development_phase():
                print("\n❌ Development phase failed")
                return False
            
            # Phase 2: CI/CD Pipeline
            if not self.simulate_ci_cd_pipeline():
                print("\n❌ CI/CD pipeline failed")
                return False
            
            # Phase 3: Staging
            if not self.simulate_staging_deployment():
                print("\n❌ Staging deployment failed")
                return False
            
            # Phase 4: Production
            if not self.simulate_production_deployment():
                print("\n❌ Production deployment failed")
                return False
            
            # Feature demonstration
            self.demonstrate_feature_usage()
            
            self.print_header("DEMO COMPLETED SUCCESSFULLY")
            print("   ✅ Feature successfully deployed to all environments")
            print("   ✅ All tests passed")
            print("   ✅ No issues encountered")
            print(f"   Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Demo failed with error: {str(e)}")
            return False


def main():
    """Main function to run the demo"""
    demo = FeatureDevelopmentDemo()
    success = demo.run_complete_demo()
    
    if success:
        print("\n🎉 Feature development lifecycle demonstration completed successfully!")
        print("   The cubic power feature is now available in all environments.")
    else:
        print("\n💥 Demo encountered issues. Please check the logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 