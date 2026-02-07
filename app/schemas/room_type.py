from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class RoomTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_rate: float = Field(..., gt=0)
    capacity: int = Field(default=2, ge=1)


class RoomTypeCreate(RoomTypeBase):
    hotel_id: int


class RoomTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_rate: Optional[float] = Field(None, gt=0)
    capacity: Optional[int] = Field(None, ge=1)


class RateAdjustmentBase(BaseModel):
    adjustment_amount: float
    effective_date: date
    reason: Optional[str] = None


class RateAdjustmentCreate(RateAdjustmentBase):
    room_type_id: int


class RateAdjustmentResponse(RateAdjustmentBase):
    id: int
    room_type_id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class RoomTypeResponse(RoomTypeBase):
    id: int
    hotel_id: int
    effective_rate: Optional[float] = None
    current_adjustment: Optional[float] = None

    class Config:
        from_attributes = True


class RoomTypeDetailResponse(RoomTypeResponse):
    rate_adjustments: list[RateAdjustmentResponse] = []

    class Config:
        from_attributes = True