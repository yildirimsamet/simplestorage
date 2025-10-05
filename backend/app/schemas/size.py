from pydantic import BaseModel
from typing import Optional, List, Union


class SizeBase(BaseModel):
    name: str


class SizeCreate(SizeBase):
    pass


class SizeUpdate(BaseModel):
    name: Optional[str]
    display_order: Optional[int]


class SizeItem(SizeBase):
    id: int
    display_order: int

    class Config:
        from_attributes = True


class SizeResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Union[SizeItem, List[SizeItem]]] = None

    class Config:
        from_attributes = True