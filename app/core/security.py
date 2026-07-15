import hashlib
import secrets

def generate_verification_token() -> str:
	""" Function generates tokens for user email verification """
	return secrets.token_urlsafe(32)

def hash_verification_token(token: str) -> str:
	""" Function hashes the token and returns encoded string """
	return hashlib.sha256(token.encode("utf-8")).hexdigest()