from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers.tone import router as tone_router
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(tone_router, prefix="/api/tone")

@app.get("/")
async def root():
    return {"message": "Tone of Voice API - use /docs for docs"}

# Verify OpenAI key on startup
@app.on_event("startup")
async def startup():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set i .env")
