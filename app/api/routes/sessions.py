from typing import List
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    SessionCreate, SessionResponse, TranscriptEntry, 
    FlagToggleRequest, TriageEscalationRequest, TriageAlertResponse
)
from app.services.session_manager import session_manager
from app.services.triage_service import triage_service

router = APIRouter(prefix="/api/sessions", tags=["Sessions & Transcripts"])

@router.get("", response_model=List[SessionResponse])
async def list_sessions():
    return session_manager.list_sessions()

@router.post("", response_model=SessionResponse)
async def create_new_session(payload: SessionCreate):
    session = session_manager.create_session(payload.facility_name, payload.department)
    return SessionResponse(
        session_id=session.session_id,
        facility_name=session.facility_name,
        department=session.department,
        created_at=session.created_at,
        is_active=session.is_active,
        patient_connected=False,
        clinician_connected=False
    )

@router.get("/{session_id}/transcript", response_model=List[TranscriptEntry])
async def get_session_transcript(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.transcripts

@router.post("/{session_id}/flag")
async def toggle_statement_flag(session_id: str, payload: FlagToggleRequest):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    updated_entry = session.toggle_flag(payload.entry_id)
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Transcript entry not found")
    
    return updated_entry

@router.post("/{session_id}/escalate", response_model=TriageAlertResponse)
async def escalate_session_triage(session_id: str, payload: TriageEscalationRequest):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return triage_service.create_escalation(payload)
