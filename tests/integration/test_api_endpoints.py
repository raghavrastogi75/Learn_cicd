import pytest
import httpx
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.main import app
from app.api.database.connection import get_db
from app.api.database.models import Base
from app.api.database.connection import engine

@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

@pytest.fixture
async def db_session():
    """Create database session for testing"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async for session in get_db():
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

class TestCalculatorEndpoints:
    """Integration tests for calculator endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Calculator API - CI/CD Learning Project"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "calculator-api"
    
    def test_get_operations(self, client):
        """Test getting available operations"""
        response = client.get("/api/calculator/operations")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 6
        assert len(data["operations"]) == 6
        
        # Check specific operations
        operations = {op["name"]: op for op in data["operations"]}
        assert "add" in operations
        assert "subtract" in operations
        assert "multiply" in operations
        assert "divide" in operations
        assert "power" in operations
        assert "sqrt" in operations
    
    def test_calculate_addition(self, client):
        """Test addition calculation"""
        payload = {
            "operation": "add",
            "a": 5,
            "b": 3
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["operation"] == "add"
        assert data["a"] == 5
        assert data["b"] == 3
        assert data["result"] == 8.0
    
    def test_calculate_subtraction(self, client):
        """Test subtraction calculation"""
        payload = {
            "operation": "subtract",
            "a": 10,
            "b": 4
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 6.0
    
    def test_calculate_multiplication(self, client):
        """Test multiplication calculation"""
        payload = {
            "operation": "multiply",
            "a": 6,
            "b": 7
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 42.0
    
    def test_calculate_division(self, client):
        """Test division calculation"""
        payload = {
            "operation": "divide",
            "a": 15,
            "b": 3
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5.0
    
    def test_calculate_power(self, client):
        """Test power calculation"""
        payload = {
            "operation": "power",
            "a": 2,
            "b": 3
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8.0
    
    def test_calculate_sqrt(self, client):
        """Test square root calculation"""
        payload = {
            "operation": "sqrt",
            "a": 16
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 4.0
    
    def test_division_by_zero(self, client):
        """Test division by zero error"""
        payload = {
            "operation": "divide",
            "a": 10,
            "b": 0
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "Division by zero is not allowed" in data["detail"]
    
    def test_sqrt_negative_number(self, client):
        """Test square root of negative number error"""
        payload = {
            "operation": "sqrt",
            "a": -4
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "Cannot calculate square root of negative number" in data["detail"]
    
    def test_invalid_operation(self, client):
        """Test invalid operation error"""
        payload = {
            "operation": "invalid",
            "a": 1,
            "b": 1
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_missing_second_operand(self, client):
        """Test missing second operand for non-sqrt operations"""
        payload = {
            "operation": "add",
            "a": 5
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_number_format(self, client):
        """Test invalid number format"""
        payload = {
            "operation": "add",
            "a": "not_a_number",
            "b": 3
        }
        response = client.post("/api/calculator/calculate", json=payload)
        assert response.status_code == 422  # Validation error

class TestHistoryEndpoints:
    """Integration tests for history endpoints"""
    
    def test_get_history(self, client):
        """Test getting calculation history"""
        response = client.get("/api/history/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "pagination" in data
    
    def test_get_history_with_pagination(self, client):
        """Test getting history with pagination parameters"""
        response = client.get("/api/history/?limit=5&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["pagination"]["limit"] == 5
        assert data["pagination"]["offset"] == 0
    
    def test_get_statistics(self, client):
        """Test getting calculation statistics"""
        response = client.get("/api/history/statistics")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "total_calculations" in data["data"]
        assert "most_used_operation" in data["data"]
        assert "average_result" in data["data"]
        assert "today_calculations" in data["data"]
        assert "week_calculations" in data["data"]
    
    def test_clear_history(self, client):
        """Test clearing calculation history"""
        response = client.delete("/api/history/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "deleted_count" in data

class TestHealthEndpoints:
    """Integration tests for health endpoints"""
    
    def test_basic_health(self, client):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_detailed_health(self, client):
        """Test detailed health check"""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "components" in data
        assert "database" in data["components"]
    
    def test_readiness_check(self, client):
        """Test readiness check"""
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_liveness_check(self, client):
        """Test liveness check"""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive" 