from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import time
import logging
from app.config import settings
from app.models import InferenceRequest, InferenceResponse, Token, User
from app.auth import authenticate_user, create_access_token, get_current_user
from app.rate_limiter import rate_limiter
from app.llm_service import ollama_service
from app.metrics import metrics_tracker
from app.logging_config import setup_logging


# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="Secure LLM Inference Service",
    description="Fast and secure local LLM inference API with authentication and rate limiting",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Check Ollama service on startup"""
    logger.info("Starting Secure LLM Inference Service...")
    if not ollama_service.health_check():
        logger.warning("Ollama service not available. Please ensure Ollama is running.")
    else:
        logger.info(f"Ollama service connected. Model: {settings.OLLAMA_MODEL}")


@app.post("/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Generate JWT token for authentication"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"User {user.username} authenticated successfully")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post(f"/{settings.API_VERSION}/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest, current_user: User = Depends(get_current_user)):
    """Main inference endpoint with authentication and rate limiting"""
    
    # Check rate limit
    rate_limiter.check_rate_limit(current_user.username)
    
    # Track start time
    start_time = time.time()
    success = False
    response_text = ""
    
    try:
        # Generate response from LLM
        response_text = ollama_service.generate(request.prompt)
        success = True
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Record metrics
        metrics_tracker.record_request(latency_ms, success=True)
        
        # Structured logging
        log_extra = {
            "user_id": current_user.username,
            "prompt_length": len(request.prompt),
            "response_length": len(response_text),
            "latency_ms": round(latency_ms, 2),
            "status": "success"
        }
        logger.info("Inference completed successfully", extra=log_extra)
        
        return InferenceResponse(response=response_text)
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        metrics_tracker.record_request(latency_ms, success=False)
        
        log_extra = {
            "user_id": current_user.username,
            "prompt_length": len(request.prompt),
            "latency_ms": round(latency_ms, 2),
            "status": "error"
        }
        logger.error(f"Inference failed: {str(e)}", extra=log_extra)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference failed: {str(e)}"
        )


@app.get("/metrics")
async def get_metrics(current_user: User = Depends(get_current_user)):
    """Get performance metrics (requires authentication)"""
    return metrics_tracker.get_metrics()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    ollama_status = ollama_service.health_check()
    return {
        "status": "healthy" if ollama_status else "degraded",
        "ollama_service": "up" if ollama_status else "down",
        "model": settings.OLLAMA_MODEL
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Secure LLM Inference Service",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/token",
            "inference": f"/{settings.API_VERSION}/infer",
            "metrics": "/metrics",
            "health": "/health"
        }
    }