import asyncio
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from app.auth import get_current_user
from app.llm_service import ollama_service
from app.models import InferenceRequest, User

router = APIRouter()

async def stream_generator(prompt: str):
    # Simulated token streaming (replace with proper Ollama streaming if available)
    response = ollama_service.generate(prompt)
    for token in response.split():
        yield token + " "
        await asyncio.sleep(0.1)

@router.post("/v1/infer/stream")
async def infer_stream(request: InferenceRequest, current_user: User = Depends(get_current_user)):
    return StreamingResponse(stream_generator(request.prompt), media_type="text/plain")
