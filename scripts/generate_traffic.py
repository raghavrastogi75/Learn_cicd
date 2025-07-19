#!/usr/bin/env python3
"""
Continuous Traffic Generator for Calculator API
Simulates real-world traffic patterns for monitoring and testing
"""

import asyncio
import aiohttp
import random
import time
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrafficGenerator:
    """Generates continuous traffic to the Calculator API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.running = False
        
        # Traffic patterns
        self.operations = ['add', 'subtract', 'multiply', 'divide', 'power', 'sqrt', 'abs_diff']
        self.operation_weights = {
            'add': 0.25,      # 25% of requests
            'subtract': 0.2,  # 20% of requests
            'multiply': 0.15, # 15% of requests
            'divide': 0.1,    # 10% of requests
            'power': 0.05,    # 5% of requests
            'sqrt': 0.05,     # 5% of requests
            'abs_diff': 0.2   # 20% of requests
        }
        
        # Traffic intensity patterns (requests per second)
        self.traffic_patterns = {
            'low': {'min_rps': 1, 'max_rps': 3},
            'medium': {'min_rps': 3, 'max_rps': 8},
            'high': {'min_rps': 8, 'max_rps': 15},
            'burst': {'min_rps': 15, 'max_rps': 30}
        }
        
        # Current traffic pattern
        self.current_pattern = 'medium'
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def get_random_operation(self) -> str:
        """Get a random operation based on weights"""
        return random.choices(
            list(self.operation_weights.keys()),
            weights=list(self.operation_weights.values())
        )[0]
    
    def get_random_numbers(self, operation: str) -> Dict[str, float]:
        """Generate random numbers for the operation"""
        if operation == 'sqrt':
            # For sqrt, only need one positive number
            a = random.uniform(1, 1000)
            return {'operation': operation, 'a': a}
        elif operation == 'abs_diff':
            # For abs_diff, need two numbers (can be any range)
            a = random.uniform(-1000, 1000)
            b = random.uniform(-1000, 1000)
            return {'operation': operation, 'a': a, 'b': b}
        else:
            # For other operations, need two numbers
            a = random.uniform(-1000, 1000)
            b = random.uniform(-1000, 1000)
            
            # Avoid division by zero
            if operation == 'divide' and abs(b) < 0.001:
                b = random.uniform(1, 100) if b >= 0 else random.uniform(-100, -1)
            
            return {'operation': operation, 'a': a, 'b': b}
    
    def get_traffic_intensity(self) -> float:
        """Get current traffic intensity (requests per second)"""
        pattern = self.traffic_patterns[self.current_pattern]
        return random.uniform(pattern['min_rps'], pattern['max_rps'])
    
    async def make_request(self, request_data: Dict[str, Any]) -> bool:
        """Make a single API request"""
        try:
            url = f"{self.base_url}/api/calculator/calculate"
            headers = {'Content-Type': 'application/json'}
            
            async with self.session.post(url, json=request_data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.debug(f"Request successful: {request_data['operation']} -> {result.get('result', 'N/A')}")
                    return True
                else:
                    logger.warning(f"Request failed with status {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Request error: {e}")
            return False
    
    async def generate_traffic_burst(self, duration: int = 10, intensity: str = 'medium'):
        """Generate traffic burst for specified duration"""
        logger.info(f"Starting traffic burst: {intensity} intensity for {duration} seconds")
        
        self.current_pattern = intensity
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < duration and self.running:
            rps = self.get_traffic_intensity()
            delay = 1.0 / rps
            
            # Generate and send request
            operation = self.get_random_operation()
            request_data = self.get_random_numbers(operation)
            
            success = await self.make_request(request_data)
            request_count += 1
            
            if success:
                logger.info(f"Request {request_count}: {request_data['operation']} ({rps:.1f} RPS)")
            else:
                logger.warning(f"Failed request {request_count}")
            
            # Wait before next request
            await asyncio.sleep(delay)
        
        logger.info(f"Traffic burst completed: {request_count} requests")
    
    async def simulate_traffic_patterns(self):
        """Simulate realistic traffic patterns"""
        logger.info("Starting continuous traffic simulation")
        
        while self.running:
            # Simulate different traffic patterns
            patterns = [
                ('low', 30),      # Low traffic for 30 seconds
                ('medium', 60),   # Medium traffic for 1 minute
                ('high', 45),     # High traffic for 45 seconds
                ('burst', 15),    # Burst traffic for 15 seconds
                ('medium', 30),   # Back to medium
                ('low', 20),      # Low traffic for 20 seconds
            ]
            
            for intensity, duration in patterns:
                if not self.running:
                    break
                    
                logger.info(f"Switching to {intensity} traffic pattern")
                await self.generate_traffic_burst(duration, intensity)
    
    async def continuous_traffic(self, rps: float = 5.0):
        """Generate continuous traffic at specified rate"""
        logger.info(f"Starting continuous traffic at {rps} RPS")
        
        delay = 1.0 / rps
        request_count = 0
        
        while self.running:
            try:
                operation = self.get_random_operation()
                request_data = self.get_random_numbers(operation)
                
                success = await self.make_request(request_data)
                request_count += 1
                
                if success:
                    logger.info(f"Request {request_count}: {request_data['operation']}")
                else:
                    logger.warning(f"Failed request {request_count}")
                
                await asyncio.sleep(delay)
                
            except KeyboardInterrupt:
                logger.info("Traffic generation interrupted")
                break
            except Exception as e:
                logger.error(f"Error in traffic generation: {e}")
                await asyncio.sleep(1)
    
    def stop(self):
        """Stop traffic generation"""
        self.running = False
        logger.info("Stopping traffic generation")

async def main():
    """Main function to run traffic generator"""
    print("🚀 Calculator API Traffic Generator")
    print("=" * 50)
    print("1. Continuous traffic at 5 RPS")
    print("2. Simulate traffic patterns")
    print("3. Custom traffic burst")
    print("4. Exit")
    print("=" * 50)
    
    choice = input("Choose option (1-4): ").strip()
    
    async with TrafficGenerator() as generator:
        generator.running = True
        
        if choice == "1":
            rps = float(input("Enter requests per second (default 5): ") or "5")
            await generator.continuous_traffic(rps)
            
        elif choice == "2":
            print("Starting realistic traffic pattern simulation...")
            await generator.simulate_traffic_patterns()
            
        elif choice == "3":
            intensity = input("Enter intensity (low/medium/high/burst): ").strip()
            duration = int(input("Enter duration in seconds: ").strip())
            await generator.generate_traffic_burst(duration, intensity)
            
        elif choice == "4":
            print("Exiting...")
            return
        
        else:
            print("Invalid choice. Starting default continuous traffic...")
            await generator.continuous_traffic(5.0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Traffic generation stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}") 