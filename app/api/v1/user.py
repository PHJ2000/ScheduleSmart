from fastapi import APIRouter, Depends
from app.schemas.user import UserProfile, UpdateUserProfileRequest, UpdateUserProfileResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/user", tags=["User"])

@router.get("/me", response_model=UserProfile)
async def get_me(current_user: UserProfile = Depends(get_current_user)):
    print("Authorization Header:", request.headers.get("authorization"))
    return current_user

@router.patch("/me", response_model=UpdateUserProfileResponse)
async def update_me(
    payload: UpdateUserProfileRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    # 프로필 업데이트 처리
    return UpdateUserProfileResponse(message="Profile updated successfully")
