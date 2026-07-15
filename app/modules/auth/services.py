from app.modules.auth.schemas import RegisterRequest, RegisterResponse
from app.modules.auth.models import PendingRegistration
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select


async def register_user(db:Session, payload: RegisterRequest) -> RegisterResponse:
	statement = select(PendingRegistration).where(
		PendingRegistration.email == payload.email
	)
	
	result = db.execute(statement)

	pending_registration = result.scalar_one_or_none()

	# Existing pending registration found
	if pending_registration:

		# If token is still valid
		if pending_registration.expires_at > datetime.now(timezone.utc):
			remaining_seconds = int((pending_registration.expires_at - datetime.now(timezone.utc)).total_seconds())

			return RegisterResponse(
				message="Verification email already sent",
				expires_in=remaining_seconds,
				can_resend=False,
			)
		# If token expired
		return RegisterResponse(
			message="Previous verification expired. A new verification email will be sent.",
			expires_in=300,
			can_resend=True,
		)

	# No pending registration exists
	new_pending_registration = PendingRegistration(
		expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
		email=payload.email,
		token=f"test-{payload.email}",
	)

	db.add(new_pending_registration)

	db.commit()

	db.refresh(new_pending_registration)
	
	return RegisterResponse(
		message="Verification email already sent",
		expires_in=300,
		can_resend=False,
	)