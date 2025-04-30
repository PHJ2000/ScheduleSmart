from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateAvailabilityRequest(BaseModel):
    start_time: datetime
    end_time: datetime

class UpdateAvailabilityRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class AvailabilityResponse(BaseModel):
    id: str
    start_time: datetime
    end_time: datetime
    is_active: bool

class MessageResponse(BaseModel):
    message: str
