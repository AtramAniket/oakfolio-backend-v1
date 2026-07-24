import hashlib
import secrets
from jose import jwt
from uuid import UUID
from app.core.config import settings
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

pwd_context = CryptContext(
	schemes=["bcrypt"],
	deprecated="auto",
)

def create_access_token(user_id: UUID) -> str:
	"""Function generates JWT access token for user id"""
	token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=int(settings.access_token_expire_minutes))

	payload: dict[str, Any] = {
		"sub": str(user_id),
		"exp": token_expires_at,
		"iat": datetime.now(timezone.utc)
	}

	return jwt.encode(
		payload,
		settings.secret_key,
		algorithm=settings.algorithm,
	)

def decode_access_token() -> str:
	pass

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