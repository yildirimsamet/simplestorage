from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from app.models.product import Product
from app.models.product_size import ProductSize
from app.schemas.product import ProductCreate, ProductSizeAdd, ProductSizeUpdate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_products(self) -> List[Product]:
        query = select(Product).options(
            selectinload(Product.product_sizes).selectinload(ProductSize.size)
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_product_by_id(self, product_id: int) -> Product:
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
    
        product = result.scalar_one_or_none()
    
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        return product

    async def add_size_to_product(self, product_id: int, size_data: ProductSizeAdd) -> Product:
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)

        product = result.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        product_size = ProductSize(
            product_id=product_id,
            size_id=size_data.size_id,
            price=size_data.price,
            stock=size_data.stock
        )
        self.db.add(product_size)
        await self.db.commit()

        query = select(Product).options(
            selectinload(Product.product_sizes).selectinload(ProductSize.size)
        ).where(Product.id == product_id)

        result = await self.db.execute(query)
        product = result.scalar_one_or_none()

        return product

    async def delete_size_from_product(self, product_id: int, size_id: int) -> Product:
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)

        product = result.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        query = select(ProductSize).where(
            ProductSize.product_id == product_id,
            ProductSize.size_id == size_id
        )

        result = await self.db.execute(query)
        product_size = result.scalar_one_or_none()

        if not product_size:
            raise ValueError(f"Size with id {size_id} not found for this product")

        await self.db.delete(product_size)
        await self.db.commit()

        query = select(Product).options(
            selectinload(Product.product_sizes).selectinload(ProductSize.size)
        ).where(Product.id == product_id)

        result = await self.db.execute(query)
        product = result.scalar_one_or_none()

        return product

    async def update_product_size(self, product_id: int, size_id: int, size_data: ProductSizeUpdate) -> Product:
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
        product = result.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        query = select(ProductSize).where(
            ProductSize.product_id == product_id,
            ProductSize.size_id == size_id
        )
        result = await self.db.execute(query)
        product_size = result.scalar_one_or_none()

        if not product_size:
            raise ValueError(f"Size with id {size_id} not found for this product")

        if size_data.price is not None:
            product_size.price = size_data.price

        if size_data.stock is not None:
            product_size.stock = size_data.stock

        await self.db.commit()

        query = select(Product).options(
            selectinload(Product.product_sizes).selectinload(ProductSize.size)
        ).where(Product.id == product_id)
    
        result = await self.db.execute(query)
        product = result.scalar_one_or_none()

        return product

    async def search_products(self, query_text: str) -> List[Product]:
        search_pattern = f"%{query_text}%"
        query = select(Product).options(
            selectinload(Product.product_sizes).selectinload(ProductSize.size)
        ).where(
            or_(Product.name.ilike(search_pattern),
            Product.description.ilike(search_pattern)
            )
        )

        result = await self.db.execute(query)

        return result.scalars().all()
