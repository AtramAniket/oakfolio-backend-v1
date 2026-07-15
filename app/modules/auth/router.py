from app.modules.auth.schemas import RegisterRequest, RegisterResponse
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
