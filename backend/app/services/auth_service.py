from datetime import timedelta
from typing import Optional
from app.schemas.user import UserLogin, Token, UserResponse
from app.repositories.user_repository import UserRepository
from app.core.security.jwt import verify_password, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def authenticate_user(self, login_data: UserLogin) -> Token:
        user = await self.user_repository.get_user_by_username(login_data.username)

        if not user or not verify_password(login_data.password, user.hashed_password):
            raise ValueError("Username or password invalid")

        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, username: str) -> Optional[UserResponse]:
        user = await self.user_repository.get_user_by_username(username)

        if user is None:
            return None

        return UserResponse.model_validate(user)
