from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.models.product import Product
from typing import List

class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repository = ProductRepository(db)
    
    async def get_products(self) -> List[Product]:
        return await self.product_repository.get_products()

    async def create_product(self, product_data: ProductCreate) -> Product:
        return await self.product_repository.create_product(product_data)