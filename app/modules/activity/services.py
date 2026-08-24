from app.modules.activity.schema import Activities, ActivityResponseMessage, CreateNewActivityRequest, GetAllActivitiesResponse
from fastapi import HTTPException, APIRouter, status
from app.modules.activity.models import Activity
from app.api.v1.dependency import SessionDep
from app.modules.auth.models import User
from sqlalchemy import select
from uuid import UUID



async def create_new_activity(db: SessionDep, current_user: User, payload: CreateNewActivityRequest) -> ActivityResponseMessage:
	"""
	Create a new activity record for the current authenticated user.

	The activity is associated with the current user and may optionally
	reference an existing entity through its entity type and UUID.

	Args:
	    db: Database session used to persist the activity.
	    current_user: The authenticated user creating the activity.
	    payload: Activity details provided in the request.

	Example payload:
	    {
	        "title": "Stock Added",
	        "description": "RELIANCE was added to Growth Portfolio",
	        "type": "portfolio_update",
	        "entity_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
	        "entity_type": "holding"
	    }

	Returns:
	    ActivityResponseMessage: Confirmation that the activity was created.
	
	"""
	
	new_activity = Activity(
		type=payload.type,
		title = payload.title,
		user_id=current_user.id,
		entity_id=payload.entity_id,
		entity_type=payload.entity_type,
		description=payload.description,
	)

	db.add(new_activity)

	db.commit()

	db.refresh(new_activity)

	return ActivityResponseMessage(
		message="Activity added successfully"
	)



async def get_all_activities(db: SessionDep, current_user: User) -> GetAllActivitiesResponse:
	"""
	Retrieve all activities belonging to the current authenticated user.

	Activities are filtered by the current user's ID and returned in
	reverse chronological order, with the most recent activity first.

	Args:
	    db: Database session used to retrieve activities.
	    current_user: The authenticated user whose activities are being retrieved.

	Returns:
	    GetAllActivitiesResponse: A collection containing the user's activities.
	    return an empty array if no activities are found
    """
	statement = select(Activity).where(
		Activity.user_id == current_user.id
	)

	result = db.execute(statement)

	user_activities = result.scalars().all()

	if not user_activities:
		return GetAllActivitiesResponse(
			message = "No activities found",
			activities=[],
		)

	else:
		return GetAllActivitiesResponse(
			message="Activites Found",
			activities=user_activities,
		)

