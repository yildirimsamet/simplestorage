from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductSizeDetail

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_products(self) -> List[ProductResponse]:
        query = select(Product)
        result = await self.db.execute(query)
        products = result.scalars().all()

        product_responses = []

        for product in products:
            sizes = []

            for ps in product.product_sizes:
                size_detail = ProductSizeDetail(
                    size_id=ps.size_id,
                    size_name=ps.size.name,
                    price=ps.price,
                    stock=ps.stock
                )

                sizes.append(size_detail)

            product_response = ProductResponse(
                id=product.id,
                name=product.name,
                image=product.image,
                description=product.description,
                category_id=product.category_id,
                sizes=sizes
            )
            product_responses.append(product_response)

        return product_responses

    async def create_product(self, product_data: ProductCreate) -> Product:

        print(f"product data: {product_data}")
        product = Product(**product_data.model_dump())
        print(f"product: {product}")
        self.db.add(product)

        await self.db.commit()
        await self.db.refresh(product)
        return product
        
        