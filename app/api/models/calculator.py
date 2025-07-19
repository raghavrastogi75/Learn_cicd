from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, Field, validator


class CalculationRequest(BaseModel):
    """Request model for calculator operations"""

    operation: Literal[
        "add", "subtract", "multiply", "divide", "power", "sqrt", "abs_diff", "cubic"
    ] = Field(..., description="Mathematical operation to perform")
    a: float = Field(..., description="First operand")
    b: Optional[float] = Field(
        None, description="Second operand (not required for sqrt)"
    )

    @validator("a", "b")
    def validate_numbers(cls, v):
        """Validate that numbers are finite"""
        if v is not None and not (
            isinstance(v, (int, float)) and v == v
        ):  # Check for NaN
            raise ValueError("Number must be finite")
        return v

    @validator("b")
    def validate_second_operand(cls, v, values):
        """Validate second operand based on operation"""
        operation = values.get("operation")
        if operation not in ["sqrt", "cubic"] and v is None:
            raise ValueError("Second operand is required for this operation")
        return v


class CalculationResponse(BaseModel):
    """Response model for calculator operations"""

    success: bool = Field(..., description="Whether the calculation was successful")
    operation: str = Field(..., description="The operation performed")
    a: float = Field(..., description="First operand")
    b: Optional[float] = Field(None, description="Second operand")
    result: float = Field(..., description="Calculation result")
    timestamp: datetime = Field(..., description="When the calculation was performed")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class OperationInfo(BaseModel):
    """Model for operation information"""

    name: str = Field(..., description="Operation name")
    symbol: str = Field(..., description="Mathematical symbol")
    description: str = Field(..., description="Operation description")
    parameters: list[str] = Field(..., description="Required parameters")


class OperationsResponse(BaseModel):
    """Response model for available operations"""

    operations: list[OperationInfo] = Field(
        ..., description="List of available operations"
    )
    count: int = Field(..., description="Number of available operations")


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[list] = Field(None, description="Validation error details")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    test_calculation: Optional[str] = Field(
        None, description="Test calculation performed"
    )
    actual_result: Optional[float] = Field(None, description="Actual result of test")
    timestamp: datetime = Field(..., description="Health check timestamp")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
