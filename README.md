# ClearCaption Kiosk — Backend Speech-to-Text & Triage Service

Asynchronous Python FastAPI backend providing real-time speech-to-text streaming, dual-client WebSocket broadcasting (patient tablet & clinician station), visual symptom triage, and medical interpreter dispatch.

---

## 🏛️ Architecture Overview

```
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
   +---------------------------+           +---------------------------+
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+
- pip

### Local Setup

```bash
# 1. Clone the repository
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

# 4. Start backend server
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API Base:** `http://localhost:8000`
- **Swagger Documentation:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/api/health`

---

## 🐳 Docker Deployment

```bash
docker compose up --build
```

---

## 📡 API Endpoints

### Health & Monitoring
- `GET /api/health` — Audio pipeline latency metrics, speech model version, service health.

### Sessions & Transcripts
- `GET /api/sessions` — List active kiosk reception sessions.
- `POST /api/sessions` — Initialize a new intake session.
- `GET /api/sessions/{session_id}/transcript` — Retrieve timestamped conversation log.
- `POST /api/sessions/{session_id}/flag` — Flag/unflag statements for physician handoff.
- `POST /api/sessions/{session_id}/escalate` — Trigger emergency triage escalation & ASL interpreter request.

### Symptoms & ASL
- `GET /api/symptoms/catalog` — Get symptom cards with urgency levels & ASL video references.
- `POST /api/symptoms/select` — Log non-verbal patient symptom selection from tablet.

### Real-Time WebSocket
- `ws://localhost:8000/ws/captions/{session_id}?client_type=patient` — Live caption streaming for tablet.
- `ws://localhost:8000/ws/captions/{session_id}?client_type=clinician` — Clinician console synchronization.

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📄 License

MIT License. Designed for accessible healthcare reception systems.
