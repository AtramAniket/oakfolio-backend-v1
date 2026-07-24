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
import app.modules.auth.services as auth_service 
from app.api.v1.dependency import SessionDep
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/test")
async def auth_test():
	return {
		"message":"Authentication router working"
	}



@auth_router.post("/verify-registration-token", response_model=VerifyRegistrationTokenResponse)
async def verify_registration_token(payload: VerifyRegistrationTokenRequest, db: SessionDep):
	return await auth_service.verify_user_registration_token(db=db, payload=payload)


@auth_router.post("/delete_pending_registration", response_model=DeleteResponse)
async def delete_pending_user(payload: DeleteRequest,db: SessionDep):
	return await auth_service.delete_pending_registration(db=db, payload=payload)


@auth_router.post("/create_user", response_model=VerifyUserResponse)
async def create_user(payload: VerifyUserRequest, db:SessionDep):
	return await auth_service.verify_and_create_new_user(db=db, payload=payload)


@auth_router.post("/register", response_model=RegisterResponse)
async def register(payload: RegisterRequest,db: SessionDep):
	return await auth_service.register_user(db=db, payload=payload)

@auth_router.post("/me", response_model=UserResponse)
async def current_user(payload: UserRequest, db:SessionDep):
	return await auth_service.get_current_user(db=db, payload=payload)

@auth_router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db:SessionDep):
	return await auth_service.login(db=db, payload=payload)
