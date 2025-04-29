from fastapi import APIRouter, Depends
from app.schemas.user import UserProfile
from app.schemas.availability import (
    CreateAvailabilityRequest, AvailabilityResponse,
    UpdateAvailabilityRequest, MessageResponse
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/availability", tags=["Availability"])

@router.post("/", response_model=AvailabilityResponse, status_code=201)
async def create_availability(
    payload: CreateAvailabilityRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    return AvailabilityResponse(
        id="mock-uuid",
        start_time=payload.start_time,
        end_time=payload.end_time,
        is_active=True
    )

@router.get("/", response_model=list[AvailabilityResponse])
async def list_availabilities(current_user: UserProfile = Depends(get_current_user)):
    return []

@router.patch("/{availability_id}", response_model=MessageResponse)
async def update_availability(
    availability_id: str,
    payload: UpdateAvailabilityRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    return MessageResponse(message="Availability updated successfully")

@router.delete("/{availability_id}", response_model=MessageResponse)
async def delete_availability(
    availability_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    return MessageResponse(message="Availability deleted (deactivated) successfully")
