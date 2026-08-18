from app.modules.auth.schemas import (
    VerifyRegistrationTokenResponse,
    VerifyRegistrationTokenRequest,
    VerifyUserResponse,
    VerifyUserRequest,
    RegisterResponse,
    RegisterRequest,
    DeleteResponse,
    DeleteRequest,
    LoginResponse,
    LoginRequest,
    UserResponse,
    UserRequest,
)

from app.modules.auth.models import User, UserSession

import app.modules.auth.services as auth_service

from fastapi import APIRouter, Depends, status

from app.api.v1.dependency import SessionDep


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post(
    "/verify-registration-token",
    response_model=VerifyRegistrationTokenResponse,
)
async def verify_registration_token(
    payload: VerifyRegistrationTokenRequest,
    db: SessionDep,
):
    return await auth_service.verify_user_registration_token(
        db=db,
        payload=payload,
    )


@auth_router.post(
    "/delete_pending_registration",
    response_model=DeleteResponse,
)
async def delete_pending_user(
    payload: DeleteRequest,
    db: SessionDep,
):
    return await auth_service.delete_pending_registration(
        db=db,
        payload=payload,
    )


@auth_router.post(
    "/create_user",
    response_model=VerifyUserResponse,
)
async def create_user(
    payload: VerifyUserRequest,
    db: SessionDep,
):
    return await auth_service.verify_and_create_new_user(
        db=db,
        payload=payload,
    )


@auth_router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    db: SessionDep,
):
    return await auth_service.register_user(
        db=db,
        payload=payload,
    )


@auth_router.get("/me")
async def current_user(
    current_user: User = Depends(
        auth_service.get_current_user
    ),
):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        verified_at=current_user.verified_at,
    )


@auth_router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    payload: LoginRequest,
    db: SessionDep,
):
    return await auth_service.login(
        db=db,
        payload=payload,
    )


@auth_router.post("/logout")
async def logout(
    db: SessionDep,
    current_session: UserSession = Depends(
        auth_service.get_current_session
    ),
):
    await auth_service.logout_user(
        db=db,
        current_session=current_session,
    )

    return {
        "message": "Successfully logged out"
    }