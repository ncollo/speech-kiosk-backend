import json
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime
from app.db.session import Base

class HospitalUser(Base):
    __tablename__ = "hospital_users"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    role = Column(String(64), nullable=False)
    department = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False, index=True)
    phone = Column(String(32), nullable=False)
    status = Column(String(32), default="Active", nullable=False)
    last_login = Column(String(64), default="Just now")
    badge_id = Column(String(32), unique=True, nullable=False, index=True)
    pin = Column(String(16), default="1234", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "lastLogin": self.last_login,
            "badgeId": self.badge_id
        }

class TriagePatient(Base):
    __tablename__ = "triage_patients"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    symptom = Column(String(128), nullable=False)
    symptom_sw = Column(String(128), nullable=False)
    places = Column(Text, nullable=False)  # JSON-encoded array
    duration = Column(String(64), nullable=False)
    urgent = Column(Boolean, default=False, nullable=False)
    time = Column(String(64), default="Just now")
    desk = Column(String(32), default="Desk 1", nullable=False)
    lang = Column(String(64), default="English", nullable=False)
    status = Column(String(32), default="Waiting", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        places_list = []
        try:
            places_list = json.loads(self.places) if self.places else []
        except Exception:
            places_list = [p.strip() for p in self.places.split(",") if p.strip()]

        return {
            "id": self.id,
            "name": self.name,
            "symptom": self.symptom,
            "symptomSw": self.symptom_sw,
            "places": places_list,
            "duration": self.duration,
            "urgent": self.urgent,
            "time": self.time,
            "desk": self.desk,
            "lang": self.lang,
            "status": self.status
        }

class KioskTerminal(Base):
    __tablename__ = "kiosk_terminals"

    id = Column(String(32), primary_key=True, index=True)
    desk_number = Column(String(32), nullable=False)
    facility = Column(String(128), nullable=False)
    device_type = Column(String(64), default="Surface Pro 9 Kiosk Mount")
    latency_ms = Column(Integer, default=180)
    status = Column(String(32), default="Online")
    last_ping = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "deskNumber": self.desk_number,
            "facility": self.facility,
            "deviceType": self.device_type,
            "latencyMs": self.latency_ms,
            "status": self.status,
            "lastPing": self.last_ping.isoformat() if self.last_ping else None
        }

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    event_type = Column(String(64), nullable=False)
    staff_id = Column(String(32), nullable=True)
    terminal_id = Column(String(32), nullable=True)
    details = Column(Text, nullable=False)
    dpa_compliant = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "eventType": self.event_type,
            "staffId": self.staff_id,
            "terminalId": self.terminal_id,
            "details": self.details,
            "dpaCompliant": self.dpa_compliant
        }
