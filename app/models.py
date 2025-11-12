from pydantic import BaseModel, Field
from typing import Optional


class InferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000, description="Input prompt for LLM")


class InferenceResponse(BaseModel):
    response: str = Field(..., description="Generated response from LLM")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class User(BaseModel):
    username: str
    disabled: Optional[bool] = False