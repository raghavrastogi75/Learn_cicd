import logging
import sys
from typing import Any, Dict

import structlog

from app.api.utils.config import config as settings


def setup_logging():
    """Setup structured logging configuration"""

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            (
                structlog.processors.JSONRenderer()
                if settings.LOG_FORMAT == "json"
                else structlog.dev.ConsoleRenderer()
            ),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )

    # Set log levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("redis").setLevel(logging.WARNING)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin to add logging capabilities to classes"""

    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger for this class"""
        return structlog.get_logger(self.__class__.__name__)


def log_request(request_data: Dict[str, Any], logger: structlog.BoundLogger = None):
    """Log request data in a structured way"""
    if logger is None:
        logger = get_logger("request")

    logger.info(
        "Request received",
        method=request_data.get("method"),
        url=request_data.get("url"),
        client_ip=request_data.get("client_ip"),
        user_agent=request_data.get("user_agent"),
        request_id=request_data.get("request_id"),
    )


def log_response(response_data: Dict[str, Any], logger: structlog.BoundLogger = None):
    """Log response data in a structured way"""
    if logger is None:
        logger = get_logger("response")

    logger.info(
        "Response sent",
        status_code=response_data.get("status_code"),
        process_time=response_data.get("process_time"),
        request_id=response_data.get("request_id"),
    )


def log_error(error_data: Dict[str, Any], logger: structlog.BoundLogger = None):
    """Log error data in a structured way"""
    if logger is None:
        logger = get_logger("error")

    logger.error(
        "Error occurred",
        error_type=error_data.get("error_type"),
        error_message=error_data.get("error_message"),
        request_id=error_data.get("request_id"),
        url=error_data.get("url"),
        method=error_data.get("method"),
    )
