from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import structlog
from datetime import datetime

from app.api.models.history import (
    HistoryResponse,
    StatisticsResponse,
    ClearHistoryResponse,
    CalculationHistory,
)
from app.api.services.calculator_service import calculator_service
from app.api.database.connection import get_db
from app.api.utils.logger import LoggerMixin

router = APIRouter()
logger = structlog.get_logger()


class HistoryRouter(LoggerMixin):
    """History router for calculation history operations"""

    @router.get("/", response_model=HistoryResponse)
    async def get_history(
        limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
        offset: int = Query(0, ge=0, description="Number of records to skip"),
        db: AsyncSession = Depends(get_db),
    ):
        """Get calculation history with pagination"""
        try:
            history_data = await calculator_service.get_history(
                limit=limit, offset=offset, session=db
            )

            # Convert to Pydantic models
            calculations = [CalculationHistory(**calc) for calc in history_data]

            return HistoryResponse(
                success=True,
                data=calculations,
                pagination={
                    "limit": limit,
                    "offset": offset,
                    "count": len(calculations),
                },
                timestamp=datetime.now(),
            )

        except Exception as e:
            logger.error("Failed to fetch calculation history", error=str(e))
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.get("/statistics", response_model=StatisticsResponse)
    async def get_statistics(db: AsyncSession = Depends(get_db)):
        """Get calculation statistics"""
        try:
            stats = await calculator_service.get_statistics(session=db)

            return StatisticsResponse(
                success=True, data=stats, timestamp=datetime.now()
            )

        except Exception as e:
            logger.error("Failed to fetch calculation statistics", error=str(e))
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.delete("/", response_model=ClearHistoryResponse)
    async def clear_history(db: AsyncSession = Depends(get_db)):
        """Clear all calculation history"""
        try:
            deleted_count = await calculator_service.clear_history(session=db)

            return ClearHistoryResponse(
                success=True,
                message="Calculation history cleared successfully",
                deleted_count=deleted_count,
                timestamp=datetime.now(),
            )

        except Exception as e:
            logger.error("Failed to clear calculation history", error=str(e))
            raise HTTPException(status_code=500, detail="Internal server error")


# Create router instance
history_router = HistoryRouter()
