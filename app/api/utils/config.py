import os
from enum import Enum


class Environment(str, Enum):
    """Environment types"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Config:
    """Application configuration with environment-specific settings"""

    # Environment detection
    ENVIRONMENT: Environment = Environment(
        os.getenv("ENVIRONMENT", "development").lower()
    )

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "1"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://calculator:password@localhost:5432/calculator_dev",
    )
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))

    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")

    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "*").split(",")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    # Monitoring Configuration
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "8001"))

    # Feature Flags
    ENABLE_ABS_DIFF: bool = os.getenv("ENABLE_ABS_DIFF", "true").lower() == "true"
    ENABLE_HISTORY: bool = os.getenv("ENABLE_HISTORY", "true").lower() == "true"

    @classmethod
    def get_environment_specific_config(cls) -> dict:
        """Get environment-specific configuration"""
        base_config = {
            "environment": cls.ENVIRONMENT.value,
            "debug": cls.DEBUG,
            "log_level": cls.LOG_LEVEL,
            "rate_limit": cls.RATE_LIMIT_PER_MINUTE,
            "enable_metrics": cls.ENABLE_METRICS,
            "feature_flags": {
                "abs_diff": cls.ENABLE_ABS_DIFF,
                "history": cls.ENABLE_HISTORY,
            },
        }

        if cls.ENVIRONMENT == Environment.DEVELOPMENT:
            base_config.update(
                {
                    "debug": True,
                    "log_level": "DEBUG",
                    "rate_limit": 1000,  # Higher limits for development
                    "enable_metrics": True,
                }
            )
        elif cls.ENVIRONMENT == Environment.STAGING:
            base_config.update(
                {
                    "debug": False,
                    "log_level": "INFO",
                    "rate_limit": 100,
                    "enable_metrics": True,
                }
            )
        elif cls.ENVIRONMENT == Environment.PRODUCTION:
            base_config.update(
                {
                    "debug": False,
                    "log_level": "WARNING",
                    "rate_limit": 60,
                    "enable_metrics": True,
                }
            )

        return base_config

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.ENVIRONMENT == Environment.DEVELOPMENT

    @classmethod
    def is_staging(cls) -> bool:
        """Check if running in staging environment"""
        return cls.ENVIRONMENT == Environment.STAGING

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT == Environment.PRODUCTION


# Global config instance
config = Config()
