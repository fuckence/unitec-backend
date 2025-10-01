# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas.auth import MeResponse
from app.security.jwt import JWT_SECRET, JWT_ALG
import jwt

router = APIRouter(prefix="/api", tags=["users"])

def get_current_user(token: str, db: Session) -> User:
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        sub = data.get("sub")
        if not sub:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.get(User, sub)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me", response_model=MeResponse)
def me(authorization: str, db: Session = Depends(get_db)):
    # ждём заголовок Authorization: Bearer <token>
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_current_user(parts[1], db)
    return MeResponse(
        aitu_user_id=user.aitu_user_id,
        first_name=user.first_name, last_name=user.last_name,
        username=user.username, phone=user.phone
    )
