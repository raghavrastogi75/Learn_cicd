from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CalculationHistory(BaseModel):
    """Model for calculation history entry"""

    id: int = Field(..., description="Calculation ID")
    operation: str = Field(..., description="Mathematical operation")
    operand_a: float = Field(..., description="First operand")
    operand_b: Optional[float] = Field(None, description="Second operand")
    result: float = Field(..., description="Calculation result")
    created_at: datetime = Field(..., description="When calculation was performed")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class HistoryResponse(BaseModel):
    """Response model for calculation history"""

    success: bool = Field(..., description="Whether the request was successful")
    data: List[CalculationHistory] = Field(..., description="List of calculations")
    pagination: dict = Field(..., description="Pagination information")
    timestamp: datetime = Field(..., description="Response timestamp")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class Statistics(BaseModel):
    """Model for calculation statistics"""

    total_calculations: int = Field(..., description="Total number of calculations")
    most_used_operation: Optional[str] = Field(
        None, description="Most frequently used operation"
    )
    average_result: float = Field(..., description="Average of all results")
    today_calculations: int = Field(..., description="Calculations performed today")
    week_calculations: int = Field(..., description="Calculations performed this week")


class StatisticsResponse(BaseModel):
    """Response model for calculation statistics"""

    success: bool = Field(..., description="Whether the request was successful")
    data: Statistics = Field(..., description="Calculation statistics")
    timestamp: datetime = Field(..., description="Response timestamp")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class ClearHistoryResponse(BaseModel):
    """Response model for clearing history"""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Success message")
    deleted_count: int = Field(..., description="Number of records deleted")
    timestamp: datetime = Field(..., description="Response timestamp")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
