from pydantic import BaseModel
from typing import Optional, List, Union
from fastapi import Form


class ProductBase(BaseModel):
    name: str
    image: Optional[str] = None
    description: Optional[str] = None
    category_id: int


class ProductCreate(ProductBase):
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        category_id: int = Form(...),
        description: Optional[str] = Form(None)
    ):
        return cls(name=name, category_id=category_id, description=description)


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


class ProductSizeAdd(BaseModel):
    size_id: int
    price: float
    stock: int


class ProductSizeUpdate(BaseModel):
    price: Optional[float] = None
    stock: Optional[int] = None