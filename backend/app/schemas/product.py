from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    image: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
