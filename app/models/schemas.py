from typing import Optional, List, Literal
from datetime import datetime
from pydantic import BaseModel, Field

SpeakerRole = Literal["clinician", "patient", "system"]
ClientType = Literal["patient", "clinician"]
TriageUrgency = Literal["routine", "urgent", "emergency"]
ConnectionStatus = Literal["listening", "reconnecting", "idle"]

class SymptomItem(BaseModel):
    id: str
    label: str
    urgency_level: TriageUrgency = "routine"
    asl_video_url: str
    icon_name: str
    description: Optional[str] = None

class SymptomSelectionPayload(BaseModel):
    symptom_id: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

class TranscriptEntryCreate(BaseModel):
    speaker: SpeakerRole
    text: str
    is_flagged: bool = False
    is_highlighted: bool = False

class TranscriptEntry(BaseModel):
    id: str
    speaker: SpeakerRole
    text: str
    timestamp: str
    is_flagged: bool = False
    is_highlighted: bool = False

class SessionCreate(BaseModel):
    facility_name: Optional[str] = "St. Mary's Medical Center"
    department: Optional[str] = "Reception"

class SessionResponse(BaseModel):
    session_id: str
    facility_name: str
    department: str
    created_at: datetime
    is_active: bool
    patient_connected: bool
    clinician_connected: bool

class FlagToggleRequest(BaseModel):
    entry_id: str
    is_flagged: bool

class TriageEscalationRequest(BaseModel):
    session_id: str
    reason: str
    request_interpreter: bool = False
    urgency: TriageUrgency = "urgent"

class TriageAlertResponse(BaseModel):
    alert_id: str
    session_id: str
    status: str
    urgency: TriageUrgency
    interpreter_dispatched: bool
    timestamp: datetime

class WebSocketCaptionEvent(BaseModel):
    type: Literal["caption_delta", "caption_final", "symptom_alert", "flag_update", "status_change"]
    session_id: str
    speaker: SpeakerRole = "clinician"
    text: Optional[str] = None
    previous_text: Optional[str] = None
    entry_id: Optional[str] = None
    symptom: Optional[SymptomItem] = None
    timestamp: str
