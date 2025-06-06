from pydantic import BaseModel
from datetime import datetime

class ToneSignatureCreate(BaseModel):
    source_text: str

class ToneSignatureResponse(BaseModel):
    id: str
    tone: str
    language_style: str
    formality_level: float
    formality_score: float
    address_style: str
    emotional_appeal: str
    sentiment_polarity: float
    sentiment_subjectivity: float
    avg_sentence_length: float
    passive_voice_ratio: float
    source_text: str
    created_at: datetime

class GenerationRequest(BaseModel):
    signature_id: str
    user_prompt: str