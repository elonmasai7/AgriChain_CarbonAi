import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Float, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class CarbonScore(Base):
    __tablename__ = "carbon_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id"), nullable=False, index=True)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    carbon_offset_tonnes = Column(Float, nullable=False)
    sustainability_score = Column(Float)
    environmental_health_score = Column(Float)
    ai_confidence_level = Column(Float)
    ndvi_avg = Column(Float)
    biomass_estimate = Column(Float)
    soil_carbon_estimate = Column(Float)
    methodology_version = Column(String(50))
    input_parameters = Column(Text)
    raw_ai_output = Column(Text)
    status = Column(String(50), default="pending")
    reviewed_by = Column(UUID(as_uuid=True))
    reviewed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="carbon_scores")
    farmer = relationship("User", back_populates="carbon_scores")


class SustainabilityReport(Base):
    __tablename__ = "sustainability_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    report_type = Column(String(100))
    report_data = Column(Text)
    recommendations = Column(Text)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
