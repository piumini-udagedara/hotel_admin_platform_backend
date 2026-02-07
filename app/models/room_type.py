from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    base_rate = Column(Float, nullable=False)
    capacity = Column(Integer, default=2)

    # Relationships
    hotel = relationship("Hotel", back_populates="room_types")
    rate_adjustments = relationship("RateAdjustment", back_populates="room_type", cascade="all, delete-orphan")