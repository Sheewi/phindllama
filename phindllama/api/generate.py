# phindllama/api/generate.py
"""Text generation API endpoint."""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 100
    temperature: Optional[float] = 0.7
    model_name: Optional[str] = None

class GenerateResponse(BaseModel):
    generated_text: str
    model_used: str
    tokens_used: int

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(
    request: GenerateRequest,
    token: str = Depends(oauth2_scheme)
) -> GenerateResponse:
    """Generate text using the specified model."""
    try:
        # Placeholder for actual text generation logic
        # This would integrate with your model manager
        generated_text = f"Generated response for: {request.prompt}"
        
        return GenerateResponse(
            generated_text=generated_text,
            model_used=request.model_name or "default",
            tokens_used=len(generated_text.split())
        )
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise HTTPException(status_code=500, detail="Text generation failed")

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "text-generation"}
