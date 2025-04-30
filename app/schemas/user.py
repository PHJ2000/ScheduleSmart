from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    email: str
    name: str
    profile_image: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UpdateUserProfileRequest(BaseModel):
    name: str
    profile_image: Optional[str] = None

class UpdateUserProfileResponse(BaseModel):
    message: str
