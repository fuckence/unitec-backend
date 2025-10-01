# app/schemas/auth.py
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class SignedChunk(BaseModel):
    sign: str = Field(..., description="Подпись base64url из Bridge")
    data: Dict[str, Any] = Field(..., description="Сырой ответ Bridge (включая все нужные поля)")

class AuthRequest(BaseModel):
    me: SignedChunk
    phone: Optional[SignedChunk] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class MeResponse(BaseModel):
    aitu_user_id: str
    first_name: Optional[str] = None
    last_name:  Optional[str] = None
    username:   Optional[str] = None
    phone:      Optional[str] = None
