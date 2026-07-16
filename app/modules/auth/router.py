from app.modules.auth.schemas import (
	VerifyUserResponse,
	VerifyUserRequest,
	RegisterResponse,
	RegisterRequest,
	DeleteResponse,
	DeleteRequest,
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

@auth_router.post("/register", response_model=RegisterResponse)
async def register(payload: RegisterRequest,db: SessionDep):
	return await auth_service.register_user(db=db, payload=payload)

@auth_router.post("/delete_pending_registration", response_model=DeleteResponse)
async def delete_pending_user(payload: DeleteRequest,db: SessionDep):
	return await auth_service.delete_pending_registration(db=db, payload=payload)

@auth_router.post("/create_user", response_model=VerifyUserResponse)
async def create_user(payload: VerifyUserRequest, db:SessionDep):
	return await auth_service.verify_and_create_new_user(db=db, payload=payload)