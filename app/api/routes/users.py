from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db.session import get_db
from app.db.models import HospitalUser

router = APIRouter(prefix="/api/users", tags=["Hospital Users & Staff Directory"])

class UserCreateRequest(BaseModel):
    name: str
    role: str
    department: str
    email: str
    phone: str
    badge_id: str
    status: Optional[str] = "Active"
    pin: Optional[str] = "1234"

class UserStatusUpdateRequest(BaseModel):
    status: str

class PinAuthRequest(BaseModel):
    badge_id: Optional[str] = None
    pin: str
    role_hint: Optional[str] = None

@router.get("", response_model=List[dict])
def list_hospital_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    status: Optional[str] = Query(None, description="Filter by duty status"),
    search: Optional[str] = Query(None, description="Search by name, email or department"),
    db: Session = Depends(get_db)
):
    query = db.query(HospitalUser)
    if role and role != "all":
        query = query.filter(HospitalUser.role == role)
    if status and status != "all":
        query = query.filter(HospitalUser.status == status)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (HospitalUser.name.ilike(search_filter)) |
            (HospitalUser.email.ilike(search_filter)) |
            (HospitalUser.department.ilike(search_filter)) |
            (HospitalUser.badge_id.ilike(search_filter))
        )
    users = query.all()
    return [u.to_dict() for u in users]

@router.get("/{user_id}", response_model=dict)
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(HospitalUser).filter(HospitalUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Staff user not found")
    return user.to_dict()

@router.post("", response_model=dict, status_code=201)
def create_hospital_user(payload: UserCreateRequest, db: Session = Depends(get_db)):
    existing = db.query(HospitalUser).filter(
        (HospitalUser.email == payload.email) | (HospitalUser.badge_id == payload.badge_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with email or badge ID already exists")

    count = db.query(HospitalUser).count()
    new_id = f"USR-{count + 1:02d}"
    
    new_user = HospitalUser(
        id=new_id,
        name=payload.name,
        role=payload.role,
        department=payload.department,
        email=payload.email,
        phone=payload.phone,
        badge_id=payload.badge_id,
        status=payload.status or "Active",
        pin=payload.pin or "1234",
        last_login="Just now"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.to_dict()

@router.patch("/{user_id}/status", response_model=dict)
def update_user_status(user_id: str, payload: UserStatusUpdateRequest, db: Session = Depends(get_db)):
    user = db.query(HospitalUser).filter(HospitalUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Staff user not found")
    user.status = payload.status
    db.commit()
    db.refresh(user)
    return user.to_dict()

@router.post("/auth/pin", response_model=dict)
def authenticate_pin(payload: PinAuthRequest, db: Session = Depends(get_db)):
    # Master administrator PIN
    if payload.pin == "9900":
        admin_user = db.query(HospitalUser).filter(HospitalUser.role == "Hospital Administrator").first()
        return {
            "authenticated": True,
            "role": "admin",
            "user": admin_user.to_dict() if admin_user else None
        }

    # Master clinician PIN
    if payload.pin == "4821":
        nurse_user = db.query(HospitalUser).filter(HospitalUser.role == "Triage Nurse").first()
        return {
            "authenticated": True,
            "role": "nurse",
            "user": nurse_user.to_dict() if nurse_user else None
        }

    # Badge/PIN specific lookup
    if payload.badge_id:
        user = db.query(HospitalUser).filter(HospitalUser.badge_id == payload.badge_id, HospitalUser.pin == payload.pin).first()
        if user:
            role = "admin" if user.role == "Hospital Administrator" else "nurse"
            return {"authenticated": True, "role": role, "user": user.to_dict()}

    raise HTTPException(status_code=401, detail="Invalid credential or PIN")
