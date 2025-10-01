# app/security/sign.py
import base64, hashlib, hmac
from typing import Any

def _to_b64url(b: bytes) -> str:
    # base64url: +->-, /->_ ; '=' оставляем
    return base64.b64encode(b).decode().replace('+','-').replace('/','_')

def _make_string_to_hash(obj: Any) -> str:
    # Канонизация по правилам Aitu (см. "Проверка подписи")
    if isinstance(obj, list):
        return ''.join(_make_string_to_hash(x) for x in obj)
    if isinstance(obj, dict):
        parts = []
        for k in sorted(obj.keys()):
            if k == 'sign':
                continue
            v = obj[k]
            # отбрасываем пустые/ложные и пустые контейнеры
            if v in (0, None, False, ""): 
                continue
            if isinstance(v, (list, dict)) and len(v) == 0:
                continue
            parts.append(f"{k}:{_make_string_to_hash(v)}")
        return ''.join(parts)
    return str(obj)

def verify_aitu_sign(full_bridge_response_obj: dict, sign_b64url: str, secret_key: str) -> bool:
    canon = _make_string_to_hash(full_bridge_response_obj)
    digest = hmac.new(secret_key.encode('utf-8'),
                      canon.encode('utf-8'),
                      hashlib.sha256).digest()
    calc = _to_b64url(digest)
    return hmac.compare_digest(calc, sign_b64url)
