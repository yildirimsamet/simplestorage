from datetime import timedelta
from typing import Optional
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.core.security.jwt import verify_password, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def authenticate_user(self, login_data: UserLogin) -> Token:
        user = await self.user_repository.get_user_by_username(login_data.username)

        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Auth error",
            )

        access_token_expires = timedelta(minutes=1)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, username: str) -> Optional[UserResponse]:
        user = await self.user_repository.get_user_by_username(username)

        if user is None:
            return None

        return UserResponse.model_validate(user)