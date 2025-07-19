from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.api.database.connection import Base


class Calculation(Base):
    """Model for storing calculation history"""

    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String(50), nullable=False, index=True)
    operand_a = Column(Float, nullable=False)
    operand_b = Column(Float, nullable=True)
    result = Column(Float, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    def __repr__(self):
        return (
            f"<Calculation(id={self.id}, operation='{self.operation}', "
            f"result={self.result})>"
        )

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "operation": self.operation,
            "operand_a": self.operand_a,
            "operand_b": self.operand_b,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
