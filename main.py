from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# API 라우터 import
from app.api.v1 import auth, availability, booking, user

app = FastAPI(
    title="ScheduleSmart API",
    version="1.0.0",
    description="스케줄 스마트 서비스 API 문서입니다."
)

# CORS 설정 (나중에 origin을 안전하게 관리해야 함)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 개발 단계에서는 * 허용, 배포 시 수정 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(auth.router)
app.include_router(availability.router)
app.include_router(booking.router)
app.include_router(user.router)

# ✅ Swagger Authorize 버튼 활성화를 위한 custom_openapi 설정
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # 이 줄이 핵심!
