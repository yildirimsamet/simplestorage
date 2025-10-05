from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database.postgresql import get_async_session
from app.schemas.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security.dependencies import get_current_user
from app.services.user_service import UserService
from app.utils.error_handler import get_db_error_message, get_exception_status_code

router = APIRouter(prefix="/users", tags=["users"])
model_name = "User"

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )
