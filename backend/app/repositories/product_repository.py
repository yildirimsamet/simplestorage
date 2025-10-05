from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_products(self) -> List[Product]:
        query = select(Product)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
