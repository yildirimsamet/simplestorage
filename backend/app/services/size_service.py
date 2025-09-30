from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.size_repository import SizeRepository
from app.schemas.size import SizeCreate
from app.models.size import Size
from typing import List

class SizeService:
    def __init__(self, db: AsyncSession):
        self.size_repository = SizeRepository(db)
    
    async def get_sizes(self) -> List[Size]:
        return await self.size_repository.get_sizes()

    async def create_size(self, size_data: SizeCreate) -> Size:
        return await self.size_repository.create_size(size_data)