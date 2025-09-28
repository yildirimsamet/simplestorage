from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from app.models.category import Category
from app.schemas.category import CategoryCreate

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_categories(self) -> List[Category]:
        categories = await self.db.execute(select(Category))
        return categories.scalars().all()

    async def create_category(self, category_data: CategoryCreate) -> Category:
        print(f"category data: {category_data}")
        category = Category(name=category_data.name)
        
        self.db.add(category)
        await self.db.commit()

        await self.db.refresh(category)
        return category