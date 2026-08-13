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
from fastapi import APIRouter, status
from app.api.v1.dependency import SessionDep
from app.modules.stocks.dependency import UserDep
import app.modules.stocks.service as stocks_service


api_v1_stocks_router = APIRouter(prefix="/stocks", tags=["Portfolios And Stock Holdings"])

# ***************************************************************************************************************************
# ************************************************PORTFOLIO ROUTES***********************************************************
# ***************************************************************************************************************************


@api_v1_stocks_router.get("/portfolios", response_model=GetAllPortfoliosResponse, status_code=status.HTTP_200_OK)
async def get_all_portfolios(
	db: SessionDep,
	current_user: UserDep):
	
	return await stocks_service.get_all_portfolios(
		db=db,
		current_user=current_user
	)


@api_v1_stocks_router.post("/portfolios", response_model=CreateNewPortfolioResponse, status_code=status.HTTP_201_CREATED)
async def create_new_portfolio(
	db: SessionDep,
	current_user: UserDep,
	payload: CreateNewPortfolioRequest):
	
	return await stocks_service.create_new_portfolio(
		db=db,
		payload=payload,
		current_user=current_user
	)


@api_v1_stocks_router.put("/portfolios/{portfolio_id}", response_model=CreateNewPortfolioResponse, status_code=status.HTTP_200_OK)
async def edit_portfolio(
	db: SessionDep,
	portfolio_id: UUID,
	current_user: UserDep,
	payload: CreateNewPortfolioRequest):
	
	return await stocks_service.edit_portfolio(
		db=db,
		payload=payload,
		current_user=current_user,
		portfolio_id=portfolio_id,
	)


@api_v1_stocks_router.delete("/portfolios/{portfolio_id}", response_model=DeletePortfolioResponse, status_code=status.HTTP_200_OK)
async def delete_portfolio(
	db: SessionDep,
	portfolio_id: UUID,
	current_user: UserDep):
	
	return await stocks_service.delete_portfolio(
		db=db,
		portfolio_id=portfolio_id,
		current_user=current_user
	)


# ***************************************************************************************************************************
# **************************************************PORTFOLIO ROUTES END*****************************************************
# ***************************************************************************************************************************





# ***************************************************************************************************************************
# ***************************************************HOLDINGS ROUTES*********************************************************
# ***************************************************************************************************************************


@api_v1_stocks_router.get("/portfolios/{portfolio_id}/holdings", response_model=GetHoldingsResponse, status_code=status.HTTP_200_OK)
async def get_holdings(
	db: SessionDep,
	portfolio_id: UUID,
	current_user: UserDep):
	
	return await stocks_service.get_all_stock_holdings(
		db=db,
		portfolio_id=portfolio_id,
		current_user=current_user,
	)


@api_v1_stocks_router.post("/portfolios/{portfolio_id}/holdings", response_model=AddStockResponse, status_code=status.HTTP_201_CREATED)
async def add_stock_to_portfolio(
	db: SessionDep,
	portfolio_id: UUID,
	current_user: UserDep,
	payload: AddStockRequest):
	
	return await stocks_service.add_stock_to_portfolio(
		db=db,
		payload=payload,
		portfolio_id=portfolio_id,
		current_user=current_user,
	)


# TODO: CREATE EDIT ROUTE FOR STOCK HOLDING
@api_v1_stocks_router.put("/portfolios/{portfolio_id}/holdings/{holding_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def update_stock_in_portfolio(
	db: SessionDep,
	holding_id: UUID,
	portfolio_id: UUID):
	
	return{
		"message":"No implemented yet!"
	}


@api_v1_stocks_router.delete("/portfolios/{portfolio_id}/holdings/{holding_id}", response_model=DeleteHoldingsResponse, status_code=status.HTTP_200_OK)
async def remove_stock_from_portfolio(
	db: SessionDep,
	holding_id: UUID,
	portfolio_id: UUID,
	current_user: UserDep):
	
	return await stocks_service.delete_stock_from_portfolio(
		db=db,
		holding_id=holding_id,
		portfolio_id=portfolio_id,
		current_user=current_user,
		)


# ***************************************************************************************************************************
# ***************************************************HOLDINGS ROUTES END*****************************************************
# ***************************************************************************************************************************