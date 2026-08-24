from app.modules.activity.schema import Activities, ActivityResponseMessage, CreateNewActivityRequest, GetAllActivitiesResponse
import app.modules.activity.services as activity_service
from app.modules.auth.dependencies import UserDep
from app.api.v1.dependency import SessionDep
from fastapi import APIRouter, status
from uuid import UUID



api_v1_activities_router = APIRouter(prefix="/activities", tags=["Oakfolio Activities"])





# *********************************CREATE NEW ACTIVITY**********************************
# *********************************** METHOD: POST *************************************
# ************************ API ENDPOINT: /api/v1/activities/new ************************
# **************************************************************************************
@api_v1_activities_router.post("/new", response_model=ActivityResponseMessage, status_code=status.HTTP_201_CREATED)
async def create_new_activity(
		db: SessionDep,
		current_user: UserDep,
		payload: CreateNewActivityRequest,
	):
	
	return await activity_service.create_new_activity(
		db=db,
		payload=payload,
		current_user=current_user,
	)





# **********************************GET ALL ACTIVITIES**********************************
# ************************************ METHOD: GET *************************************
# ************************ API ENDPOINT: /api/v1/activities/ ***************************
# **************************************************************************************
@api_v1_activities_router.get("/", response_model=GetAllActivitiesResponse, status_code=status.HTTP_200_OK)
async def get_all_activities(
		db: SessionDep,
		current_user: UserDep,
	):
	
	return await activity_service.get_all_activities(
		db=db,
		current_user=current_user,
	)
