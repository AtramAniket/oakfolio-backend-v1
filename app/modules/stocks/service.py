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

import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.v1.dependency import SessionDep
from app.modules.auth.models import User
from fastapi import status, HTTPException
from app.modules.stocks.models import StockPortfolio, StockHolding


async def get_all_portfolios(db: SessionDep, current_user: User) -> GetAllPortfoliosResponse:

	statement = select(StockPortfolio).where(
		StockPortfolio.user_id == current_user.id
	)

	result = db.execute(statement).scalars().all()

	return GetAllPortfoliosResponse(
		message="Data is available!",
		portfolios=result,
	)


async def create_new_portfolio(payload: CreateNewPortfolioRequest, db:SessionDep, current_user: User) -> CreateNewPortfolioResponse:
	
	new_portfolio = StockPortfolio(
		user_id = current_user.id,
		name=payload.name,
		description=payload.description,
	)

	db.add(new_portfolio)

	db.commit()

	db.refresh(new_portfolio)

	return CreateNewPortfolioResponse(
		message="Portfolio Created Successfully",
		id=new_portfolio.id,
		name=new_portfolio.name,
		description=new_portfolio.description
	)
