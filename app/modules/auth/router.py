from app.modules.auth.schemas import RegisterRequest
from app.api.v1.dependency import SessionDep
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/test")
async def auth_test():
	return {
		"message":"Authentication router working"
	}

@auth_router.post("/register")
async def register(payload: RegisterRequest,db: SessionDep):
	pass
