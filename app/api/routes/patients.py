import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import TriagePatient

router = APIRouter(prefix="/api/patients", tags=["Patient Triage & Intake Queue"])

class PatientCreateRequest(BaseModel):
    name: str
    symptom: str
    symptom_sw: Optional[str] = ""
    places: List[str] = []
    duration: str
    urgent: bool = False
    desk: Optional[str] = "Desk 1"
    lang: Optional[str] = "English"

class PatientStatusUpdateRequest(BaseModel):
    status: str

@router.get("", response_model=List[dict])
def list_patients(
    desk: Optional[str] = Query(None, description="Filter by desk"),
    status: Optional[str] = Query(None, description="Filter by status"),
    urgent: Optional[bool] = Query(None, description="Filter by urgency"),
    search: Optional[str] = Query(None, description="Search by name or symptom"),
    db: Session = Depends(get_db)
):
    query = db.query(TriagePatient)
    if desk and desk != "all":
        query = query.filter(TriagePatient.desk == desk)
    if status and status != "all":
        query = query.filter(TriagePatient.status == status)
    if urgent is not None:
        query = query.filter(TriagePatient.urgent == urgent)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (TriagePatient.name.ilike(search_filter)) |
            (TriagePatient.symptom.ilike(search_filter)) |
            (TriagePatient.symptom_sw.ilike(search_filter)) |
            (TriagePatient.id.ilike(search_filter))
        )
    patients = query.order_by(TriagePatient.urgent.desc(), TriagePatient.created_at.desc()).all()
    return [p.to_dict() for p in patients]

@router.get("/{patient_id}", response_model=dict)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(TriagePatient).filter(TriagePatient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return patient.to_dict()

@router.post("", response_model=dict, status_code=201)
def create_patient_intake(payload: PatientCreateRequest, db: Session = Depends(get_db)):
    count = db.query(TriagePatient).count()
    new_id = f"PT-{1043 + count}"

    new_patient = TriagePatient(
        id=new_id,
        name=payload.name,
        symptom=payload.symptom,
        symptom_sw=payload.symptom_sw or payload.symptom,
        places=json.dumps(payload.places),
        duration=payload.duration,
        urgent=payload.urgent,
        time="Just now",
        desk=payload.desk or "Desk 1",
        lang=payload.lang or "English",
        status="Waiting"
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient.to_dict()

@router.patch("/{patient_id}/status", response_model=dict)
def update_patient_status(patient_id: str, payload: PatientStatusUpdateRequest, db: Session = Depends(get_db)):
    patient = db.query(TriagePatient).filter(TriagePatient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")
    patient.status = payload.status
    db.commit()
    db.refresh(patient)
    return patient.to_dict()
