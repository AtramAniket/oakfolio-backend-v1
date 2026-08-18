import hashlib
import secrets
from jose import jwt
from typing import Any
from uuid import UUID, uuid4
from app.core.config import settings
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta


pwd_context = CryptContext(
	schemes=["bcrypt"],
	deprecated="auto",
)


def create_access_token(user_id: UUID) -> tuple[str, UUID, datetime]:
    now = datetime.now(timezone.utc)

    token_expires_at = (
        now + timedelta(
            minutes=int(settings.access_token_expire_minutes)
        )
    )

    jti = uuid4()

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "jti": str(jti),
        "exp": token_expires_at,
        "iat": now,
    }

    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    return token, jti, token_expires_at


def decode_access_token(token: str) -> dict[str, Any]:
	"""Function returns user's id if the token is valid"""
	payload = jwt.decode(
		token,
		settings.secret_key,
		algorithms=settings.algorithm,
	)

	return payload
	

def generate_verification_token() -> str:
	""" Function generates tokens for user email verification """
	return secrets.token_urlsafe(32)

def hash_verification_token(token: str) -> str:
	""" Function hashes the token and returns encoded string """
	return hashlib.sha256(token.encode("utf-8")).hexdigest()

def hash_password(password: str) -> str:
	return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)

def generate_verification_link(token: str) -> str:
	return f"{settings.frontend_url}/verify?token={token}"