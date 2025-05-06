from sqlalchemy import Column, String, Float, DateTime, Text
from datetime import datetime
from app.database import Base


class ToneSignature(Base):
    __tablename__ = "tone_signatures"

    id = Column(String, primary_key=True, index=True)
    tone = Column(String)
    language_style = Column(String)
    formality_level = Column(Float)  # btw 0.0 to 1.0
    formality_score = Column(Float)  # via NLP
    address_style = Column(String)
    emotional_appeal = Column(String)
    sentiment_polarity = Column(Float) # via NLP
    sentiment_subjectivity = Column(Float) # via NLP
    avg_sentence_length = Column(Float)  # via NLP
    passive_voice_ratio = Column(Float)  # via NLP
    source_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)