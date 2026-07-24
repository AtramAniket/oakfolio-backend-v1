from uuid import UUID
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator

class VerifyRegistrationTokenRequest(BaseModel):
	verification_token: str

class VerifyRegistrationTokenResponse(BaseModel):
	status: Literal["invalid", "expired", "valid"]

class RegisterRequest(BaseModel):
	email: EmailStr

	@field_validator("email", mode="before")
	@classmethod
	def normalize_email(cls, value):
		return value.strip().lower()

class RegisterResponse(BaseModel):
	message: str
	expires_in: int | None = None
	can_resend: bool | None = None
	verification_token: str | None = None

class DeleteRequest(BaseModel):
	email: EmailStr

class DeleteResponse(BaseModel):
	message: str

class VerifyUserRequest(BaseModel):
	token: str
	password: str = Field(
		min_length=8,
		max_length=64,
	)

class VerifyUserResponse(BaseModel):
	message: str

class UserRequest(BaseModel):
	access_token: str

class UserResponse(BaseModel):
	id: UUID
	email: str
	username: str
	verified_at: datetime

class LoginRequest(BaseModel):
	password: str
	email: EmailStr

class LoginResponse(BaseModel):
	token_type: str | None = None
	access_token: str | None = None
	user: UserResponse | None = None