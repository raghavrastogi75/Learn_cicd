import pytest
from unittest.mock import AsyncMock, MagicMock
from app.api.services.calculator_service import CalculatorService
from app.api.database.models import Calculation


@pytest.fixture
def calculator_service():
    return CalculatorService()


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


class TestCalculatorService:
    """Test cases for CalculatorService"""

    @pytest.mark.asyncio
    async def test_add_operation(self, calculator_service, mock_session):
        """Test addition operation"""
        result = await calculator_service.calculate("add", 5, 3, mock_session)
        assert result == 8.0

        # Verify calculation was stored
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_subtract_operation(self, calculator_service, mock_session):
        """Test subtraction operation"""
        result = await calculator_service.calculate("subtract", 10, 4, mock_session)
        assert result == 6.0

    @pytest.mark.asyncio
    async def test_multiply_operation(self, calculator_service, mock_session):
        """Test multiplication operation"""
        result = await calculator_service.calculate("multiply", 6, 7, mock_session)
        assert result == 42.0

    @pytest.mark.asyncio
    async def test_divide_operation(self, calculator_service, mock_session):
        """Test division operation"""
        result = await calculator_service.calculate("divide", 15, 3, mock_session)
        assert result == 5.0

    @pytest.mark.asyncio
    async def test_power_operation(self, calculator_service, mock_session):
        """Test power operation"""
        result = await calculator_service.calculate("power", 2, 3, mock_session)
        assert result == 8.0

    @pytest.mark.asyncio
    async def test_sqrt_operation(self, calculator_service, mock_session):
        """Test square root operation"""
        result = await calculator_service.calculate("sqrt", 16, None, mock_session)
        assert result == 4.0

    @pytest.mark.asyncio
    async def test_abs_diff_operation(self, calculator_service, mock_session):
        """Test absolute difference operation"""
        # Test positive difference
        result = await calculator_service.calculate("abs_diff", 10, 3, mock_session)
        assert result == 7.0

        # Test negative difference (should be positive)
        result = await calculator_service.calculate("abs_diff", 3, 10, mock_session)
        assert result == 7.0

        # Test same numbers
        result = await calculator_service.calculate("abs_diff", 5, 5, mock_session)
        assert result == 0.0

    @pytest.mark.asyncio
    async def test_division_by_zero(self, calculator_service, mock_session):
        """Test division by zero error"""
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            await calculator_service.calculate("divide", 10, 0, mock_session)

    @pytest.mark.asyncio
    async def test_sqrt_negative_number(self, calculator_service, mock_session):
        """Test square root of negative number error"""
        with pytest.raises(
            ValueError, match="Cannot calculate square root of negative number"
        ):
            await calculator_service.calculate("sqrt", -4, None, mock_session)

    @pytest.mark.asyncio
    async def test_invalid_operation(self, calculator_service, mock_session):
        """Test invalid operation error"""
        with pytest.raises(ValueError, match="Unsupported operation"):
            await calculator_service.calculate("invalid", 1, 1, mock_session)

    @pytest.mark.asyncio
    async def test_floating_point_precision(self, calculator_service, mock_session):
        """Test floating point precision handling"""
        result = await calculator_service.calculate("divide", 1, 3, mock_session)
        assert result == 0.33333333  # Rounded to 8 decimal places

    @pytest.mark.asyncio
    async def test_store_calculation_success(self, calculator_service, mock_session):
        """Test successful calculation storage"""
        calculation = Calculation(operation="add", operand_a=5, operand_b=3, result=8.0)

        await calculator_service._store_calculation("add", 5, 3, 8.0, mock_session)

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_store_calculation_no_session(self, calculator_service):
        """Test calculation storage without session"""
        # Should not raise an error, just log a warning
        await calculator_service._store_calculation("add", 5, 3, 8.0, None)

    @pytest.mark.asyncio
    async def test_get_history(self, calculator_service, mock_session):
        """Test getting calculation history"""
        # Mock database query result
        mock_calculation = MagicMock()
        mock_calculation.to_dict.return_value = {
            "id": 1,
            "operation": "add",
            "operand_a": 5,
            "operand_b": 3,
            "result": 8.0,
            "created_at": "2024-01-01T00:00:00Z",
        }

        # Fix the mocking chain
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_calculation]
        mock_session.execute.return_value = mock_result

        result = await calculator_service.get_history(
            limit=10, offset=0, session=mock_session
        )

        assert len(result) == 1
        assert result[0]["operation"] == "add"
        assert result[0]["result"] == 8.0

    @pytest.mark.asyncio
    async def test_get_history_no_session(self, calculator_service):
        """Test getting history without session"""
        with pytest.raises(ValueError, match="Database session is required"):
            await calculator_service.get_history()

    @pytest.mark.asyncio
    async def test_get_statistics(self, calculator_service, mock_session):
        """Test getting calculation statistics"""
        # Mock database query results
        mock_result = MagicMock()
        mock_result.scalar.side_effect = [100, 25.5, 10, 50]
        mock_result.first.return_value = ("add", 30)
        mock_session.execute.return_value = mock_result

        result = await calculator_service.get_statistics(session=mock_session)

        assert result["total_calculations"] == 100
        assert result["most_used_operation"] == "add"
        assert result["average_result"] == 25.5
        assert result["today_calculations"] == 10
        assert result["week_calculations"] == 50

    @pytest.mark.asyncio
    async def test_clear_history(self, calculator_service, mock_session):
        """Test clearing calculation history"""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 50
        mock_session.execute.return_value = mock_result

        result = await calculator_service.clear_history(session=mock_session)

        assert result == 50
        mock_session.execute.assert_called()
        mock_session.commit.assert_called_once()
