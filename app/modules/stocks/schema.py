from pydantic import BaseModel, Field, ConfigDict
from app.modules.stocks.models import Exchange
from datetime import datetime
from typing import Optional
from decimal import Decimal
from uuid import UUID



# *********************************************
# **************Holdings Schema****************
# *********************************************

class AddStockRequest(BaseModel):
	company_name: str
	ticker: str
	exchange: Exchange
	quantity: int = Field(gt=0)
	buy_price: Decimal = Field(gt=0)
	buy_date: datetime


class AddStockResponse(BaseModel):
	message: str
	id: UUID
	company_name: str
	ticker: str

class HoldingsResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	portfolio_id: UUID
	company_name: str
	exchange: Exchange
	ticker: str
	quantity: int = Field(gt=0)
	buy_price: Decimal = Field(gt=0)
	buy_date: datetime

class GetHoldingsResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	holdings: list[HoldingsResponse]


class DeleteHoldingsResponse(BaseModel):
	message: str



# *********************************************
# *************Portfolio Schema****************
# *********************************************

class CreateNewPortfolioRequest(BaseModel):
	name: str = Field(min_length=3)
	description: Optional[str] = None


class CreateNewPortfolioResponse(BaseModel):
	message: str
	id: UUID
	name: str
	description: Optional[str] = None


class PortfolioResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	
	id: UUID
	user_id: UUID
	name: str
	description: Optional[str] = None
	holdings: list[HoldingsResponse]


class GetAllPortfoliosResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	message: str
	portfolios: list[PortfolioResponse]


class DeletePortfolioResponse(BaseModel):
	message: str