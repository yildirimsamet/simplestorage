from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_size_repository import ProductSizeRepository
from app.schemas.product_size import ProductSizeCreate
from app.models.product_size import ProductSize
from typing import List

class ProductSizeService:
    def __init__(self, db: AsyncSession):
        self.product_size_repository = ProductSizeRepository(db)
    
    async def get_sizes_by_product_id(self, product_id: int) -> List[ProductSize]:
        return await self.product_size_repository.get_sizes_by_product_id(product_id)

    async def create_product_size(self, product_size_data: ProductSizeCreate) -> ProductSize:
        return await self.product_size_repository.create_product_size(product_size_data)