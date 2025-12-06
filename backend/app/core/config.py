"""
Application Configuration
Manages environment variables and settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "Quantum"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://quantum:quantum@localhost:5432/quantum"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    
    # Keycloak
    KEYCLOAK_SERVER_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "quantum"
    KEYCLOAK_CLIENT_ID: str = "quantum-backend"
    KEYCLOAK_CLIENT_SECRET: Optional[str] = None
    
    # ML Service
    ML_SERVICE_URL: str = "http://localhost:8001"
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:4200",
        "http://localhost:3000",
    ]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
