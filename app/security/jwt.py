# app/security/jwt.py
import os, jwt
from datetime import datetime, timedelta, timezone

JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
JWT_ALG = "HS256"
ACCESS_TTL_MIN = int(os.getenv("ACCESS_TOKEN_TTL_MIN", "1440"))  # 24h

def issue_access_token(subject: str) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=ACCESS_TTL_MIN)
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp()), "iss": "aitu-miniapp"}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG), ACCESS_TTL_MIN * 60
