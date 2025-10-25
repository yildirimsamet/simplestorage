from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse
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
