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
    REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "DATABASE_URL"]
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing environment variables in .env: {', '.join(missing)}")
