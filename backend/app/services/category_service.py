from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repository = CategoryRepository(db)

    async def get_all_categories(self) -> List[Category]:
        return await self.category_repository.get_all_categories()

    async def create_category(self, category_data: CategoryCreate) -> Category:
        return await self.category_repository.create_category(category_data)

    async def update_category(self, category_id: int, category_data: CategoryUpdate) -> Category:
        return await self.category_repository.update_category(category_id, category_data)

    async def delete_category(self, category_id: int) -> Category:
        return await self.category_repository.delete_category(category_id)
