from sqlalchemy import String, Integer, Text, DateTime, func, UniqueConstraint, Enum, Numeric, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID as SQLAlchemyUUID
from enum import Enum as PythonEnum
from typing import TYPE_CHECKING
from datetime import datetime
from app.db.base import Base
from uuid import UUID, uuid4
from typing import Optional
from decimal import Decimal


# Avoid circular imports
if TYPE_CHECKING:
	from app.modules.auth.models import User

class Exchange(PythonEnum):
	NSE="NSE"
	BSE="BSE"


# ****************************************************
# ************* Stocks Portfolio Table ***************
# ****************************************************

class StockPortfolio(Base):

	__tablename__ = "stocks_portfolio"

	__table_args__ = (
		UniqueConstraint("user_id", "name", name="uniq_user_name"),
	)

	id: Mapped[UUID] = mapped_column(
		SQLAlchemyUUID(as_uuid=True),
		primary_key=True,
		default=uuid4,
	)

	# Foreign Key
	user_id: Mapped[UUID] = mapped_column(
		ForeignKey("users.id",ondelete="CASCADE"),
		nullable=False,
		index=True,
	)

	# relationship with user
	user: Mapped["User"] = relationship(
		"User",
		back_populates="stock_portfolios",
	)

	# One-To-Many relationship with holdings
	holdings: Mapped[list["StockHolding"]] = relationship(
		"StockHolding",
		back_populates="portfolio",
		cascade="all, delete-orphan",
		order_by="asc(StockHolding.ticker)",
	)

	name: Mapped[str] = mapped_column(
		String(100),
		nullable=False,
	)

	description: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True,
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		nullable=False,
	)

	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		onupdate=func.now(),
		nullable=False,
	)

# ****************************************************
# ************** Stocks Holdings Table ***************
# ****************************************************

class StockHolding(Base):

	__tablename__ = "stocks_holdings"

	__table_args__ = (
		UniqueConstraint("portfolio_id", "ticker", "exchange", name="uq_stock_holding_portfolio_ticker_exchange"),
	)

	id: Mapped[UUID] = mapped_column(
		SQLAlchemyUUID(as_uuid=True),
		primary_key=True,
		default=uuid4,
	)

	# Foreign Key
	portfolio_id: Mapped[UUID] = mapped_column(
		ForeignKey("stocks_portfolio.id",ondelete="CASCADE"),
		nullable=False,
		index=True,
	)

	# Relationship with portfolio
	portfolio: Mapped["StockPortfolio"] = relationship(
		"StockPortfolio",
		back_populates="holdings",
	)

	company_name: Mapped[str] = mapped_column(
		String(200),
		nullable=False,
	)

	ticker: Mapped[str] = mapped_column(
		String(20),
		nullable=False,
	)

	exchange: Mapped[Exchange] = mapped_column(
		Enum(Exchange),
		nullable=False,
	)

	quantity: Mapped[int] = mapped_column(
		Integer,
		nullable=False,
	)

	buy_price: Mapped[Decimal] = mapped_column(
		Numeric(18, 2),
		nullable=False,
	)

	buy_date: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		nullable=False,
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		nullable=False,
	)

	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		onupdate=func.now(),
		nullable=False,
	)