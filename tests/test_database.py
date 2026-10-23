from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_database
from app.db.session import SessionLocal
from app.db.models import HospitalUser, TriagePatient, KioskTerminal, AuditLog

client = TestClient(app)

def test_database_init_and_counts():
    init_database()
    db = SessionLocal()
    try:
        assert db.query(HospitalUser).count() == 30
        assert db.query(TriagePatient).count() == 30
        assert db.query(KioskTerminal).count() == 6
        assert db.query(AuditLog).count() >= 4
    finally:
        db.close()

def test_get_users_api():
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 30
    assert any(u["name"] == "Dr. Geoffrey Mutiso" for u in data)

def test_get_patients_api():
    response = client.get("/api/patients")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 30
    assert any(p["name"] == "Wanjiru Karanja" for p in data)

def test_get_terminals_api():
    response = client.get("/api/terminals")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6

def test_pin_authentication():
    # Admin PIN
    admin_res = client.post("/api/users/auth/pin", json={"pin": "9900"})
    assert admin_res.status_code == 200
    assert admin_res.json()["role"] == "admin"

    # Clinician PIN
    nurse_res = client.post("/api/users/auth/pin", json={"pin": "4821"})
    assert nurse_res.status_code == 200
    assert nurse_res.json()["role"] == "nurse"
