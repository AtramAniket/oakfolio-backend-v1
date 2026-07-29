from app.modules.auth.schemas import (
	VerifyRegistrationTokenResponse,
	VerifyRegistrationTokenRequest,
	VerifyUserResponse,
	VerifyUserRequest,
	RegisterResponse,
	RegisterRequest,
	DeleteResponse,
	DeleteRequest,
	LoginResponse,
	LoginRequest,
	UserResponse,
	UserRequest,
)
from app.core.security import (
	generate_verification_token,
	hash_verification_token,
	create_access_token,
	decode_access_token,
	verify_password,
	hash_password,
)
from app.modules.auth.models import PendingRegistration, User
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from app.api.v1.dependency import SessionDep
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from uuid import UUID


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def login(db:Session, payload:LoginRequest) -> LoginResponse:
	
	# FInd user by email
	find_user_statement = select(User).where(
		User.email == payload.email
	)

	result = db.execute(find_user_statement)

	user = result.scalar_one_or_none()

	# If user is not present
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Invalid email or password'
		)
	
	# If password verification failed
	password_match = verify_password(payload.password, user.password_hash)
	if not password_match:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Invalid email or password'
		)
	
	# Generate JWT token
	jwt_token = create_access_token(user.id)
	return LoginResponse(
		token_type="bearer",
		access_token=jwt_token,
		user=UserResponse(
			id = user.id,
			email = user.email,
			username = user.username,
			verified_at = user.verified_at,
		)
	)


async def get_current_user(db:SessionDep, token: str = Depends(oauth2_scheme)) -> UserResponse:
	token_timeout_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Access token expired. Please generate new access token',
		headers={"WWW-Authenticate": "Bearer"},
	)
	
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={"WWW-Authenticate": "Bearer"},
	)

	user_not_found_exception = HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail='User not found',
	)

	try:
		jwt_payload = decode_access_token(token)
		 
		current_user_id = UUID(jwt_payload.get("sub"))
		 
		if current_user_id is None:
			raise credentials_exception
	
	except ExpiredSignatureError:
		raise token_timeout_exception

	except JWTError:
		raise credentials_exception

	current_user_statement = select(User).where(
		User.id == current_user_id)

	result = db.execute(current_user_statement).scalar_one_or_none()

	if result is None:
		raise user_not_found_exception

	return UserResponse(
		id=result.id,
		email=result.email,
		username=result.username,
		verified_at=result.verified_at,
	)


async def verify_user_registration_token(db:Session, payload:VerifyRegistrationTokenRequest) -> VerifyRegistrationTokenResponse:

	hashed_token = hash_verification_token(payload.verification_token)
	
	# Get the user from pending registrations table
	statement = select(PendingRegistration).where(
		PendingRegistration.token == hashed_token
	)
	
	result = db.execute(statement)

	pending_registration = result.scalar_one_or_none()


	# Check if token is valid
	if(not pending_registration):
		return VerifyRegistrationTokenResponse(
			status="invalid",
		)

	# Check if token has expired
	if datetime.now(timezone.utc) > pending_registration.expires_at:
		return VerifyRegistrationTokenResponse(
			status="expired",
		)
	else:
		return VerifyRegistrationTokenResponse(
			status="valid",
		)



async def register_user(db:Session, payload:RegisterRequest) -> RegisterResponse:
	
	# Check if user already registered
	existing_user_statement = select(User).where(
		User.email == payload.email)

	existing_user_result = db.execute(existing_user_statement)

	existing_user = existing_user_result.scalar_one_or_none()

	if existing_user:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail='An account already exists with this email.'
		)
		
	# Get the user from pending registrations table
	statement = select(PendingRegistration).where(
		PendingRegistration.email == payload.email
	)
	
	result = db.execute(statement)

	pending_registration = result.scalar_one_or_none()

	# Existing pending registration found
	if pending_registration:

		# If token is still valid
		if pending_registration.expires_at > datetime.now(timezone.utc):
			remaining_seconds = int((pending_registration.expires_at - datetime.now(timezone.utc)).total_seconds())

			return RegisterResponse(
				message="Verification email already sent",
				expires_in=remaining_seconds,
				can_resend=False,
			)
		# If token expired
		expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
		
		token = generate_verification_token()
		hashed_token = hash_verification_token(token)
		
		pending_registration.expires_at = expires_at
		pending_registration.token = hashed_token
		
		db.commit()
		
		db.refresh(pending_registration)
		
		return RegisterResponse(
			message="Previous verification expired. A new verification email will be sent.",
			verification_token=token,
			can_resend=True,
			expires_in=300,
		)

	# No pending registration exists
	expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
	
	token = generate_verification_token()
	hashed_token = hash_verification_token(token)

	new_pending_registration = PendingRegistration(
		expires_at=expires_at,
		email=payload.email,
		token=hashed_token,
	)

	db.add(new_pending_registration)

	db.commit()

	db.refresh(new_pending_registration)

	return RegisterResponse(
		message="Verification email sent successfully",
		verification_token=token,
		can_resend=False,
		expires_in=300,
	)




async def delete_pending_registration(db:Session, payload:DeleteRequest) -> DeleteResponse:
	statement = select(PendingRegistration).where(
		PendingRegistration.email == payload.email
	)
	
	result = db.execute(statement)

	pending_registration = result.scalar_one_or_none()

	# If email is present
	if pending_registration:

		db.delete(pending_registration)

		db.commit()

		return DeleteResponse(
			message=f"User with email {payload.email} deleted successfully from pending registrations"
		)
	# If email is not present
	return DeleteResponse(
		message=f"No user with email {payload.email} found in pending registrations"
	)




async def verify_and_create_new_user(db:Session, payload:VerifyUserRequest) -> VerifyUserResponse:
	
	# Hash incoming raw token
	hashed_token = hash_verification_token(payload.token)

	# Hash plain text password
	hashed_password = hash_password(payload.password)

	# Find user in pending registrations
	statement = select(PendingRegistration).where(
		PendingRegistration.token == hashed_token)

	result = db.execute(statement)

	pending_registration = result.scalar_one_or_none()

	# Check if token is valid
	if not pending_registration:
		return VerifyUserResponse(
				message="Invalid token."
		)

	# Check if token is expired
	if datetime.now(timezone.utc) > pending_registration.expires_at:
		return VerifyUserResponse(
			message="Verification token expired."
		)

	# Create new user
	new_user = User(
		username=pending_registration.email,
		email=pending_registration.email,
		password_hash=hashed_password,
	)

	db.add(new_user)

	# Remove pending registration for user
	db.delete(pending_registration)

	# Add new user and commit to user table while removing from pending transaction
	db.commit()

	return VerifyUserResponse(
		message="User created successfully."
	)