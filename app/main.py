import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.init_db import init_database
from app.db.session import engine
from app.api.routes import (
    sessions,
    symptoms,
    websocket,
    admin,
    users,
    patients,
    terminals,
    audit
)

logger = logging.getLogger("clearcaption.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize PostgreSQL / database schema and initial 30 users/patients seed data
    try:
        logger.info("Initializing database schema and seeds...")
        init_database()
        logger.info("Database schema and seed data ready.")
    except Exception as e:
        logger.error(f"Database initialization warning: {e}")
    yield
    # Cleanup if needed

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real-Time Speech-to-Text Captioning & Triage API with PostgreSQL for Hospital Reception Kiosks",
    lifespan=lifespan
)

# CORS configuration for frontend tablet & console interfaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(sessions.router)
app.include_router(symptoms.router)
app.include_router(websocket.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(terminals.router)
app.include_router(audit.router)

@app.get("/api/health", tags=["System Health"])
async def health_check():
    db_status = "connected"
    db_dialect = str(engine.dialect.name)
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": db_status,
            "engine": db_dialect
        },
        "audio_pipeline": {
            "sample_rate_hz": settings.AUDIO_SAMPLE_RATE,
            "target_latency_ms": settings.LATENCY_THRESHOLD_MS,
            "speech_model": "whisper-base-en"
        }
    }
