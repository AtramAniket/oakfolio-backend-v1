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
	avatar_id: str
	verified_at: datetime
	notifications_enabled: bool

class LoginRequest(BaseModel):
	password: str
	email: EmailStr

class LoginResponse(BaseModel):
	token_type: str | None = None
	access_token: str | None = None

class UpdateUserRequest(BaseModel):
	username: str | None = None
	avatar_id: str | None = None
	notifications_enabled: bool | None = None

	@field_validator("username")
	@classmethod
	def validate_username(cls, value):
		value = value.strip()

		if not value:
			raise ValueError("Username cannot be empty")

		if(len(value) < 3):
			raise ValueError("Username must be atleast 3 characters")

		if(len(value) > 50):
			raise ValueError("Username must not exceed 50 characters")

		return value

	@field_validator("avatar_id")
	def validate_avatar_id(cls, value):

		valid_avatar_ids = [
			"avatar_01",
			"avatar_02",
			"avatar_03",
			"avatar_04",
			"avatar_05",
			"avatar_06",
			"avatar_07",
			"avatar_08",
		]

		if value not in valid_avatar_ids:
			raise ValueError("Invalid Avatar ID")

		return value

class UpdateUserResponse(BaseModel):
	message: str