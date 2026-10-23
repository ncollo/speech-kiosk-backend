from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import KioskTerminal

router = APIRouter(prefix="/api/terminals", tags=["Kiosk Hardware Terminals Fleet"])

@router.get("", response_model=List[dict])
def list_terminals(db: Session = Depends(get_db)):
    terminals = db.query(KioskTerminal).order_by(KioskTerminal.desk_number.asc()).all()
    return [t.to_dict() for t in terminals]

@router.post("/{terminal_id}/ping", response_model=dict)
def ping_terminal(terminal_id: str, db: Session = Depends(get_db)):
    terminal = db.query(KioskTerminal).filter(KioskTerminal.id == terminal_id).first()
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    terminal.last_ping = datetime.utcnow()
    terminal.status = "Online"
    db.commit()
    db.refresh(terminal)
    return terminal.to_dict()
