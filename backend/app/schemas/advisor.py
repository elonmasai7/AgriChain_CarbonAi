from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AdvisorMessageRequest(BaseModel):
    content: str
    language: str = "en"


class AdvisorMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    language: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdvisorRecommendationResponse(BaseModel):
    id: str
    farm_id: str
    recommendation_type: str
    title: str
    description: str
    priority: str
    category: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
