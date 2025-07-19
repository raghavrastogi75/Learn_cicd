import time
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.database.connection import close_db, init_db
from app.api.routes import alerts, calculator, health, history
from app.api.utils.config import config as settings
from app.api.utils.logger import setup_logging
from app.api.utils.metrics import PrometheusMiddleware, get_metrics

# Setup structured logging
setup_logging()
logger = structlog.get_logger()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Calculator API")
    await init_db()
    logger.info("Calculator API started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Calculator API")
    await close_db()
    logger.info("Calculator API shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Calculator API",
    description="A simple calculator API for CI/CD learning",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics middleware
app.add_middleware(PrometheusMiddleware)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing information"""
    start_time = time.time()

    # Generate request ID
    request_id = request.headers.get("X-Request-ID", f"req_{int(start_time * 1000)}")

    # Log request
    logger.info(
        "Request started",
        request_id=request_id,
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log response
    logger.info(
        "Request completed",
        request_id=request_id,
        status_code=response.status_code,
        process_time=round(process_time, 4),
    )

    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(calculator.router, prefix="/api/calculator", tags=["calculator"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])


# Metrics endpoint
@app.get("/metrics", tags=["metrics"])
async def metrics():
    """Prometheus metrics endpoint"""
    return get_metrics()


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Calculator API - CI/CD Learning Project",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "endpoints": {
            "health": "/health",
            "calculator": "/api/calculator",
            "history": "/api/history",
            "docs": "/docs" if settings.ENVIRONMENT != "production" else None,
        },
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions"""
    logger.error(
        "Unhandled exception",
        request_id=request.headers.get("X-Request-ID", "unknown"),
        exception_type=type(exc).__name__,
        exception_message=str(exc),
        url=str(request.url),
        method=request.method,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "request_id": request.headers.get("X-Request-ID", "unknown"),
        },
    )


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "service": "calculator-api", "timestamp": time.time()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False,
    )
