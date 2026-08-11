from app.modules.stocks.schema import (
	AddStockRequest,
	AddStockResponse,
	HoldingsResponse,
	PortfolioResponse,
	GetHoldingsResponse,
	DeleteHoldingsResponse,
	DeletePortfolioResponse,
	GetAllPortfoliosResponse,
	CreateNewPortfolioRequest,
	CreateNewPortfolioResponse,
)

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.v1.dependency import SessionDep
from fastapi import APIRouter, Depends, status
import app.modules.stocks.service as stocks_service
from app.modules.auth.models import User
import app.modules.auth.services as auth_service


api_v1_stocks_router = APIRouter(prefix="/stocks", tags=["Stocks"])

@api_v1_stocks_router.get("/portfolios", status_code=status.HTTP_200_OK)
async def get_all_portfolios( db: SessionDep, current_user: User = Depends(auth_service.get_current_user)):
	return await stocks_service.get_all_portfolios(db=db, current_user=current_user)


@api_v1_stocks_router.post("/portfolios", response_model=CreateNewPortfolioResponse, status_code=status.HTTP_201_CREATED)
async def create_new_portfolio(
	db: SessionDep,
	payload: CreateNewPortfolioRequest,
	current_user: User = Depends(auth_service.get_current_user)):
	
	return await stocks_service.create_new_portfolio(
		db=db,
		payload=payload,
		current_user=current_user
	)


@api_v1_stocks_router.delete("/portfolios/{portfolio_id}", response_model=DeleteHoldingsResponse)
def delete_portfolio(portfolio_id: UUID, db:SessionDep):
	pass
