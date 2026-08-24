from fastapi import Depends
from typing import Annotated
from app.modules.auth.models import User
import app.modules.auth.services as auth_service

UserDep = Annotated[User, Depends(auth_service.get_current_user)]