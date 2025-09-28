from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.product import ProductCreate, ProductResponse
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model = List[ProductResponse], status_code=status.HTTP_200_OK)
async def get_products(
    db: AsyncSession = Depends(get_async_session)):
    product_service = ProductService(db)
    return await product_service.get_products()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_async_session)
):
    product_service = ProductService(db)
    return await product_service.create_product(product_data)
