from pydantic import BaseModel
from typing import Optional

class ProductSizeBase(BaseModel):
    product_id: int
    size_id: int
    price: float
    stock: int

class ProductSizeCreate(ProductSizeBase):
    pass

class ProductSizeUpdate(BaseModel):
    price: Optional[float] = None
    stock: Optional[int] = None


class ProductSizeResponse(ProductSizeBase):
    id: int

    class Config:
        from_attributes=True
