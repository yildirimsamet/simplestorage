from pydantic import BaseModel
from typing import Optional

class SizeBase(BaseModel):
    name: str

class SizeCreate(SizeBase):
    pass

class SizeUpdate(SizeBase):
    pass


class SizeResponse(SizeBase):
    id: int

    class Config:
        from_attributes = True