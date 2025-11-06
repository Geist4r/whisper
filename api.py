"""
Whisper API Server for Railway Deployment
Supports transcription from URLs
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import whisper
import os
from typing import Optional, List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Whisper Transcription API",
    description="Speech-to-text transcription service using OpenAI's Whisper",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
MODEL_NAME = os.getenv("WHISPER_MODEL", "base")  # Default to 'base' for faster loading
logger.info(f"Loading Whisper model: {MODEL_NAME}")
model = whisper.load_model(MODEL_NAME)
logger.info(f"Model {MODEL_NAME} loaded successfully")


class TranscribeRequest(BaseModel):
    """Request model for transcription"""
    url: HttpUrl
    language: Optional[str] = None
    task: str = "transcribe"  # "transcribe" or "translate"
    word_timestamps: bool = False
    temperature: float = 0.0


class TranscribeResponse(BaseModel):
    """Response model for transcription"""
    text: str
    language: str
    segments: List[Dict[str, Any]]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Whisper API is running",
        "model": MODEL_NAME,
        "endpoints": {
            "transcribe": "/transcribe (POST)",
            "health": "/health (GET)",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    """Health check for Railway"""
    return {"status": "healthy", "model": MODEL_NAME}


@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(request: TranscribeRequest):
    """
    Transcribe audio from a URL
    
    Parameters:
    - url: Direct URL to audio file (mp3, wav, m4a, flac, ogg, etc.)
    - language: Optional language code (e.g., "en", "de", "fr")
    - task: "transcribe" or "translate" (translate converts to English)
    - word_timestamps: Extract word-level timestamps
    - temperature: Sampling temperature (0.0 = deterministic)
    
    Returns:
    - text: Full transcribed text
    - language: Detected or specified language
    - segments: List of segments with timestamps and text
    """
    try:
        logger.info(f"Transcribing audio from URL: {request.url}")
        
        # Prepare options
        options = {
            "task": request.task,
            "word_timestamps": request.word_timestamps,
            "temperature": request.temperature,
        }
        
        if request.language:
            options["language"] = request.language
        
        # Transcribe (URL is handled automatically by our modified whisper)
        result = model.transcribe(str(request.url), **options)
        
        logger.info(f"Transcription completed. Language: {result['language']}")
        
        return TranscribeResponse(
            text=result["text"],
            language=result["language"],
            segments=result["segments"]
        )
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
