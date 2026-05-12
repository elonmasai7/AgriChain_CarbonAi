import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class AdvisorMessage(Base):
    __tablename__ = "advisor_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    role = Column(String(20))
    content = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    message_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AdvisorRecommendation(Base):
    __tablename__ = "advisor_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    recommendation_type = Column(String(100))
    title = Column(String(255))
    description = Column(Text)
    priority = Column(String(50))
    category = Column(String(100))
    is_read = Column(Text, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
