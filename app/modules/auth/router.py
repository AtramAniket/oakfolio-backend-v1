from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/test")
async def auth_test():
	return {
		"message":"Authentication router working"
	}