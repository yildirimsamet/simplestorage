from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database.postgresql import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.core.security.dependencies import get_current_user
from app.schemas.user import UserResponse
from app.utils.error_handler import get_db_error_message, get_exception_status_code

router = APIRouter(prefix="/categories", tags=["categories"])

model_name = "Category"

@router.get("/", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_all_categories(
    db: AsyncSession = Depends(get_async_session),
):
    try:
        category_service = CategoryService(db)
        categories = await category_service.get_all_categories()

        return CategoryResponse(
            success=True,
            data=categories
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=get_db_error_message(e, model_name)
        )


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        category_service = CategoryService(db)
        category = await category_service.create_category(category_data)

        return CategoryResponse(
            success=True,
            data=category
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        category_service = CategoryService(db)
        category = await category_service.update_category(category_id, category_data)

        return CategoryResponse(
            success=True,
            data=category
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )


@router.delete("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        category_service = CategoryService(db)
        category = await category_service.delete_category(category_id)

        return CategoryResponse(
            success=True,
            data=category
        )
    except Exception as e:
        raise HTTPException(
            status_code=get_exception_status_code(e),
            detail=get_db_error_message(e, model_name)
        )
