# Tone of Voice API
An AI-powered text analysis + generation system that preserves brand voice characteristics.

## Features
- Creates tone signature from sample texts + docs
- Generate text using stored Tone of voice
- Hybrid implementation NLP/LLM analysis (spaCy + OpenAI)
- File upload support (txt, pdf, docx - <2MB)
- Docker deployment support

## Prerequisites
- Python 3.12
- OpenAI API key
- Docker

## Installation
```bash
git clone https://github.com/quincykwende/tone-of-voice-api
cd tone-of-voice-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Create .env file:
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@db:5432/tone_db
```

### Running with Docker
```bash
  docker-compose down -v && docker-compose up --build
```

### Visit Docs at 
```
http://localhost:8000/docs
```
