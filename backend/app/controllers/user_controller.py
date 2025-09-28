from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database.postgresql import get_async_session
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security.dependencies import get_current_user
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

