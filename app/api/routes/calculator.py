from datetime import datetime

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.database.connection import get_db
from app.api.models.calculator import (
    CalculationRequest,
    CalculationResponse,
    HealthResponse,
    OperationInfo,
    OperationsResponse,
)
from app.api.services.calculator_service import calculator_service
from app.api.utils.logger import LoggerMixin

router = APIRouter()
logger = structlog.get_logger()


class CalculatorRouter(LoggerMixin):
    """Calculator router with rate limiting"""

    def __init__(self):
        self.limiter = Limiter(key_func=get_remote_address)

    @router.post("/calculate", response_model=CalculationResponse)
    async def calculate(
        request: CalculationRequest,
        db: AsyncSession = Depends(get_db),
        http_request: Request = None,
    ):
        """Perform mathematical calculation"""
        try:
            # Validate operation-specific requirements
            if request.operation not in ["sqrt", "cubic"] and request.b is None:
                raise HTTPException(
                    status_code=400,
                    detail="Second operand is required for this operation",
                )

            # Perform calculation
            result = await calculator_service.calculate(
                operation=request.operation, a=request.a, b=request.b, session=db
            )

            return CalculationResponse(
                success=True,
                operation=request.operation,
                a=request.a,
                b=request.b,
                result=result,
                timestamp=datetime.now(),
            )

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(
                "Calculation error",
                operation=request.operation,
                a=request.a,
                b=request.b,
                error=str(e),
            )
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.get("/operations", response_model=OperationsResponse)
    async def get_operations():
        """Get list of supported operations"""
        operations = [
            OperationInfo(
                name="add",
                symbol="+",
                description="Add two numbers",
                parameters=["a", "b"],
            ),
            OperationInfo(
                name="subtract",
                symbol="-",
                description="Subtract second number from first",
                parameters=["a", "b"],
            ),
            OperationInfo(
                name="multiply",
                symbol="×",
                description="Multiply two numbers",
                parameters=["a", "b"],
            ),
            OperationInfo(
                name="divide",
                symbol="÷",
                description="Divide first number by second",
                parameters=["a", "b"],
            ),
            OperationInfo(
                name="power",
                symbol="^",
                description="Raise first number to power of second",
                parameters=["a", "b"],
            ),
            OperationInfo(
                name="sqrt",
                symbol="√",
                description="Calculate square root of number",
                parameters=["a"],
            ),
            OperationInfo(
                name="abs_diff",
                symbol="|a-b|",
                description="Calculate absolute difference between two numbers",
                parameters=["a", "b"],
            ),
            OperationInfo(
                name="cubic",
                symbol="³",
                description="Raise number to the power of 3 (cubic)",
                parameters=["a"],
            ),
        ]

        return OperationsResponse(operations=operations, count=len(operations))

    @router.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check for calculator service"""
        try:
            # Test a simple calculation
            test_result = await calculator_service.calculate("add", 1, 1)

            return HealthResponse(
                status="healthy",
                service="calculator",
                test_calculation="1 + 1 = 2",
                actual_result=test_result,
                timestamp=datetime.now(),
            )
        except Exception as e:
            logger.error("Calculator health check failed", error=str(e))

            raise HTTPException(
                status_code=503, detail=f"Calculator service unhealthy: {str(e)}"
            )


# Create router instance
calculator_router = CalculatorRouter()
