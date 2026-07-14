from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
	email: EmailStr

	@field_validator("email", mode="before")
	@classmethod
	def normalize_email(cls, value):
		return value.strip().lower()
