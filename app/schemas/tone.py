# app/schemas/tone.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ToneSignatureCreate(BaseModel):
    source_text: str

class ToneSignatureResponse(BaseModel):
    id: str
    tone: str
    language_style: str
    formality_level: float
    address_style: str
    emotional_appeal: str
    source_text: str
    created_at: datetime

class GenerationRequest(BaseModel):
    signature_id: str
    user_prompt: str