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

from app.core.security import (
    generate_verification_token,
    generate_verification_link,
    hash_verification_token,
    create_access_token,
    decode_access_token,
    verify_password,
    hash_password,
)

from app.modules.auth.models import (
    PendingRegistration,
    UserSession,
    User,
)

from datetime import datetime, timezone, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError

from app.api.v1.dependency import SessionDep

from fastapi import HTTPException, status, Depends

from sqlalchemy.orm import Session
from sqlalchemy import select

from uuid import UUID

from app.utils.mail_service import send_email_verification_mail


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


token_timeout_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token expired. Please generate new access token",
    headers={"WWW-Authenticate": "Bearer"},
)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)


authentication_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password",
)


async def login(
    db: Session,
    payload: LoginRequest,
) -> LoginResponse:

    # Find user by email
    find_user_statement = select(User).where(
        User.email == payload.email
    )

    result = db.execute(find_user_statement)

    user = result.scalar_one_or_none()

    # If user is not present
    if not user:
        raise authentication_exception

    # If password verification failed
    password_match = verify_password(
        payload.password,
        user.password_hash,
    )

    if not password_match:
        raise authentication_exception

    # Generate JWT token, JTI and expiration
    jwt_token, jti, expires_at = create_access_token(user.id)

    # Create user's session
    user_session = UserSession(
        jti=jti,
        user_id=user.id,
        expires_at=expires_at,
    )

    db.add(user_session)
    db.commit()

    return LoginResponse(
        token_type="bearer",
        access_token=jwt_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            verified_at=user.verified_at,
        ),
    )


async def get_current_session(
    db: SessionDep,
    token: str = Depends(oauth2_scheme),
) -> UserSession:

    try:
        # Decode and validate JWT
        jwt_payload = decode_access_token(token)

        # Extract JTI
        jti = jwt_payload.get("jti")

        if not jti:
            raise credentials_exception

        current_jti = UUID(jti)

    except ExpiredSignatureError:
        raise token_timeout_exception

    except (JWTError, ValueError):
        raise credentials_exception

    # Find the session associated with this JWT
    session_statement = select(UserSession).where(
        UserSession.jti == current_jti
    )

    user_session = db.execute(
        session_statement
    ).scalar_one_or_none()

    # Session was deleted/revoked
    if not user_session:
        raise credentials_exception

    return user_session


async def get_current_user(
    db: SessionDep,
    current_session: UserSession = Depends(get_current_session),
) -> User:

    current_user_statement = select(User).where(
        User.id == current_session.user_id
    )

    result = db.execute(
        current_user_statement
    ).scalar_one_or_none()

    if result is None:
        raise user_not_found_exception

    return result


async def logout_user(
    db: SessionDep,
    current_session: UserSession,
):
    db.delete(current_session)
    db.commit()


async def verify_user_registration_token(
    db: Session,
    payload: VerifyRegistrationTokenRequest,
) -> VerifyRegistrationTokenResponse:

    hashed_token = hash_verification_token(
        payload.verification_token
    )

    # Get the user from pending registrations table
    statement = select(PendingRegistration).where(
        PendingRegistration.token == hashed_token
    )

    result = db.execute(statement)

    pending_registration = result.scalar_one_or_none()

    print(pending_registration.email)

    # Check if token is valid
    if not pending_registration:
        return VerifyRegistrationTokenResponse(
            status="invalid",
        )

    # Check if token has expired
    if datetime.now(timezone.utc) > pending_registration.expires_at:
        return VerifyRegistrationTokenResponse(
            status="expired",
        )

    return VerifyRegistrationTokenResponse(
        status="valid",
    )


async def register_user(
    db: Session,
    payload: RegisterRequest,
) -> RegisterResponse:

    # Check if user already registered
    existing_user_statement = select(User).where(
        User.email == payload.email
    )

    existing_user_result = db.execute(
        existing_user_statement
    )

    existing_user = existing_user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account already exists with this email.",
        )

    # Get the user from pending registrations table
    statement = select(PendingRegistration).where(
        PendingRegistration.email == payload.email
    )

    result = db.execute(statement)

    pending_registration = result.scalar_one_or_none()

    # Existing pending registration found
    if pending_registration:

        # If token is still valid
        if pending_registration.expires_at > datetime.now(timezone.utc):

            remaining_seconds = int(
                (
                    pending_registration.expires_at
                    - datetime.now(timezone.utc)
                ).total_seconds()
            )

            return RegisterResponse(
                message="Verification email already sent",
                expires_in=remaining_seconds,
                can_resend=False,
            )

        # If token expired
        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(minutes=5)
        )

        token = generate_verification_token()
        hashed_token = hash_verification_token(token)

        pending_registration.expires_at = expires_at
        pending_registration.token = hashed_token

        db.commit()

        db.refresh(pending_registration)

        verification_link = generate_verification_link(token)

        await send_email_verification_mail(
            verification_link,
            payload.email,
        )

        return RegisterResponse(
            message="Previous verification expired. A new verification email will be sent.",
            verification_token=token,
            can_resend=True,
            expires_in=300,
        )

    # No pending registration exists
    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(minutes=5)
    )

    token = generate_verification_token()
    hashed_token = hash_verification_token(token)

    new_pending_registration = PendingRegistration(
        expires_at=expires_at,
        email=payload.email,
        token=hashed_token,
    )

    db.add(new_pending_registration)

    db.commit()

    db.refresh(new_pending_registration)

    verification_link = generate_verification_link(token)

    await send_email_verification_mail(
        verification_link,
        payload.email,
    )

    return RegisterResponse(
        message="Verification email sent successfully",
        verification_token=token,
        can_resend=False,
        expires_in=300,
    )


async def delete_pending_registration(
    db: Session,
    payload: DeleteRequest,
) -> DeleteResponse:

    statement = select(PendingRegistration).where(
        PendingRegistration.email == payload.email
    )

    result = db.execute(statement)

    pending_registration = result.scalar_one_or_none()

    if pending_registration:

        db.delete(pending_registration)

        db.commit()

        return DeleteResponse(
            message=(
                f"User with email {payload.email} "
                "deleted successfully from pending registrations"
            )
        )

    return DeleteResponse(
        message=(
            f"No user with email {payload.email} "
            "found in pending registrations"
        )
    )


async def verify_and_create_new_user(
    db: Session,
    payload: VerifyUserRequest,
) -> VerifyUserResponse:

    # Hash incoming raw token
    hashed_token = hash_verification_token(
        payload.token
    )

    # Hash plain text password
    hashed_password = hash_password(
        payload.password
    )

    # Find user in pending registrations
    statement = select(PendingRegistration).where(
        PendingRegistration.token == hashed_token
    )

    result = db.execute(statement)

    pending_registration = result.scalar_one_or_none()

    # Check if token is valid
    if not pending_registration:
        return VerifyUserResponse(
            message="Invalid token."
        )

    # Check if token is expired
    if datetime.now(timezone.utc) > pending_registration.expires_at:
        return VerifyUserResponse(
            message="Verification token expired."
        )

    # Create new user
    new_user = User(
        username=pending_registration.email,
        email=pending_registration.email,
        password_hash=hashed_password,
    )

    db.add(new_user)

    # Remove pending registration
    db.delete(pending_registration)

    # Commit user creation and pending registration removal
    db.commit()

    return VerifyUserResponse(
        message="User created successfully."
    )