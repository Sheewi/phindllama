# app/api/endpoints.py
"""API endpoints with security and validation."""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models.model_manager import ModelLoader
from app.utils.rate_limiter import RateLimiter
from app.utils.error_handler import ErrorHandler

router = APIRouter()
model = ModelLoader("phind-codellama-34b-v2.Q4_K_M.gguf")
rate_limiter = RateLimiter(max_requests=100, time_window=timedelta(minutes=1))
error_handler = ErrorHandler()

@router.post("/generate")
async def generate_text(request: Request, prompt: str):
    """Generate text with rate limiting and error handling."""
    if not rate_limiter.check(request.client.host):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
    try:
        response = model.generate(prompt)
        return JSONResponse(content={"response": response}, media_type="application/json")
    except Exception as e:
        error_handler.handle_error(e)
        raise HTTPException(status_code=500, detail="Internal server error")
