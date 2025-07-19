#!/usr/bin/env python3
"""
Environment Comparison Script
Shows differences between development, staging, and production environments
"""

import json
import os
import subprocess
import sys
from typing import Any, Dict


class EnvironmentComparator:
    """Compare different environments"""

    def __init__(self):
        self.environments = {
            "development": {
                "namespace": "calculator-dev",
                "port": 8080,
                "config_map": "calculator-config-dev",
            },
            "staging": {
                "namespace": "calculator-staging",
                "port": 8081,
                "config_map": "calculator-config-staging",
            },
            "production": {
                "namespace": "calculator-prod",
                "port": 8082,
                "config_map": "calculator-config-prod",
            },
        }

    def get_environment_config(self, env: str) -> Dict[str, Any]:
        """Get configuration for a specific environment"""
        if env not in self.environments:
            raise ValueError(f"Unknown environment: {env}")

        env_info = self.environments[env]

        # Try to get actual config from Kubernetes
        try:
            result = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "configmap",
                    env_info["config_map"],
                    "-n",
                    env_info["namespace"],
                    "-o",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            config_data = json.loads(result.stdout)
            return {
                "environment": env,
                "namespace": env_info["namespace"],
                "port": env_info["port"],
                "config": config_data["data"],
                "status": "active",
            }
        except subprocess.CalledProcessError:
            return {
                "environment": env,
                "namespace": env_info["namespace"],
                "port": env_info["port"],
                "config": {},
                "status": "not deployed",
            }

    def compare_environments(self) -> Dict[str, Any]:
        """Compare all environments"""
        comparison = {}

        for env in self.environments.keys():
            comparison[env] = self.get_environment_config(env)

        return comparison

    def display_comparison(self, comparison: Dict[str, Any]):
        """Display environment comparison in a nice format"""
        print("🌍 Environment Comparison")
        print("=" * 80)

        # Headers
        headers = [
            "Environment",
            "Namespace",
            "Status",
            "Debug",
            "Log Level",
            "Rate Limit",
            "Features",
        ]
        print(
            f"{headers[0]:<15} {headers[1]:<20} {headers[2]:<12} {headers[3]:<8} {headers[4]:<10} {headers[5]:<12} {headers[6]}"
        )
        print("-" * 80)

        for env_name, env_data in comparison.items():
            config = env_data.get("config", {})

            # Extract values
            namespace = env_data["namespace"]
            status = env_data["status"]
            debug = config.get("DEBUG", "N/A")
            log_level = config.get("LOG_LEVEL", "N/A")
            rate_limit = config.get("RATE_LIMIT_PER_MINUTE", "N/A")

            # Feature flags
            abs_diff = config.get("ENABLE_ABS_DIFF", "N/A")
            history = config.get("ENABLE_HISTORY", "N/A")
            features = f"abs_diff:{abs_diff}, history:{history}"

            print(
                f"{env_name:<15} {namespace:<20} {status:<12} {debug:<8} {log_level:<10} {rate_limit:<12} {features}"
            )

        print("\n" + "=" * 80)

    def display_detailed_config(self, env: str):
        """Display detailed configuration for a specific environment"""
        config = self.get_environment_config(env)

        print(f"\n🔧 Detailed Configuration for {env.upper()}")
        print("=" * 50)

        if config["status"] == "active":
            print(f"Namespace: {config['namespace']}")
            print(f"Port: {config['port']}")
            print(f"Status: {config['status']}")
            print("\nConfiguration:")

            for key, value in config["config"].items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ Environment {env} is not deployed")
            print(f"   Namespace: {config['namespace']}")
            print(f"   Expected Port: {config['port']}")

    def test_environment_connectivity(self, env: str):
        """Test connectivity to a specific environment"""
        env_info = self.environments[env]

        print(f"\n🧪 Testing connectivity to {env.upper()}")
        print("=" * 40)

        # Check if namespace exists
        try:
            result = subprocess.run(
                ["kubectl", "get", "namespace", env_info["namespace"]],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"✅ Namespace {env_info['namespace']} exists")
        except subprocess.CalledProcessError:
            print(f"❌ Namespace {env_info['namespace']} does not exist")
            return

        # Check if pods are running
        try:
            result = subprocess.run(
                ["kubectl", "get", "pods", "-n", env_info["namespace"]],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"✅ Pods in {env_info['namespace']}:")
            print(result.stdout)
        except subprocess.CalledProcessError:
            print(f"❌ Cannot get pods in {env_info['namespace']}")

        # Check services
        try:
            result = subprocess.run(
                ["kubectl", "get", "services", "-n", env_info["namespace"]],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"✅ Services in {env_info['namespace']}:")
            print(result.stdout)
        except subprocess.CalledProcessError:
            print(f"❌ Cannot get services in {env_info['namespace']}")


def main():
    """Main function"""
    comparator = EnvironmentComparator()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "compare":
            comparison = comparator.compare_environments()
            comparator.display_comparison(comparison)

        elif command == "detail" and len(sys.argv) > 2:
            env = sys.argv[2]
            comparator.display_detailed_config(env)

        elif command == "test" and len(sys.argv) > 2:
            env = sys.argv[2]
            comparator.test_environment_connectivity(env)

        else:
            print("Usage:")
            print("  python scripts/compare-environments.py compare")
            print("  python scripts/compare-environments.py detail <environment>")
            print("  python scripts/compare-environments.py test <environment>")
            print("\nEnvironments: development, staging, production")
    else:
        # Default: show comparison
        comparison = comparator.compare_environments()
        comparator.display_comparison(comparison)


if __name__ == "__main__":
    main()
