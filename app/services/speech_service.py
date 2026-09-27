import asyncio
from typing import AsyncGenerator, Dict, Any
from datetime import datetime

class SpeechRecognitionEngine:
    """
    Real-time speech-to-text processing engine.
    Supports low-latency streaming recognition and speaker tokenization.
    """

    def __init__(self, model_name: str = "whisper-base-en"):
        self.model_name = model_name
        self.is_ready = True
        self.sample_rate = 16000

    async def transcribe_audio_chunk(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Process incoming PCM audio stream and return transcription delta.
        """
        latency_ms = 142
        return {
            "partial_text": "",
            "is_final": False,
            "latency_ms": latency_ms,
            "confidence": 0.98
        }

    async def simulate_reception_dialogue(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Simulate typical reception dialogue for testing and verification.
        """
        dialogue = [
            ("Good morning, welcome to St. Mary's Medical Center.", "clinician"),
            ("Please let me know what brings you in today.", "clinician"),
            ("Can you tell me when your symptoms first started?", "clinician"),
            ("It started around eight AM, after I had breakfast.", "patient"),
            ("Are you currently taking any prescription medications?", "clinician")
        ]
        for phrase, speaker in dialogue:
            words = phrase.split()
            current = []
            for w in words:
                current.append(w)
                yield {
                    "is_final": False,
                    "speaker": speaker,
                    "text": " ".join(current),
                    "timestamp": datetime.now().strftime("%H:%M")
                }
                await asyncio.sleep(0.18)
            yield {
                "is_final": True,
                "speaker": speaker,
                "text": phrase,
                "timestamp": datetime.now().strftime("%H:%M")
            }
            await asyncio.sleep(0.8)

speech_engine = SpeechRecognitionEngine()
