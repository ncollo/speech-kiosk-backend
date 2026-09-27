import uuid
from datetime import datetime
from typing import Dict, Any
from app.models.schemas import TriageEscalationRequest, TriageAlertResponse, TriageUrgency

HIGH_PRIORITY_SYMPTOMS = {"chest-pain", "shortness-of-breath", "headache"}

class TriageEvaluator:
    """
    Evaluates clinical urgency and dispatches on-site healthcare resources.
    """

    @staticmethod
    def evaluate_urgency(symptom_id: str) -> TriageUrgency:
        if symptom_id in HIGH_PRIORITY_SYMPTOMS:
            return "emergency"
        return "routine"

    @staticmethod
    def create_escalation(request: TriageEscalationRequest) -> TriageAlertResponse:
        alert_id = f"TRG-{str(uuid.uuid4())[:6].upper()}"
        return TriageAlertResponse(
            alert_id=alert_id,
            session_id=request.session_id,
            status="dispatched",
            urgency=request.urgency,
            interpreter_dispatched=request.request_interpreter,
            timestamp=datetime.utcnow()
        )

triage_service = TriageEvaluator()
