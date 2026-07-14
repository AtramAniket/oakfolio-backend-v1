from app.db.session import SessionLocal
from collections.abc import Generator
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()

	try:
		yield db
	finally:
		db.close()


SessionDep = Annotated[Session,Depends(get_db)]