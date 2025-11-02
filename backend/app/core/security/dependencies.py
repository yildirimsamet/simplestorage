from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.postgresql import get_async_session
from app.core.security.jwt import verify_token
from app.services.auth_service import AuthService
from app.schemas.user import UserResponse


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserResponse:

    token = request.cookies.get("access_token")
    print(token)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    payload = verify_token(token)
    print(payload)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user data"
        )

    auth_service = AuthService(db)
    user = await auth_service.get_current_user(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user