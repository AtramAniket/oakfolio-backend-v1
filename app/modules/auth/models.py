from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, DateTime, func
from sqlalchemy import UUID as SQLAlchemyUUID
from typing import TYPE_CHECKING
from datetime import datetime
from app.db.base import Base
from uuid import UUID, uuid4

if TYPE_CHECKING:
	from app.modules.stocks.models import StockPortfolio, StockHolding


class PendingRegistration(Base):
	
	__tablename__ = "pending_registrations"

	id: Mapped[UUID] = mapped_column(
		SQLAlchemyUUID(as_uuid=True),
		primary_key=True,
		default=uuid4,
	)

	email: Mapped[str] = mapped_column(
		String(255),
		nullable=False,
		unique=True,
	)

	token: Mapped[str] = mapped_column(
		Text,
		nullable=False,
		unique=True,
	)

	expires_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		nullable=False,
	)


class User(Base):

	__tablename__ = "users"

	id: Mapped[UUID] = mapped_column(
		SQLAlchemyUUID(as_uuid=True),
		primary_key=True,
		default=uuid4,
	)

	email: Mapped[str] = mapped_column(
		String(255),
		nullable=False,
		unique=True,
	)

	username: Mapped[str] = mapped_column(
		String(100),
		nullable=False,
	)

	password_hash: Mapped[str] = mapped_column(
		Text,
		nullable=False,
	)

	verified_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		nullable=False,
	)

	stock_portfolios: Mapped[list["StockPortfolio"]] = relationship(
		"StockPortfolio",
		back_populates="user",
		cascade="all, delete-orphan",
		order_by="desc(StockPortfolio.created_at)",
	)

	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		onupdate=func.now(),
		nullable=False,
	)