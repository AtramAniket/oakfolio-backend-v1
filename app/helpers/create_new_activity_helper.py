from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.activity.models import Activity, ActivityType

def create_new_activity(
	title: str,
	db: Session,
	user_id: UUID,
	description: str,
	type: ActivityType,
	entity_id: Optional[UUID] = None,
	entity_type: Optional[str] = None,) -> Activity:

	activity = Activity(
		type=type,
		title=title,
		user_id=user_id,
		entity_id=entity_id,
		description=description,
		entity_type=entity_type,
	)


	db.add(activity)

	return activity