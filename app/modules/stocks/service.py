from app.modules.stocks.schema import (
	CreateNewPortfolioResponse,
	CreateNewPortfolioRequest,
	GetAllPortfoliosResponse,
	DeletePortfolioResponse,
	DeleteHoldingsResponse,
	GetHoldingsResponse,
	AddStockResponse,
	AddStockRequest,
)

from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.modules.auth.models import User
from fastapi import status, HTTPException
from app.api.v1.dependency import SessionDep
from app.modules.stocks.models import StockPortfolio, StockHolding

not_found_exception = HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail='Portfolio(s) not found',
)

stock_not_found_exception = HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail='Stock not found',
)

# *****************************************************************
# ***********************GET ALL PORTFOLIOS************************
# *****************************************************************

async def get_all_portfolios(db: SessionDep, current_user: User) -> GetAllPortfoliosResponse:

	statement = select(StockPortfolio).where(
		StockPortfolio.user_id == current_user.id
	)

	result = db.execute(statement)

	portfolios = result.scalars().all()

	if not portfolios:
		return GetAllPortfoliosResponse(
		portfolios=portfolios,
		message="No portfolio available. Please add one.",
	)

	return GetAllPortfoliosResponse(
		portfolios=portfolios,
		message="Data is available!",
	)

# *****************************************************************
# *********************CREATE NEW PORTFOLIO************************
# *****************************************************************

async def create_new_portfolio(payload: CreateNewPortfolioRequest, db:SessionDep, current_user: User) -> CreateNewPortfolioResponse:
	
	new_portfolio = StockPortfolio(
		name=payload.name,
		user_id = current_user.id,
		description=payload.description,
	)

	db.add(new_portfolio)

	db.commit()

	db.refresh(new_portfolio)

	return CreateNewPortfolioResponse(
		id=new_portfolio.id,
		name=new_portfolio.name,
		description=new_portfolio.description,
		message="Portfolio Created Successfully",
	)

# *****************************************************************
# ***************************EDIT PORTFOLIO************************
# *****************************************************************

async def edit_portfolio(portfolio_id: UUID, payload: CreateNewPortfolioRequest, db:SessionDep, current_user: User) -> CreateNewPortfolioResponse:
	
	statement = select(StockPortfolio).where(
		StockPortfolio.id == portfolio_id,
		StockPortfolio.user_id == current_user.id,
	)

	result = db.execute(statement)

	portfolio = result.scalar_one_or_none()

	if portfolio:
		
		updated_data = payload.model_dump(exclude_unset=True)

		for field, value in updated_data.items():
			setattr(portfolio, field, value)

		db.commit()

		db.refresh(portfolio)

		return CreateNewPortfolioResponse(
		id=portfolio.id,
		name=portfolio.name,
		description=portfolio.description,
		message="Portfolio Updated Successfully",
		)

	else:
		raise not_found_exception


# *****************************************************************
# ************************DELETE PORTFOLIO*************************
# *****************************************************************

async def delete_portfolio(portfolio_id: UUID, current_user: User, db: SessionDep) -> DeletePortfolioResponse:
	
	statement = select(StockPortfolio).where(
		StockPortfolio.id == portfolio_id,
		StockPortfolio.user_id == current_user.id,
	)

	result = db.execute(statement)

	portfolio = result.scalar_one_or_none()

	if portfolio:
		
		db.delete(portfolio)
		
		db.commit()


		return DeletePortfolioResponse(
			message="Portfolio deleted successfully"
		)

	else:
		raise not_found_exception


# *****************************************************************
# *************************GET ALL HOLDINGS************************
# *****************************************************************

async def get_all_stock_holdings(db: SessionDep, portfolio_id: UUID, current_user: User) -> GetHoldingsResponse:

	portfolio_statement = select(StockPortfolio).where(
		StockPortfolio.id == portfolio_id,
		StockPortfolio.user_id == current_user.id
	)

	portfolio_result = db.execute(portfolio_statement)

	portfolio = portfolio_result.scalar_one_or_none()

	if not portfolio:
		raise not_found_exception


	holdings_statement = select(StockHolding).where(
		StockHolding.portfolio_id == portfolio_id
	)

	holdings_result = db.execute(holdings_statement)

	holdings = holdings_result.scalars().all()

	return GetHoldingsResponse(
		holdings=holdings
	)


# *****************************************************************
# *******************ADD STOCK TO STOCK PORTFOLIO******************
# *****************************************************************
async def add_stock_to_portfolio(db: SessionDep, payload: AddStockRequest, portfolio_id: UUID, current_user: User) -> AddStockResponse:
	
	portfolio_statement = select(StockPortfolio).where(
		StockPortfolio.id == portfolio_id,
		StockPortfolio.user_id == current_user.id
	)

	portfolio_result = db.execute(portfolio_statement)

	portfolios = portfolio_result.scalar_one_or_none()

	if not portfolios:
		raise not_found_exception


	new_stock = StockHolding(
		ticker=payload.ticker,
		portfolio_id=portfolio_id,
		exchange=payload.exchange,
		quantity=payload.quantity,
		buy_date=payload.buy_date,
		buy_price=payload.buy_price,
		company_name=payload.company_name,
	)

	db.add(new_stock)

	db.commit()

	db.refresh(new_stock)

	return AddStockResponse(
		id=new_stock.id,
		ticker=new_stock.ticker,
		company_name=new_stock.company_name,
		message="New stock added successfully"
	)


# *****************************************************************
# *******************DELETE STOCK FROM PORTFOLIO*******************
# *****************************************************************

async def delete_stock_from_portfolio(db: SessionDep, holding_id: UUID, portfolio_id: UUID, current_user: User) -> DeleteHoldingsResponse:
	
	portfolio_statement = select(StockPortfolio).where(
		StockPortfolio.id == portfolio_id,
		StockPortfolio.user_id == current_user.id
	)

	portfolio_result = db.execute(portfolio_statement)

	portfolio = portfolio_result.scalar_one_or_none()

	if not portfolio:
		raise not_found_exception


	holding_statement = select(StockHolding).where(
		StockHolding.id == holding_id,
		StockHolding.portfolio_id == portfolio_id,
	)

	holding_result = db.execute(holding_statement)

	holding = holding_result.scalar_one_or_none()

	if holding:

		db.delete(holding)

		db.commit()

		return DeleteHoldingsResponse(
			message="Stock removed from portfolio"
		)

	else:
		raise stock_not_found_exception

