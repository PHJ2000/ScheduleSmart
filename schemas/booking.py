from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateBookingRequest(BaseModel):
    guest_name: str
    guest_email: EmailStr
    start_time: datetime
    end_time: datetime

class BookingResponse(BaseModel):
    id: str
    guest_name: str
    guest_email: EmailStr
    start_time: datetime
    end_time: datetime
    status: str  # 예: "pending", "accepted", "rejected"

class BookingStatusUpdateResponse(BaseModel):
    message: str
