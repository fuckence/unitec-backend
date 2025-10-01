# app/routers/auth.py
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas.auth import AuthRequest, TokenResponse
from app.security.sign import verify_aitu_sign
from app.security.jwt import issue_access_token
from datetime import datetime, timezone

AITU_API_SECRET = os.getenv("AITU_API_SECRET", "")

router = APIRouter(prefix="/api/aitu", tags=["auth"])

@router.post("/auth", response_model=TokenResponse, summary="Идентификация через getMe/getPhone")
def aitu_auth(payload: AuthRequest, db: Session = Depends(get_db)):
    # 1) Проверяем подпись getMe
    if not verify_aitu_sign(payload.me.data, payload.me.sign, AITU_API_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature for getMe")

    # 2) Проверяем (если прислали) getPhone
    phone_number = None
    if payload.phone:
        if not verify_aitu_sign(payload.phone.data, payload.phone.sign, AITU_API_SECRET):
            raise HTTPException(status_code=401, detail="Invalid signature for getPhone")
        phone_number = (
            payload.phone.data.get("phone")
            or payload.phone.data.get("phone_number")
            or payload.phone.data.get("msisdn")
        )

    # 3) Достаём базовые поля из getMe
    me = payload.me.data
    aitu_user_id = str(me.get("id") or me.get("user_id") or me.get("aitu_id") or me.get("userId") or me.get("uid"))
    if not aitu_user_id or aitu_user_id == "None":
        raise HTTPException(status_code=400, detail="Cannot determine aitu_user_id")

    first_name = me.get("name") or me.get("first_name") or me.get("firstName")
    last_name  = me.get("lastname") or me.get("last_name") or me.get("lastName")
    username   = me.get("username") or me.get("nick")

    # 4) Upsert пользователя
    user = db.get(User, aitu_user_id)
    if user:
        user.first_name = first_name or user.first_name
        user.last_name  = last_name  or user.last_name
        user.username   = username   or user.username
        user.phone      = phone_number or user.phone
        user.updated_at = datetime.now(timezone.utc)
    else:
        user = User(aitu_user_id=aitu_user_id, first_name=first_name, last_name=last_name,
                    username=username, phone=phone_number, updated_at=datetime.now(timezone.utc))
        db.add(user)
    db.commit()

    # 5) Выдаём JWT
    token, ttl = issue_access_token(aitu_user_id)
    return TokenResponse(access_token=token, expires_in=ttl)
