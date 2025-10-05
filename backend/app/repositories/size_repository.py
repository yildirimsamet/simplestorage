from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from app.models.size import Size
from app.schemas.size import SizeCreate

class SizeRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
    
    async def get_sizes(self) -> List[Size]:
        sizes = await self.db.execute(select(Size))
        return sizes.scalars().all()

    async def create_size(self, size_data: SizeCreate) -> Size:
        size = Size(**size_data.model_dump())
        self.db.add(size)
        await self.db.commit()
        await self.db.refresh(size)
        return size