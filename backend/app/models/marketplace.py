import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Float, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class MarketplaceListing(Base):
    __tablename__ = "marketplace_listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    carbon_asset_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    seller_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    price_per_tonne = Column(Float, nullable=False)
    total_tonnes = Column(Float, nullable=False)
    available_tonnes = Column(Float, nullable=False)
    currency = Column(String(10), default="USDC")
    status = Column(String(50), default="active")
    esg_score = Column(Float)
    verification_badge = Column(Boolean, default=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="listings")


class CarbonPurchase(Base):
    __tablename__ = "carbon_purchases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    tonnes_purchased = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    currency = Column(String(10))
    transaction_hash = Column(String(255))
    status = Column(String(50), default="pending")
    is_retired = Column(Boolean, default=False)
    retired_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
