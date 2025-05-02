from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.schemas.user import UserProfile

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/google/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserProfile:
    print(f"[DEBUG] Raw Token: {token}", flush=True)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"[DEBUG] Decoded Payload: {payload}", flush=True)

        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        name: str = payload.get("name")
        profile_image: str = payload.get("profile_image")

        if user_id is None or email is None:
            print("[DEBUG] Missing required user info in token.")
            raise _unauthorized()

        return UserProfile(
            id=user_id,
            email=email,
            name=name,
            profile_image=profile_image,
            created_at=None,
            updated_at=None
        )
    except JWTError as e:
        print(f"[DEBUG] JWTError occurred: {e}")
        raise _unauthorized()

def _unauthorized():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
