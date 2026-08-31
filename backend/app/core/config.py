import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PharmaShield"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pharmashield.db")
    
    JWT_SECRET: str = os.getenv("JWT_SECRET", "pharmashield_hackathon_super_secret_jwt_key_2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "gemini-1.5-pro")
    
    SAP_BASE_URL: str = os.getenv("SAP_BASE_URL", "https://mock-sap.pharmashield.local")
    SAP_MODE: str = os.getenv("SAP_MODE", "MOCK")
    
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]

settings = Settings()
