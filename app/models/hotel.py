from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    description = Column(Text)
    status = Column(String, default="active")  # Added in second migration

    # Relationships
    room_types = relationship("RoomType", back_populates="hotel", cascade="all, delete-orphan")