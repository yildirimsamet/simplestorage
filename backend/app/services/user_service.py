from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        if await self.user_repository.check_user_exists(user_data.email, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User alread exist"
            )

        user = await self.user_repository.create_user(user_data)
        return UserResponse.model_validate(user)

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is None:
            return None
        return UserResponse.model_validate(user)

    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        user = await self.user_repository.get_user_by_username(username)
        if user is None:
            return None
        return UserResponse.model_validate(user)