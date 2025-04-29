from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from app.schemas.auth import TokenResponse
from app.utils.auth import create_access_token
from app.core.config import settings
import httpx
from datetime import timedelta
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

# 구글 OAuth 관련 상수
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

@router.get("/google/login")
async def google_login():
    """
    구글 OAuth 로그인 URL 반환 (Swagger 친화형)
    """
    redirect_uri = "http://localhost:8000/api/v1/auth/google/callback"
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&redirect_uri={redirect_uri}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return JSONResponse(content={"redirect_url": google_auth_url})

@router.get("/google/callback", response_model=TokenResponse)
async def google_callback(code: str):
    """
    구글 로그인 완료 후 콜백 처리: access_token 발급
    """
    redirect_uri = "http://localhost:8000/api/v1/auth/google/callback"

    async with httpx.AsyncClient() as client:
        # 1. 구글에 토큰 요청
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch token from Google")

        token_json = token_response.json()
        access_token = token_json.get("access_token")

        # 2. 구글에서 사용자 정보 요청
        userinfo_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if userinfo_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")

        user_info = userinfo_response.json()

    # 3. 우리 서버 JWT 발급
    token_data = {
        "sub": user_info["sub"],
        "email": user_info["email"],
        "name": user_info.get("name", ""),
        "profile_image": user_info.get("picture", None)
    }

    jwt_token = create_access_token(
        subject=token_data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=jwt_token,
        token_type="bearer"
    )
