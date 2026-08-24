from sqlalchemy import func, Enum, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID as SQLAlchemyUUID
from typing import Optional, TYPE_CHECKING
from enum import Enum as PythonEnum
from datetime import datetime
from uuid import UUID, uuid4


if TYPE_CHECKING:
	from app.modules.auth.models import User


# ****************************************
# **ALLOWED VALUES FOR NOTIFICATION TYPE**
# ****************************************
class ActivityType(PythonEnum):
	portfolio_update="portfolio_update"
	account_settings="account_settings"
	security="security"
	insight="insight"
	system="system"


class Activity(object):
	
	__tablename__ = "notifications"

	# Primary Key
	id: Mapped[UUID] = mapped_column(
		SQLAlchemyUUID(as_uuid=True),
		primary_key=True,
		default=uuid4,
	)

	# Foreign Key
	user_id: Mapped[UUID] = mapped_column(
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)

	# Many-To-One Relationship with user
	user: Mapped["User"] = relationship(
		"User",
		back_populates="user_activities",
	)

	type: Mapped[Optional[ActivityType]] = mapped_column(
		Enum(ActivityType),
		nullable=False,
	)

	title: Mapped[str] = mapped_column(
		String(80),
		nullable=False,
	)

	description: Mapped[str] = mapped_column(
		String(200),
		nullable=False,
	)

	entity_type: Mapped[Optional[str]] = mapped_column(
		String(50),
		nullable=True,
	)
	
	entity_id: Mapped[Optional[UUID]] = mapped_column(
		SQLAlchemyUUID(as_uuid=True),
		nullable=True,
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		nullable=False,
	)