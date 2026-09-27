from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "audio_pipeline" in data

def test_symptom_catalog():
    response = client.get("/api/symptoms/catalog")
    assert response.status_code == 200
    symptoms = response.json()
    assert len(symptoms) >= 8
    assert any(s["id"] == "chest-pain" for s in symptoms)

def test_session_lifecycle():
    # 1. Create session
    create_res = client.post("/api/sessions", json={
        "facility_name": "St. Mary's Medical Center",
        "department": "Emergency Intake"
    })
    assert create_res.status_code == 200
    session_id = create_res.json()["session_id"]
    assert session_id.startswith("kiosk-")

    # 2. Get transcript
    transcript_res = client.get(f"/api/sessions/{session_id}/transcript")
    assert transcript_res.status_code == 200
