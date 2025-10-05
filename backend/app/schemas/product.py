from pydantic import BaseModel
from typing import Optional, List, Union


class ProductBase(BaseModel):
    name: str
    image: Optional[str] = None
    description: Optional[str] = None
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductSizeDetail(BaseModel):
    size_id: int
    size_name: str
    price: float
    stock: int

    class Config:
        from_attributes = True


class ProductItem(ProductBase):
    id: int
    sizes: Optional[List[ProductSizeDetail]] = []

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Union[ProductItem, List[ProductItem]]] = None

    class Config:
        from_attributes = True
