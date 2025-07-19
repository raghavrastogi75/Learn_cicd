#!/usr/bin/env python3
"""
Test Alerting System
Generates errors to trigger alerts
"""

import asyncio
import aiohttp
import random
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_alerts():
    """Test the alerting system by generating errors"""
    
    async with aiohttp.ClientSession() as session:
        base_url = "http://localhost:8000"
        
        print("🚨 Testing Alert System")
        print("=" * 50)
        
        # Test 1: Generate 400 errors (bad requests)
        print("\n1️⃣ Testing 400 Errors (Bad Requests)")
        print("-" * 30)
        
        for i in range(10):
            # Send invalid requests to trigger 400 errors
            invalid_data = [
                {"operation": "divide", "a": 10, "b": 0},  # Division by zero
                {"operation": "power", "a": 1000, "b": 1000},  # Very large power
                {"operation": "sqrt", "a": -1},  # Negative sqrt
                {"invalid": "data"},  # Invalid JSON
                {"operation": "unknown", "a": 1, "b": 2},  # Unknown operation
            ]
            
            data = random.choice(invalid_data)
            try:
                async with session.post(f"{base_url}/api/calculator/calculate", json=data) as response:
                    logger.info(f"Request {i+1}: Status {response.status} - {data}")
            except Exception as e:
                logger.error(f"Request {i+1} failed: {e}")
            
            await asyncio.sleep(0.5)
        
        # Test 2: Generate high load to test response time alerts
        print("\n2️⃣ Testing High Load (Response Time Alerts)")
        print("-" * 40)
        
        # Send many requests quickly
        tasks = []
        for i in range(50):
            task = session.post(
                f"{base_url}/api/calculator/calculate",
                json={"operation": "add", "a": i, "b": i}
            )
            tasks.append(task)
        
        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in responses if hasattr(r, 'status') and r.status == 200)
        error_count = len(responses) - success_count
        
        logger.info(f"High load test: {success_count} success, {error_count} errors")
        
        # Test 3: Test alert webhook endpoint
        print("\n3️⃣ Testing Alert Webhook")
        print("-" * 25)
        
        test_alert = {
            "alerts": [
                {
                    "status": "firing",
                    "labels": {
                        "alertname": "High Error Rate",
                        "severity": "warning",
                        "service": "calculator-api"
                    },
                    "annotations": {
                        "summary": "High error rate detected",
                        "description": "Error rate is 15% for the last 5 minutes"
                    }
                }
            ]
        }
        
        try:
            async with session.post(f"{base_url}/api/alerts/webhook", json=test_alert) as response:
                if response.status == 200:
                    logger.info("✅ Alert webhook test successful")
                else:
                    logger.error(f"❌ Alert webhook test failed: {response.status}")
        except Exception as e:
            logger.error(f"❌ Alert webhook test failed: {e}")
        
        # Test 4: Check alert status
        print("\n4️⃣ Checking Alert Status")
        print("-" * 25)
        
        try:
            async with session.get(f"{base_url}/api/alerts/status") as response:
                if response.status == 200:
                    status_data = await response.json()
                    logger.info(f"✅ Alert status: {status_data}")
                else:
                    logger.error(f"❌ Alert status check failed: {response.status}")
        except Exception as e:
            logger.error(f"❌ Alert status check failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_alerts()) 