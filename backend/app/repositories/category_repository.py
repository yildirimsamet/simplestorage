from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select, update, delete
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_categories(self) -> List[Category]:
        result = await self.db.execute(select(Category))
        return result.scalars().all()

    async def create_category(self, category_data: CategoryCreate) -> Category:
        category = Category(name=category_data.name)

        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)

        return category

    async def update_category(self, category_id: int, category_data: CategoryUpdate) -> Category:
        query = update(Category).where(Category.id == category_id).values(**category_data.model_dump()).returning(Category)

        execute_result = await self.db.execute(query)
        category = execute_result.scalar_one_or_none()

        if category is None:
            raise ValueError(f"Category with id {category_id} not found")

        await self.db.commit()

        return category

    async def delete_category(self, category_id: int) -> Category:
        query = delete(Category).where(Category.id == category_id).returning(Category)

        execute_result = await self.db.execute(query)
        category = execute_result.scalar_one_or_none()

        if category is None:
            raise ValueError(f"Category with id {category_id} not found")

        await self.db.commit()

        return category
