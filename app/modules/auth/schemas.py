from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
	email: EmailStr

	@field_validator("email", mode="before")
	@classmethod
	def normalize_email(cls, value):
		return value.strip().lower()

class RegisterResponse(BaseModel):
	message: str
	expires_in: int
	can_resend: bool

class DeleteRequest(BaseModel):
	email: EmailStr

class DeleteResponse(BaseModel):
	message: str

class VerifyUserRequest(BaseModel):
	token: str
	password: str = Field(
		min_length=8,
		max_length=128,
	)

class VerifyUserResponse(BaseModel):
	message: str