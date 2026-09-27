import uuid
from typing import Dict, List, Optional, Set
from datetime import datetime
from fastapi import WebSocket
from app.models.schemas import TranscriptEntry, SessionResponse

class KioskSession:
    def __init__(self, session_id: str, facility_name: str, department: str):
        self.session_id = session_id
        self.facility_name = facility_name
        self.department = department
        self.created_at = datetime.utcnow()
        self.is_active = True
        self.transcripts: List[TranscriptEntry] = []
        self.patient_sockets: Set[WebSocket] = set()
        self.clinician_sockets: Set[WebSocket] = set()
        self.selected_symptom_ids: List[str] = []

    def add_transcript(self, speaker: str, text: str, is_flagged: bool = False, is_highlighted: bool = False) -> TranscriptEntry:
        entry_id = str(uuid.uuid4())[:8]
        entry = TranscriptEntry(
            id=entry_id,
            speaker=speaker,
            text=text,
            timestamp=datetime.now().strftime("%H:%M"),
            is_flagged=is_flagged,
            is_highlighted=is_highlighted
        )
        self.transcripts.append(entry)
        return entry

    def toggle_flag(self, entry_id: str) -> Optional[TranscriptEntry]:
        for entry in self.transcripts:
            if entry.id == entry_id:
                entry.is_flagged = not entry.is_flagged
                return entry
        return None

class SessionManager:
    def __init__(self):
        self._sessions: Dict[str, KioskSession] = {}
        # Pre-populate default session
        default_id = "st-marys-001"
        default_session = KioskSession(
            session_id=default_id,
            facility_name="St. Mary's Medical Center",
            department="Reception"
        )
        default_session.add_transcript("clinician", "Good morning, welcome to St. Mary's reception.")
        default_session.add_transcript("clinician", "I have been experiencing chest tightness since this morning.", is_flagged=True, is_highlighted=True)
        default_session.add_transcript("clinician", "The pain is about a six out of ten, maybe a seven.", is_flagged=True, is_highlighted=True)
        default_session.add_transcript("clinician", "Can you tell me when this started?")
        default_session.add_transcript("patient", "It started around eight AM, after I had breakfast.")
        self._sessions[default_id] = default_session

    def create_session(self, facility_name: str, department: str) -> KioskSession:
        session_id = f"kiosk-{str(uuid.uuid4())[:8]}"
        session = KioskSession(session_id, facility_name, department)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[KioskSession]:
        return self._sessions.get(session_id)

    def list_sessions(self) -> List[SessionResponse]:
        return [
            SessionResponse(
                session_id=s.session_id,
                facility_name=s.facility_name,
                department=s.department,
                created_at=s.created_at,
                is_active=s.is_active,
                patient_connected=len(s.patient_sockets) > 0,
                clinician_connected=len(s.clinician_sockets) > 0
            )
            for s in self._sessions.values()
        ]

session_manager = SessionManager()
