from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.postgresql import get_async_session
from app.core.security.jwt import verify_token
from app.services.auth_service import AuthService
from app.schemas.user import UserResponse

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session)
) -> UserResponse: 

    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="JWT payload error",
    )

    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="JWT username 'sub' not found error",
    )

    auth_service = AuthService(db)
    user = await auth_service.get_current_user(username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found")

    return user