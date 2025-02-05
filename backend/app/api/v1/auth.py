from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()
_auth = AuthService()
_demo_user = _auth.create_user("analyst@example.com", "ChangeMe123")


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    token = _auth.authenticate(payload.email, payload.password, _demo_user["password_hash"])
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=token)
