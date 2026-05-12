from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FarmCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    country: str = Field(min_length=1, max_length=100)
    region: Optional[str] = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    area_hectares: float = Field(gt=0)
    crop_types: Optional[str] = None
    irrigation_type: Optional[str] = None
    fertilizer_usage: Optional[str] = None
    soil_type: Optional[str] = None
    sustainability_practices: Optional[str] = None


class FarmUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    crop_types: Optional[str] = None
    irrigation_type: Optional[str] = None
    fertilizer_usage: Optional[str] = None
    sustainability_practices: Optional[str] = None


class FarmResponse(BaseModel):
    id: str
    farmer_id: str
    name: str
    description: Optional[str]
    country: str
    region: Optional[str]
    latitude: float
    longitude: float
    area_hectares: float
    crop_types: Optional[str]
    irrigation_type: Optional[str]
    fertilizer_usage: Optional[str]
    soil_type: Optional[str]
    sustainability_practices: Optional[str]
    is_verified: bool
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FarmListResponse(BaseModel):
    farms: List[FarmResponse]
    total: int
    page: int
    per_page: int
