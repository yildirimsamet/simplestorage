from pydantic import BaseModel
from typing import Optional

class SizeBase(BaseModel):
    name: str

class SizeCreate(SizeBase):
    pass

class SizeUpdate(BaseModel):
    name: Optional[str]
    display_order: Optional[int]


class SizeResponse(SizeBase):
    id: int
    display_order: int

    class Config:
        from_attributes = True