import secrets
from typing import Dict, Optional
from passlib.context import CryptContext

_tokens: Dict[str, int] = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the password using bcrypt for security."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hashed value."""
    return pwd_context.verify(password, hashed)

def create_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    _tokens[token] = user_id
    return token

def get_user_id(token: str) -> Optional[int]:
    return _tokens.get(token)
