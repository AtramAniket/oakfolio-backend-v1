import hashlib
import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(
	schemes=["bcrypt"],
	deprecated="auto",
)

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