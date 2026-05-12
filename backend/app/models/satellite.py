import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class SatelliteData(Base):
    __tablename__ = "satellite_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    source = Column(String(100))
    image_url = Column(String(500))
    ndvi_value = Column(Float)
    evi_value = Column(Float)
    land_health_score = Column(Float)
    water_stress_index = Column(Float)
    vegetation_fraction = Column(Float)
    acquisition_date = Column(DateTime(timezone=True))
    processing_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    raw_metadata = Column(Text)

    farm = relationship("Farm", back_populates="satellite_data")
