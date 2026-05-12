import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Float, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class BlockchainTransaction(Base):
    __tablename__ = "blockchain_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_hash = Column(String(255), unique=True, index=True)
    contract_address = Column(String(255))
    function_name = Column(String(100))
    args = Column(Text)
    block_number = Column(Integer)
    status = Column(String(50))
    gas_used = Column(Integer)
    chain = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CarbonAsset(Base):
    __tablename__ = "carbon_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = Column(Integer, unique=True)
    farm_id = Column(UUID(as_uuid=True), nullable=False)
    carbon_score_id = Column(UUID(as_uuid=True), nullable=False)
    owner_address = Column(String(255))
    certificate_uri = Column(String(500))
    carbon_tonnes = Column(Float)
    chain = Column(String(50))
    contract_address = Column(String(255))
    mint_tx_hash = Column(String(255))
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
