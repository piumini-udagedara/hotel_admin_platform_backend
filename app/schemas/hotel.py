from pydantic import BaseModel
from typing import Optional


class HotelBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class HotelResponse(HotelBase):
    id: int
    status: str

    class Config:
        from_attributes = True