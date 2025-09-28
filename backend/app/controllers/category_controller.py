from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model = List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories(
    db: AsyncSession = Depends(get_async_session)
):
    category_service = CategoryService(db)
    return await category_service.get_all_categories()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_async_session)
):
    category_service = CategoryService(db)
    return await category_service.create_category(category_data)