from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.size_service import SizeService
from app.schemas.size import SizeCreate, SizeUpdate, SizeResponse
from app.utils.error_handler import get_db_error_message, get_exception_status_code

router = APIRouter(prefix="/sizes", tags=["sizes"])

model_name = "Size"

@router.get("/", response_model=SizeResponse, status_code=status.HTTP_200_OK)
async def get_sizes(
    db: AsyncSession = Depends(get_async_session)
):
    try:
        size_service = SizeService(db)
        sizes = await size_service.get_sizes()

        return SizeResponse(
            success=True,
            data=sizes
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.post("/", response_model=SizeResponse, status_code=status.HTTP_201_CREATED)
async def create_size(
    size_data: SizeCreate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        size_service = SizeService(db)
        size = await size_service.create_size(size_data)

        return SizeResponse(
            success=True,
            data=size
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.put("/{size_id}", response_model=SizeResponse, status_code=status.HTTP_200_OK)
async def update_size(
    size_id: int,
    size_data: SizeUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        size_service = SizeService(db)
        size = await size_service.update_size(size_id, size_data)

        return SizeResponse(
            success=True,
            data=size
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.delete("/{size_id}", response_model=SizeResponse, status_code=status.HTTP_200_OK)
async def delete_size(
    size_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        size_service = SizeService(db)
        size = await size_service.delete_size(size_id)

        return SizeResponse(
            success=True,
            data=size
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )
