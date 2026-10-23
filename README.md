# ClearCaption Kiosk — Backend Speech-to-Text, PostgreSQL & Triage Service

Asynchronous Python FastAPI backend providing real-time speech-to-text streaming, dual-client WebSocket broadcasting (patient tablet & clinician station), PostgreSQL database persistence (SQLAlchemy 2.0 ORM), visual symptom triage, and medical interpreter dispatch.

---

## 🏛️ Architecture Overview

`
                      +-----------------------------+
                      | Reception Microphone Stream |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |   WebSocket Audio Ingestion |
                      |    (/ws/captions/{id})      |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      | Speech Recognition Pipeline |
                      |   (Sub-300ms Transcription) |
                      +--------------+--------------+
                                     |
                 +-------------------+-------------------+
                 |                                       |
                 v                                       v
   +---------------------------+           +---------------------------+
   |  Patient Tablet Display   |           | Clinician Triage Console  |
   | (Live High-Contrast Text) |           |  (Log & Statement Flags)  |
   +-------------+-------------+           +-------------+-------------+
                 |                                       |
                 +-------------------+-------------------+
                                     |
                                     v
                      +-----------------------------+
                      |   PostgreSQL 16 Database    |
                      | (30 Staff, 30 Patients, DPA)|
                      +-----------------------------+
`

---

## 🗄️ PostgreSQL Database Integration

The backend is backed by **PostgreSQL 16** via SQLAlchemy 2.0 ORM and psycopg2-binary, featuring auto-initialization and seeding on startup:

- **hospital_users table**: 30 hospital system staff members spanning Hospital Administrators, Triage Nurses, Reception Officers, Medical Doctors, KSL Interpreters, and Audiology Specialists.
- **	riage_patients table**: 30 patient triage intake records with Swahili/English translations, affected body locations, duration, priority triage flags, and desk assignments.
- **kiosk_terminals table**: 6 kiosk fleet hardware terminals (Desks 1–6) tracking latency and availability.
- **udit_logs table**: DPA-compliant ephemeral wipe verifications, KSL assistance logs, and administrative access audits.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+
- PostgreSQL 16 (or Docker)

### Docker Deployment (Recommended)

Spins up both PostgreSQL and the FastAPI application with auto-seeding:

`ash
docker compose up --build
`

- **Backend API:** http://localhost:8000
- **Interactive Swagger Docs:** http://localhost:8000/docs
- **Database:** localhost:5432 (clearcaption_db)

### Local Setup without Docker

`ash
# 1. Clone repository
git clone https://github.com/ncollo/speech-kiosk-backend.git
cd speech-kiosk-backend

# 2. Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run backend (PostgreSQL with automatic SQLite fallback for local test flexibility)
uvicorn app.main:app --reload --port 8000
`

---

## 📡 API Endpoints

### Health & Database Status
- GET /api/health — Audio pipeline latency metrics, speech model version, PostgreSQL engine status.

### Hospital Users & Staff Directory (PostgreSQL)
- GET /api/users — List hospital staff (supports filters: ole, status, search).
- GET /api/users/{user_id} — Get single staff profile.
- POST /api/users — Register a new staff member.
- PATCH /api/users/{user_id}/status — Update duty status (Active, On-Duty, Break, Offline).
- POST /api/users/auth/pin — Authenticate staff via PIN (Clinician PIN: 4821, Admin PIN: 9900).

### Patient Triage Queue (PostgreSQL)
- GET /api/patients — List triage queue (supports filters: desk, status, urgent, search).
- GET /api/patients/{patient_id} — Get patient intake details.
- POST /api/patients — Submit patient kiosk intake form.
- PATCH /api/patients/{patient_id}/status — Advance patient workflow (Waiting -> In Triage -> With Doctor -> Completed).

### Kiosk Terminals Fleet (PostgreSQL)
- GET /api/terminals — Status, hardware type, and latency metrics across Desks 1–6.
- POST /api/terminals/{terminal_id}/ping — Terminal ping heartbeat.

### DPA Compliance & Audit Trail (PostgreSQL)
- GET /api/audit/logs — Ephemeral wipe and compliance audit logs.
- POST /api/audit/logs — Record new audit event.

### Real-Time WebSocket Captioning
- ws://localhost:8000/ws/captions/{session_id}?client_type=patient — Patient live captions stream.
- ws://localhost:8000/ws/captions/{session_id}?client_type=clinician — Clinician station sync.

---

## 🧪 Running Tests

`ash
pytest tests/
`

---

## 📄 License

MIT License. Designed for accessible healthcare reception systems.
