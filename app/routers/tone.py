from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.tone import ToneSignature
from app.schemas.tone import (
    ToneSignatureCreate,
    ToneSignatureResponse,
    GenerationRequest
)
from app.services.llm_service import ToneManager
from app.services.nlp_analysis import ToneAnalyzer
from PyPDF2 import PdfReader
from docx import Document
import io

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signatures", response_model=ToneSignatureResponse)
async def create_signature(request: ToneSignatureCreate, db: Session = Depends(get_db)):

    try:
        llm_data = ToneManager.create_signature(request.source_text)
        nlp_data = ToneAnalyzer.analyze_text(request.source_text)

        signature_data = {
            "id": llm_data["id"],
            "tone": llm_data["tone"],
            "language_style": llm_data["language_style"],
            "formality_level": llm_data["formality_level"],
            "formality_score": nlp_data["formality_score"],
            "address_style": llm_data["address_style"],
            "emotional_appeal": llm_data["emotional_appeal"],
            "sentiment_polarity": nlp_data["sentiment_polarity"],
            "sentiment_subjectivity": nlp_data["sentiment_subjectivity"],
            "avg_sentence_length": nlp_data["avg_sentence_length"],
            "passive_voice_ratio": nlp_data["passive_voice_ratio"],
            "source_text": request.source_text,
        }

        db_signature = ToneSignature(**signature_data)
        db.add(db_signature)
        db.commit()
        db.refresh(db_signature)

        return db_signature
    except Exception as e:
        raise HTTPException(500, f"Signature creation failed: {str(e)}")


@router.get("/signatures", response_model=list[ToneSignatureResponse])
async def get_all_signatures(db: Session = Depends(get_db)):
    return db.query(ToneSignature).all()


@router.post("/generate")
async def generate_text(request: GenerationRequest, db: Session = Depends(get_db)):
    # Get signature
    signature = db.query(ToneSignature).filter(ToneSignature.id == request.signature_id).first()

    if not signature:
        raise HTTPException(404, "Tone signature not found")

    try:
        generated_text = ToneManager.generate_text(signature.__dict__, request.user_prompt)
    except Exception as e:
        raise HTTPException(500, f"Generation failed: {str(e)}")

    return {"generated_text": generated_text}


def extract_text_from_file(content: bytes, mime_type: str) -> str:
    """
    Extract text from various file formats without textract
    """
    try:
        if mime_type == "text/plain":
            return content.decode("utf-8")

        elif mime_type == "application/pdf":
            pdf = PdfReader(io.BytesIO(content))
            return "\n".join([page.extract_text() for page in pdf.pages])

        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(io.BytesIO(content))
            return "\n".join([para.text for para in doc.paragraphs])

        else:
            raise ValueError("Unsupported file type")

    except Exception as e:
        raise ValueError(f"Text extraction error: {str(e)}")