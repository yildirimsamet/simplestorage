from pydantic import BaseModel
from typing import Optional, List, Union

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryItem(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Union[CategoryItem, List[CategoryItem]]] = None

    class Config:
        from_attributes = True
