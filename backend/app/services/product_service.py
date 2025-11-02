from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductItem, ProductSizeDetail, ProductSizeAdd, ProductSizeUpdate
from app.core.cache.redis import get_redis
from app.core.constants import REDIS_KEYS
from typing import List
import json


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repository = ProductRepository(db)

    async def _invalidate_search_cache(self):
        redis = await get_redis()
        try:
            pattern = REDIS_KEYS["product"]["search"].replace("{query}", "*")
            cursor = 0
            while True:
                cursor, keys = await redis.scan(cursor, match=pattern, count=100)
                if keys:
                    await redis.delete(*keys)
                if cursor == 0:
                    break
        except Exception:
            pass

    def _transform_to_product_item(self, product) -> ProductItem:
        sizes = [
            ProductSizeDetail(
                size_id=product_size.size_id,
                size_name=product_size.size.name,
                price=product_size.price,
                stock=product_size.stock
            )
            for product_size in product.product_sizes
        ]

        return ProductItem(
            id=product.id,
            name=product.name,
            image=product.image,
            description=product.description,
            category_id=product.category_id,
            sizes=sizes
        )

    async def get_products(self) -> List[ProductItem]:
        products = await self.product_repository.get_products()
        return [self._transform_to_product_item(product) for product in products]

    async def create_product(self, product_data: ProductCreate) -> ProductItem:
        product = await self.product_repository.create_product(product_data)
        await self._invalidate_search_cache()

        return ProductItem(
            id=product.id,
            name=product.name,
            image=product.image,
            description=product.description,
            category_id=product.category_id,
            sizes=[]
        )

    async def add_size_to_product(self, product_id: int, size_data: ProductSizeAdd) -> ProductItem:
        product = await self.product_repository.add_size_to_product(product_id, size_data)
        await self._invalidate_search_cache()
        return self._transform_to_product_item(product)

    async def delete_size_from_product(self, product_id: int, size_id: int) -> ProductItem:
        product = await self.product_repository.delete_size_from_product(product_id, size_id)
        await self._invalidate_search_cache()
        return self._transform_to_product_item(product)

    async def update_product_size(self, product_id: int, size_id: int, size_data: ProductSizeUpdate) -> ProductItem:
        product = await self.product_repository.update_product_size(product_id, size_id, size_data)
        await self._invalidate_search_cache()
        return self._transform_to_product_item(product)

    async def search_products(self, search_query: str) -> List[ProductItem]:
        cache_key = REDIS_KEYS["product"]["search"].format(query=search_query.lower())
        redis = await get_redis()

        try:
            cached_data = await redis.get(cache_key)
            if cached_data:
                products_data = json.loads(cached_data)
                print('return from cache#########')
                return [ProductItem(**item) for item in products_data]
        except (Exception):
            pass

        products = await self.product_repository.search_products(search_query)
        product_items = [self._transform_to_product_item(product) for product in products]

        try:
            serialized_data = json.dumps([item.model_dump() for item in product_items])
            await redis.setex(cache_key, 300, serialized_data)
        except (Exception):
            pass

        print('return from db########')
        return product_items
