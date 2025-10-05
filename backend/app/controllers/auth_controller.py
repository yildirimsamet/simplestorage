from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import AuthService
from app.schemas.user import UserLogin, Token
from app.utils.error_handler import get_exception_status_code, get_db_error_message

router = APIRouter(prefix="/auth", tags=["authentication"])

model_name = "User"

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        auth_service = AuthService(db)
        return await auth_service.authenticate_user(login_data)
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )
