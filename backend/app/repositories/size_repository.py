from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select
from app.models.size import Size
from app.schemas.size import SizeCreate, SizeUpdate

class SizeRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
    
    async def get_sizes(self) -> List[Size]:
        sizes = await self.db.execute(select(Size))
        return sizes.scalars().all()

    async def get_size_by_id(self, size_id: int) -> Optional[Size]:
        query = select(Size).where(Size.id == size_id)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_size_by_display_order(self, display_order: int) -> Optional[Size]:
        query = select(Size).where(Size.display_order == display_order)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def create_size(self, size_data: SizeCreate) -> Size:
        size = Size(**size_data.model_dump())
        self.db.add(size)
        await self.db.commit()
        await self.db.refresh(size)
        return size

    async def update_size(self, size_id: int, size_data: SizeUpdate) -> Size:
        size = await self.get_size_by_id(size_id)
        print(f"size---: {size}")

        if not size:
            raise ValueError(f"Size with id {size_id} not found")

        if size_data.name is not None:
            size.name = size_data.name

        if size_data.display_order is not None and size_data.display_order != size.display_order:
            existing_size = await self.get_size_by_display_order(size_data.display_order)
            if existing_size:
                existing_size.display_order = size.display_order
            size.display_order = size_data.display_order

        await self.db.commit()

        await self.db.refresh(size)
        return size

    async def delete_size(self, size_id: int) -> Size:
        size = await self.get_size_by_id(size_id)
        if not size:
            raise ValueError(f"Size with id {size_id} not found")

        await self.db.delete(size)
        await self.db.commit()
    
        return size