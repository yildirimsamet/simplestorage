from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse, ProductSizeAdd, ProductSizeUpdate
from app.core.security.dependencies import get_current_user
from app.schemas.user import UserResponse
from app.utils.error_handler import get_db_error_message, get_exception_status_code
from app.utils.file_handler import save_upload_file
from typing import Optional

router = APIRouter(prefix="/products", tags=["products"])

model_name = "Product"

@router.get("/", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_products(
    db: AsyncSession = Depends(get_async_session),
):
    try:
        product_service = ProductService(db)
        product_items = await product_service.get_products()

        return ProductResponse(
            success=True,
            data=product_items
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.get("/search", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def search_products(
    search_query: str,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        product_service = ProductService(db)
        product_items = await product_service.search_products(search_query)

        return ProductResponse(
            success=True,
            data=product_items
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate = Depends(ProductCreate.as_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        if image:
            image_filename = await save_upload_file(image)
            product_data.image = image_filename

        product_service = ProductService(db)
        product_item = await product_service.create_product(product_data)

        return ProductResponse(
            success=True,
            data=product_item
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.post("/{product_id}/sizes", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def add_size_to_product(
    product_id: int,
    size_data: ProductSizeAdd,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        product_service = ProductService(db)
        product_item = await product_service.add_size_to_product(product_id, size_data)

        return ProductResponse(
            success=True,
            data=product_item
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.delete("/{product_id}/sizes/{size_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def delete_size_from_product(
    product_id: int,
    size_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        product_service = ProductService(db)
        product_item = await product_service.delete_size_from_product(product_id, size_id)

        return ProductResponse(
            success=True,
            data=product_item
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.put("/{product_id}/sizes/{size_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product_size(
    product_id: int,
    size_id: int,
    size_data: ProductSizeUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        product_service = ProductService(db)
        product_item = await product_service.update_product_size(product_id, size_id, size_data)

        return ProductResponse(
            success=True,
            data=product_item
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )
