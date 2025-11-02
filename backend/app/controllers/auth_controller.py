from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import AuthService
from app.schemas.user import UserLogin, Token
from app.utils.error_handler import get_exception_status_code, get_db_error_message
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

model_name = "User"

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    login_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        auth_service = AuthService(db)
        token_response = await auth_service.authenticate_user(login_data)

        print(f"token res: {token_response}")
        response.set_cookie(
            key="access_token",
            value=token_response.access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.access_token_expire_minutes
        )

        return token_response
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    print("Logged out successfully")
    return {"success": True, "message": "Logged out successfully"}
