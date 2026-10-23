from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import AuditLog

router = APIRouter(prefix="/api/audit", tags=["DPA Compliance & Audit Logs"])

class AuditLogCreateRequest(BaseModel):
    event_type: str
    details: str
    staff_id: Optional[str] = None
    terminal_id: Optional[str] = None
    dpa_compliant: Optional[bool] = True

@router.get("/logs", response_model=List[dict])
def list_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return [l.to_dict() for l in logs]

@router.post("/logs", response_model=dict, status_code=201)
def record_audit_log(payload: AuditLogCreateRequest, db: Session = Depends(get_db)):
    log = AuditLog(
        event_type=payload.event_type,
        details=payload.details,
        staff_id=payload.staff_id,
        terminal_id=payload.terminal_id,
        dpa_compliant=payload.dpa_compliant if payload.dpa_compliant is not None else True
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log.to_dict()
