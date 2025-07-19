from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import structlog
from datetime import datetime
import time

from app.api.database.connection import get_db, health_check_db
from app.api.utils.logger import LoggerMixin

router = APIRouter()
logger = structlog.get_logger()

class HealthRouter(LoggerMixin):
    """Health check router"""
    
    @router.get("/")
    async def health_check():
        """Basic health check endpoint"""
        return {
            "status": "healthy",
            "service": "calculator-api",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    
    @router.get("/detailed")
    async def detailed_health_check(db: AsyncSession = Depends(get_db)):
        """Detailed health check with database connectivity"""
        start_time = time.time()
        
        try:
            # Check database health
            db_health = await health_check_db()
            
            # Calculate response time
            response_time = time.time() - start_time
            
            return {
                "status": "healthy" if db_health["status"] == "healthy" else "unhealthy",
                "service": "calculator-api",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "response_time": round(response_time, 4),
                "components": {
                    "database": db_health
                }
            }
            
        except Exception as e:
            self.logger.error("Health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "service": "calculator-api",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "error": str(e)
            }
    
    @router.get("/ready")
    async def readiness_check(db: AsyncSession = Depends(get_db)):
        """Readiness check for Kubernetes"""
        try:
            # Test database connection
            db_health = await health_check_db()
            
            if db_health["status"] == "healthy":
                return {
                    "status": "ready",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "not_ready",
                    "reason": "Database connection failed",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error("Readiness check failed", error=str(e))
            return {
                "status": "not_ready",
                "reason": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    @router.get("/live")
    async def liveness_check():
        """Liveness check for Kubernetes"""
        return {
            "status": "alive",
            "timestamp": datetime.now().isoformat()
        }

# Create router instance
health_router = HealthRouter() 