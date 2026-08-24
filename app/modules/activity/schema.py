from pydantic import BaseModel, ConfigDict, field_validator
from app.modules.activity.models import ActivityType
from typing import Optional
from uuid import UUID


# **************************************
# ****GENERIC API RESPONSE MESSAGES*****
# **************************************
class ActivityResponseMessage(BaseModel):
	message: str



# **************************************
# **********ACTIVITIES SCHEMA***********
# **************************************
class Activities(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	title: str
	user_id: UUID
	description: str
	type: ActivityType
	entity_id: Optional[UUID] = None
	entity_type: Optional[str] = None



# ******************(C)*******************
# ****SCHEMA FOR CREATING NEW ACTIVITY****
# ****************************************
class CreateNewActivityRequest(BaseModel):
	title: str
	description: str
	type: ActivityType
	entity_id: Optional[UUID] = None
	entity_type: Optional[str] = None

	@field_validator("title")
	@classmethod
	def validate_title(cls, value):

		title = value.strip()

		if not title:
			raise ValueError("Title cannot be empty")

		if(len(title) > 80):
			raise ValueError("Title cannot exceed 80 characters")

		if(len(title) < 10):
			raise ValueError("Title should be atleast 10 characters")

		return title


	@field_validator("description")
	@classmethod
	def validate_description(cls, value):

		description = value.strip()

		if not description:
			raise ValueError("Description cannot be empty")

		if(len(description) > 200):
			raise ValueError("Description cannot exceed 200 characters")

		if(len(description) < 10):
			raise ValueError("Description should be atleast 10 characters")

		return description



# ******************(R)********************
# ****SCHEMA FOR GETTING ALL ACTIVITIES****
# *****************************************
class GetAllActivitiesResponse(BaseModel):
	message: str
	activities: list[Activities]