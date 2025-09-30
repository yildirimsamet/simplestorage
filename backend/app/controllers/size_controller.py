from fastapi import APIRouter, Depends, status
from app.schemas.size import SizeResponse, SizeCreate
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.services.size_service import SizeService

router = APIRouter(prefix="/sizes", tags=["sizes"])

@router.get("/", response_model= List[SizeResponse], status_code=status.HTTP_200_OK)
async def get_sizes(
    db: AsyncSession = Depends(get_async_session)
):
    size_service = SizeService(db)

    return await size_service.get_sizes()

@router.post("/", response_model= SizeResponse, status_code=status.HTTP_201_CREATED)
async def create_size(
    size_data: SizeCreate,
    db: AsyncSession = Depends(get_async_session)
):
    size_service = SizeService(db)

    return await size_service.create_size(size_data)