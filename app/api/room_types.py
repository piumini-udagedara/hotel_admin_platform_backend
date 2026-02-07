from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import date

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.room_type import RoomType
from app.models.rate_adjustment import RateAdjustment
from app.models.user import User
from app.schemas.room_type import (
    RoomTypeCreate, RoomTypeUpdate, RoomTypeResponse, 
    RoomTypeDetailResponse, RateAdjustmentCreate, RateAdjustmentResponse
)

router = APIRouter(prefix="/room-types", tags=["room-types"])


def calculate_effective_rate(room_type: RoomType, reference_date: date = None) -> tuple[float, float]:
    """Calculate effective rate for a room type based on the latest adjustment."""
    if reference_date is None:
        reference_date = date.today()
    
    # Get the latest adjustment with effective_date <= reference_date
    latest_adjustment = (
        Session.object_session(room_type)
        .query(RateAdjustment)
        .filter(
            and_(
                RateAdjustment.room_type_id == room_type.id,
                RateAdjustment.effective_date <= reference_date
            )
        )
        .order_by(RateAdjustment.effective_date.desc())
        .first()
    )
    
    adjustment_amount = latest_adjustment.adjustment_amount if latest_adjustment else 0.0
    effective_rate = room_type.base_rate + adjustment_amount
    
    return effective_rate, adjustment_amount


@router.get("", response_model=List[RoomTypeResponse])
def list_room_types(
    hotel_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(RoomType)
    if hotel_id:
        query = query.filter(RoomType.hotel_id == hotel_id)
    
    room_types = query.offset(skip).limit(limit).all()
    
    # Add effective rates
    result = []
    for rt in room_types:
        effective_rate, current_adjustment = calculate_effective_rate(rt)
        rt_dict = RoomTypeResponse.model_validate(rt).model_dump()
        rt_dict["effective_rate"] = effective_rate
        rt_dict["current_adjustment"] = current_adjustment
        result.append(RoomTypeResponse(**rt_dict))
    
    return result


@router.get("/{room_type_id}", response_model=RoomTypeDetailResponse)
def get_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    
    effective_rate, current_adjustment = calculate_effective_rate(room_type)
    
    # Get all adjustments sorted by effective_date descending
    adjustments = (
        db.query(RateAdjustment)
        .filter(RateAdjustment.room_type_id == room_type_id)
        .order_by(RateAdjustment.effective_date.desc())
        .all()
    )
    
    rt_dict = RoomTypeDetailResponse.model_validate(room_type).model_dump()
    rt_dict["effective_rate"] = effective_rate
    rt_dict["current_adjustment"] = current_adjustment
    rt_dict["rate_adjustments"] = [
        RateAdjustmentResponse.model_validate(adj).model_dump() for adj in adjustments
    ]
    
    return RoomTypeDetailResponse(**rt_dict)


@router.post("", response_model=RoomTypeResponse, status_code=status.HTTP_201_CREATED)
def create_room_type(
    room_type: RoomTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_room_type = RoomType(**room_type.model_dump())
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    
    effective_rate, current_adjustment = calculate_effective_rate(db_room_type)
    rt_dict = RoomTypeResponse.model_validate(db_room_type).model_dump()
    rt_dict["effective_rate"] = effective_rate
    rt_dict["current_adjustment"] = current_adjustment
    
    return RoomTypeResponse(**rt_dict)


@router.put("/{room_type_id}", response_model=RoomTypeResponse)
def update_room_type(
    room_type_id: int,
    room_type: RoomTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not db_room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    
    update_data = room_type.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_room_type, field, value)
    
    db.commit()
    db.refresh(db_room_type)
    
    effective_rate, current_adjustment = calculate_effective_rate(db_room_type)
    rt_dict = RoomTypeResponse.model_validate(db_room_type).model_dump()
    rt_dict["effective_rate"] = effective_rate
    rt_dict["current_adjustment"] = current_adjustment
    
    return RoomTypeResponse(**rt_dict)


@router.delete("/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not db_room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    
    db.delete(db_room_type)
    db.commit()
    return None


@router.post("/{room_type_id}/adjustments", response_model=RateAdjustmentResponse, status_code=status.HTTP_201_CREATED)
def create_rate_adjustment(
    room_type_id: int,
    adjustment: RateAdjustmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify room type exists
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    
    # Override room_type_id with path parameter
    adjustment_data = adjustment.model_dump()
    adjustment_data["room_type_id"] = room_type_id
    
    db_adjustment = RateAdjustment(**adjustment_data)
    db.add(db_adjustment)
    db.commit()
    db.refresh(db_adjustment)
    
    return db_adjustment


@router.get("/{room_type_id}/adjustments", response_model=List[RateAdjustmentResponse])
def list_rate_adjustments(
    room_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    adjustments = (
        db.query(RateAdjustment)
        .filter(RateAdjustment.room_type_id == room_type_id)
        .order_by(RateAdjustment.effective_date.desc())
        .all()
    )
    return adjustments