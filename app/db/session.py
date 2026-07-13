from app.core.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABSE_URL, echo=settings.debug)

SessionLocal = sessionmaker(
	bind=engine,
	autoflush=True,
	autocommit=True,
)