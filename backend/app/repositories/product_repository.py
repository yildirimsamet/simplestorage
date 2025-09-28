from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from app.models.product import Product
from app.schemas.product import ProductCreate

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_products(self) -> List[Product]:
        products = await self.db.execute(select(Product))
        return products.scalars().all()

    async def create_product(self, product_data: ProductCreate) -> Product:

        print(f"product data: {product_data}")
        product = Product(**product_data.model_dump())
        print(f"product: {product}")
        self.db.add(product)

        await self.db.commit()
        await self.db.refresh(product)
        return product
        
        