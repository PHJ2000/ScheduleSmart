from fastapi import APIRouter, Depends
from app.schemas.user import UserProfile

from app.schemas.booking import (
    CreateBookingRequest, BookingResponse, BookingStatusUpdateResponse
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/booking", tags=["Booking"])

@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(payload: CreateBookingRequest):
    return BookingResponse(
        id="mock-booking-uuid",
        guest_name=payload.guest_name,
        guest_email=payload.guest_email,
        start_time=payload.start_time,
        end_time=payload.end_time,
        status="pending"
    )

@router.get("/", response_model=list[BookingResponse])
async def list_bookings(current_user: UserProfile = Depends(get_current_user)):
    return []

@router.post("/{booking_id}/accept", response_model=BookingStatusUpdateResponse)
async def accept_booking(
    booking_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    return BookingStatusUpdateResponse(message="Booking accepted successfully")

@router.post("/{booking_id}/reject", response_model=BookingStatusUpdateResponse)
async def reject_booking(
    booking_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    return BookingStatusUpdateResponse(message="Booking rejected successfully")
