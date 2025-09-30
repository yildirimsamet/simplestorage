from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from app.models.product_size import ProductSize
from app.schemas.product_size import ProductSizeCreate

class ProductSizeRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
    
    async def get_product_sizes(self) -> List[ProductSize]:
        product_sizes = self.db.execute(select(ProductSize))
        return product_sizes.scalar().all()

    async def create_product_size(self, product_sizes_data: ProductSizeCreate) -> ProductSize:
        product_size = ProductSize(**product_sizes_data.model_dump())

        self.db.add(product_size)

        await self.db.commit()
        await self.db.refresh(product_size)

        return product_size