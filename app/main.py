from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.api_router import api_v1_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
	title=settings.app_name,
	debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://oakfolio-app.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
