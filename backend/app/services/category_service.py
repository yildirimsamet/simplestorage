from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate
from typing import List
from app.models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repository = CategoryRepository(db)

    async def get_all_categories(self) -> List[Category]:
        return await self.category_repository.get_all_categories()
    
    async def create_category(self, category_data: CategoryCreate) -> Category:
        return await self.category_repository.create_category(category_data)