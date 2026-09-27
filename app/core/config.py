from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "ClearCaption Hospital Kiosk API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Facility defaults
    DEFAULT_FACILITY: str = "St. Mary's Medical Center"
    DEFAULT_DEPARTMENT: str = "Reception & Triage"
    
    # Audio & Transcription settings
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHUNK_DURATION_MS: int = 250
    LATENCY_THRESHOLD_MS: int = 300
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
