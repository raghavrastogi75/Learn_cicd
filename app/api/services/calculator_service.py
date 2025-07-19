import math
import time
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload
import structlog
from app.api.database.models import Calculation
from app.api.utils.logger import LoggerMixin
from app.api.utils.metrics import CALCULATION_COUNT, CALCULATION_LATENCY

logger = structlog.get_logger()


class CalculatorService(LoggerMixin):
    """Service for calculator operations"""

    async def calculate(
        self,
        operation: str,
        a: float,
        b: Optional[float] = None,
        session: AsyncSession = None,
    ) -> float:
        """Perform mathematical calculation"""
        start_time = time.time()
        try:
            result = None

            # Perform calculation based on operation
            if operation == "add":
                if b is None:
                    raise ValueError("Second operand is required for addition")
                result = a + b
            elif operation == "subtract":
                if b is None:
                    raise ValueError("Second operand is required for subtraction")
                result = a - b
            elif operation == "multiply":
                if b is None:
                    raise ValueError("Second operand is required for multiplication")
                result = a * b
            elif operation == "divide":
                if b is None:
                    raise ValueError("Second operand is required for division")
                if b == 0:
                    raise ValueError("Division by zero is not allowed")
                result = a / b
            elif operation == "power":
                if b is None:
                    raise ValueError("Second operand is required for power operation")
                result = math.pow(a, b)
            elif operation == "sqrt":
                if a < 0:
                    raise ValueError("Cannot calculate square root of negative number")
                result = math.sqrt(a)
            elif operation == "abs_diff":
                if b is None:
                    raise ValueError("Second operand is required for absolute difference")
                result = abs(a - b)
            elif operation == "cubic":
                # Cubic power: raise number to power of 3
                result = math.pow(a, 3)
            else:
                raise ValueError(f"Unsupported operation: {operation}")

            # Round to 8 decimal places to avoid floating point precision issues
            result = round(result, 8)

            # Store calculation in database
            await self._store_calculation(operation, a, b, result, session)

            # Record metrics
            duration = time.time() - start_time
            CALCULATION_COUNT.labels(operation=operation, status="success").inc()
            CALCULATION_LATENCY.labels(operation=operation).observe(duration)

            self.logger.info(
                "Calculation completed", operation=operation, a=a, b=b, result=result
            )

            return result

        except Exception as e:
            # Record error metrics
            duration = time.time() - start_time
            CALCULATION_COUNT.labels(operation=operation, status="error").inc()
            CALCULATION_LATENCY.labels(operation=operation).observe(duration)

            self.logger.error(
                "Calculation failed", operation=operation, a=a, b=b, error=str(e)
            )
            raise

    async def _store_calculation(
        self,
        operation: str,
        a: float,
        b: Optional[float],
        result: float,
        session: AsyncSession = None,
    ):
        """Store calculation in database"""
        try:
            calculation = Calculation(
                operation=operation, operand_a=a, operand_b=b, result=result
            )

            if session:
                session.add(calculation)
                await session.commit()
                await session.refresh(calculation)

                self.logger.info(
                    "Calculation stored in database", calculation_id=calculation.id
                )
            else:
                # If no session provided, we'll store it later
                self.logger.warning(
                    "No database session provided for storing calculation"
                )

        except Exception as e:
            self.logger.error(
                "Failed to store calculation in database",
                operation=operation,
                a=a,
                b=b,
                result=result,
                error=str(e),
            )
            # Don't raise error here as the calculation was successful

    async def get_history(
        self, limit: int = 10, offset: int = 0, session: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Get calculation history"""
        try:
            if not session:
                raise ValueError("Database session is required")

            query = (
                select(Calculation)
                .order_by(Calculation.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            calculations = result.scalars().all()

            return [calc.to_dict() for calc in calculations]

        except Exception as e:
            self.logger.error("Failed to get calculation history", error=str(e))
            raise

    async def get_statistics(self, session: AsyncSession = None) -> Dict[str, Any]:
        """Get calculation statistics"""
        try:
            if not session:
                raise ValueError("Database session is required")

            # Total calculations
            total_query = select(func.count(Calculation.id))
            total_result = await session.execute(total_query)
            total_calculations = total_result.scalar()

            # Most used operation
            operation_query = (
                select(
                    Calculation.operation,
                    func.count(Calculation.operation).label("count"),
                )
                .group_by(Calculation.operation)
                .order_by(func.count(Calculation.operation).desc())
                .limit(1)
            )
            operation_result = await session.execute(operation_query)
            most_used_operation = operation_result.first()

            # Average result
            avg_query = select(func.avg(Calculation.result))
            avg_result = await session.execute(avg_query)
            average_result = avg_result.scalar() or 0

            # Today's calculations
            today_query = select(func.count(Calculation.id)).where(
                func.date(Calculation.created_at) == func.current_date()
            )
            today_result = await session.execute(today_query)
            today_calculations = today_result.scalar()

            # This week's calculations
            week_query = select(func.count(Calculation.id)).where(
                Calculation.created_at >= func.now() - text("INTERVAL '7 days'")
            )
            week_result = await session.execute(week_query)
            week_calculations = week_result.scalar()

            return {
                "total_calculations": total_calculations,
                "most_used_operation": most_used_operation[0]
                if most_used_operation
                else None,
                "average_result": float(average_result),
                "today_calculations": today_calculations,
                "week_calculations": week_calculations,
            }

        except Exception as e:
            self.logger.error("Failed to get calculation statistics", error=str(e))
            raise

    async def clear_history(self, session: AsyncSession = None) -> int:
        """Clear all calculation history"""
        try:
            if not session:
                raise ValueError("Database session is required")

            result = await session.execute(select(func.count(Calculation.id)))
            count_before = result.scalar()

            await session.execute(text("DELETE FROM calculations"))
            await session.commit()

            self.logger.info("Calculation history cleared", deleted_count=count_before)
            return count_before

        except Exception as e:
            self.logger.error("Failed to clear calculation history", error=str(e))
            raise


# Create service instance
calculator_service = CalculatorService()
