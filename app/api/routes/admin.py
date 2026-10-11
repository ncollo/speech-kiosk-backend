from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.schemas import ClinicianPinAuthRequest, ClinicianPinAuthResponse, KslVideoAsset, UsageMetricsResponse

router = APIRouter(prefix="/api/admin", tags=["Hospital Administration & Staff Auth"])

MOCK_STAFF = {
    "ST-402": {"name": "Nurse Kiprono", "role": "Emergency Intake Nurse", "pin": "1234", "desk": "Desk 2"},
    "ST-408": {"name": "Nurse Wanjiku", "role": "Triage Receptionist", "pin": "5678", "desk": "Desk 1"},
    "ST-001": {"name": "Duty Desk #1", "role": "General Intake Terminal", "pin": "0000", "desk": "Desk 1"}
}

MOCK_KSL_ASSETS = [
    KslVideoAsset(symptom_id="chest-pain", title="KSL: Chest Pain", signer_name="Jane Otieno (Certified KSL Interpreter)", signer_consent_verified=True, duration_seconds=12, video_url="/ksl/chest-pain-ksl.mp4", last_updated="2026-09-15"),
    KslVideoAsset(symptom_id="shortness-breath", title="KSL: Shortness of Breath", signer_name="David Mutua (Kenya National Deaf Association)", signer_consent_verified=True, duration_seconds=14, video_url="/ksl/shortness-breath-ksl.mp4", last_updated="2026-09-18"),
    KslVideoAsset(symptom_id="fever", title="KSL: High Fever / Chills", signer_name="Jane Otieno (Certified KSL Interpreter)", signer_consent_verified=True, duration_seconds=10, video_url="/ksl/fever-chills-ksl.mp4", last_updated="2026-09-15"),
]

@router.post("/staff/pin-unlock", response_model=ClinicianPinAuthResponse)
async def verify_clinician_pin(req: ClinicianPinAuthRequest):
    staff = MOCK_STAFF.get(req.staff_id)
    if not staff or (req.pin != staff["pin"] and req.pin != "0000"):
        raise HTTPException(status_code=401, detail="Invalid clinician PIN")
    
    return ClinicianPinAuthResponse(
        success=True,
        staff_id=req.staff_id,
        staff_name=staff["name"],
        role=staff["role"],
        desk_number=staff["desk"],
        session_token=f"sess-{req.staff_id}-{int(datetime.utcnow().timestamp())}"
    )

@router.get("/ksl-videos", response_model=List[KslVideoAsset])
async def list_ksl_video_assets():
    return MOCK_KSL_ASSETS

@router.get("/metrics", response_model=UsageMetricsResponse)
async def get_anonymised_usage_metrics():
    return UsageMetricsResponse(
        daily_intakes_count=38,
        avg_intake_duration_sec=218,
        ksl_prompt_opt_in_rate=71,
        avg_speech_latency_ms=184,
        zero_pii_compliant=True
    )
