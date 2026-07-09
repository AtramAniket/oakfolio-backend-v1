from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.api_router import api_v1_router


app = FastAPI(
	title=settings.app_name,
	debug=settings.debug,
)


@app.get("/")
async def root():
	return {
		"message": f"{settings.app_name} is running"
	}


@app.get("/health")
async def health():
	return {
		"status": "Healthy"
	}


app.include_router(
	api_v1_router,
	prefix=settings.api_v1_prefix,
)
