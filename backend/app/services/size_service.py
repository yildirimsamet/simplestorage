from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.size_repository import SizeRepository
from app.schemas.size import SizeCreate, SizeUpdate, SizeItem
from app.models.size import Size
from typing import List

class SizeService:
    def __init__(self, db: AsyncSession):
        self.size_repository = SizeRepository(db)

    async def get_sizes(self) -> List[Size]:
        return await self.size_repository.get_sizes()

    async def create_size(self, size_data: SizeCreate) -> Size:
        return await self.size_repository.create_size(size_data)

    async def update_size(self, size_id: int, size_data: SizeUpdate) -> SizeItem:
        size = await self.size_repository.update_size(size_id, size_data)

        return SizeItem(
            id=size.id,
            name=size.name,
            display_order=size.display_order
        )

    async def delete_size(self, size_id: int) -> SizeItem:
        size = await self.size_repository.delete_size(size_id)

        return SizeItem(
            id=size.id,
            name=size.name,
            display_order=size.display_order
        )