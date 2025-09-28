from app.core.database.postgresql import async_session_maker
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas.user import UserCreate


async def create_admin_user():
    async with async_session_maker() as db:
        try:
            user_service = UserService(db)

            existing_user = await user_service.get_user_by_username(settings.user_username)
            if existing_user:
                return

            admin_user_data = UserCreate(
                username=settings.user_username,
                password=settings.user_password,
                email=settings.user_email,
                is_admin=settings.user_is_admin
            )

            created_user = await user_service.create_user(admin_user_data)

        except Exception as e:
            print(f"Error: {e}")