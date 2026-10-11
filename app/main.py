from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import sessions, symptoms, websocket, admin

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real-Time Speech-to-Text Captioning & Triage API for Hospital Reception Kiosks"
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

@app.get("/api/health", tags=["System Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "audio_pipeline": {
            "sample_rate_hz": settings.AUDIO_SAMPLE_RATE,
            "target_latency_ms": settings.LATENCY_THRESHOLD_MS,
            "speech_model": "whisper-base-en"
        }
    }
