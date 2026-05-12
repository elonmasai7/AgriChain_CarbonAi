import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    country = Column(String(100), nullable=False)
    region = Column(String(200))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    area_hectares = Column(Float, nullable=False)
    crop_types = Column(Text)
    irrigation_type = Column(String(100))
    fertilizer_usage = Column(String(200))
    soil_type = Column(String(100))
    sustainability_practices = Column(Text)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime(timezone=True))
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farmer = relationship("User", back_populates="farms")
    carbon_scores = relationship("CarbonScore", back_populates="farm")
    satellite_data = relationship("SatelliteData", back_populates="farm")
    images = relationship("FarmImage", back_populates="farm")
    listings = relationship("MarketplaceListing", back_populates="farm")


class FarmImage(Base):
    __tablename__ = "farm_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    image_type = Column(String(50))
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="images")
