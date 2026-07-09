from fastapi import APIRouter

from app.modules.auth.router import auth_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)