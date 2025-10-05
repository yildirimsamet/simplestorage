from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductItem, ProductSizeDetail
from typing import List


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repository = ProductRepository(db)

    async def get_products(self) -> List[ProductItem]:
        products = await self.product_repository.get_products()

        product_items = []
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

            product_item = ProductItem(
                id=product.id,
                name=product.name,
                image=product.image,
                description=product.description,
                category_id=product.category_id,
                sizes=sizes
            )
            product_items.append(product_item)

        return product_items

    async def create_product(self, product_data: ProductCreate) -> ProductItem:
        product = await self.product_repository.create_product(product_data)

        return ProductItem(
            id=product.id,
            name=product.name,
            image=product.image,
            description=product.description,
            category_id=product.category_id,
            sizes=[]
        )
