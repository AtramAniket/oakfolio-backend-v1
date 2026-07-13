from datetime import datetime
from app.db.base import Base
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, DateTime, func

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