import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Float, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    alert_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    fraud_score = Column(Float, nullable=False)
    description = Column(Text)
    evidence = Column(Text)
    status = Column(String(50), default="open")
    assigned_auditor_id = Column(UUID(as_uuid=True))
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(100))
    entity_id = Column(UUID(as_uuid=True))
    action = Column(String(100))
    performed_by = Column(UUID(as_uuid=True))
    details = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
