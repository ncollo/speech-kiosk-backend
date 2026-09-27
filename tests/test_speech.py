import pytest
from app.services.speech_service import speech_engine
from app.services.triage_service import triage_service

@pytest.mark.asyncio
async def test_speech_engine_ready():
    assert speech_engine.is_ready is True
    assert speech_engine.sample_rate == 16000

def test_triage_urgency_evaluation():
    urgency_chest_pain = triage_service.evaluate_urgency("chest-pain")
    assert urgency_chest_pain == "emergency"

    urgency_fatigue = triage_service.evaluate_urgency("fatigue")
    assert urgency_fatigue == "routine"
