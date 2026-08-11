from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	pass

class MFPortfolio(Base):

	__tablename__ = "mutual_funds_portfolio"