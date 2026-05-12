import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, Enum as SAEnum, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    AUDITOR = "auditor"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.FARMER)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    phone = Column(String(50))
    country = Column(String(100))
    wallet_address = Column(String(255))
    profile_image = Column(String(500))
    preferred_language = Column(String(10), default="en")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farms = relationship("Farm", back_populates="farmer")
    carbon_scores = relationship("CarbonScore", back_populates="farmer")
