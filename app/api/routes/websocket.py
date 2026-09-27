import json
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.session_manager import session_manager

router = APIRouter(tags=["WebSocket Real-Time Captions"])

@router.websocket("/ws/captions/{session_id}")
async def websocket_caption_stream(websocket: WebSocket, session_id: str, client_type: str = "patient"):
    await websocket.accept()
    session = session_manager.get_session(session_id)
    if not session:
        session = session_manager.create_session("St. Mary's Medical Center", "Reception")

    if client_type == "patient":
        session.patient_sockets.add(websocket)
    else:
        session.clinician_sockets.add(websocket)

    try:
        # Send initial confirmation
        await websocket.send_json({
            "type": "connection_established",
            "session_id": session_id,
            "client_type": client_type,
            "timestamp": datetime.now().strftime("%H:%M")
        })

        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # Broadcast caption updates to all connected tablet and staff clients
            action = payload.get("action")
            if action == "speech_delta":
                broadcast_data = {
                    "type": "caption_delta",
                    "text": payload.get("text"),
                    "speaker": payload.get("speaker", "clinician"),
                    "timestamp": datetime.now().strftime("%H:%M")
                }
                for s in session.patient_sockets | session.clinician_sockets:
                    await s.send_json(broadcast_data)

            elif action == "speech_finalized":
                entry = session.add_transcript(
                    speaker=payload.get("speaker", "clinician"),
                    text=payload.get("text", "")
                )
                broadcast_data = {
                    "type": "caption_final",
                    "entry_id": entry.id,
                    "text": entry.text,
                    "speaker": entry.speaker,
                    "timestamp": entry.timestamp
                }
                for s in session.patient_sockets | session.clinician_sockets:
                    await s.send_json(broadcast_data)

    except WebSocketDisconnect:
        if client_type == "patient":
            session.patient_sockets.discard(websocket)
        else:
            session.clinician_sockets.discard(websocket)
