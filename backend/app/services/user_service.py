from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> User:
        if await self.user_repository.check_user_exists(user_data.email, user_data.username):
            raise ValueError("User already exists")

        return await self.user_repository.create_user(user_data)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.user_repository.get_user_by_username(username)
