import hashlib
import secrets
from typing import Dict, Optional

_tokens: Dict[str, int] = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    _tokens[token] = user_id
    return token

def get_user_id(token: str) -> Optional[int]:
    return _tokens.get(token)
