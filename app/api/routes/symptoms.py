from typing import List
from fastapi import APIRouter, HTTPException
from app.models.schemas import SymptomItem, SymptomSelectionPayload
from app.services.session_manager import session_manager
from app.services.triage_service import triage_service

router = APIRouter(prefix="/api/symptoms", tags=["Symptoms & ASL"])

SYMPTOM_CATALOG: List[SymptomItem] = [
    SymptomItem(id="chest-pain", label="Chest Pain", urgency_level="emergency", asl_video_url="/asl/chest-pain.mp4", icon_name="heart", description="Tightness or pressure in chest area"),
    SymptomItem(id="shortness-of-breath", label="Shortness of Breath", urgency_level="emergency", asl_video_url="/asl/shortness-of-breath.mp4", icon_name="lungs", description="Difficulty inhaling or breathing"),
    SymptomItem(id="nausea-vomiting", label="Nausea / Vomiting", urgency_level="routine", asl_video_url="/asl/nausea.mp4", icon_name="stomach", description="Upset stomach or sickness"),
    SymptomItem(id="dizziness", label="Dizziness", urgency_level="urgent", asl_video_url="/asl/dizziness.mp4", icon_name="spin", description="Loss of balance or lightheadedness"),
    SymptomItem(id="headache", label="Headache", urgency_level="urgent", asl_video_url="/asl/headache.mp4", icon_name="head", description="Severe head pain or migraine"),
    SymptomItem(id="fever-chills", label="Fever / Chills", urgency_level="urgent", asl_video_url="/asl/fever.mp4", icon_name="thermometer", description="High temperature or shivering"),
    SymptomItem(id="abdominal-pain", label="Abdominal Pain", urgency_level="urgent", asl_video_url="/asl/abdomen.mp4", icon_name="abdomen", description="Localized abdominal cramps or aches"),
    SymptomItem(id="swelling", label="Swelling", urgency_level="routine", asl_video_url="/asl/swelling.mp4", icon_name="swelling", description="Inflammation of limbs or joints"),
    SymptomItem(id="fatigue", label="Fatigue", urgency_level="routine", asl_video_url="/asl/fatigue.mp4", icon_name="battery", description="Extreme exhaustion or weakness"),
    SymptomItem(id="other", label="Other Concern", urgency_level="routine", asl_video_url="/asl/other.mp4", icon_name="plus", description="Other symptoms to describe to nurse")
]

@router.get("/catalog", response_model=List[SymptomItem])
async def get_symptom_catalog():
    return SYMPTOM_CATALOG

@router.post("/select")
async def record_symptom_selection(payload: SymptomSelectionPayload):
    session = session_manager.get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.selected_symptom_ids.append(payload.symptom_id)
    urgency = triage_service.evaluate_urgency(payload.symptom_id)
    
    return {
        "status": "recorded",
        "symptom_id": payload.symptom_id,
        "urgency": urgency,
        "session_id": payload.session_id
    }
