from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SatelliteDataResponse(BaseModel):
    id: str
    farm_id: str
    source: Optional[str]
    ndvi_value: Optional[float]
    evi_value: Optional[float]
    land_health_score: Optional[float]
    water_stress_index: Optional[float]
    vegetation_fraction: Optional[float]
    acquisition_date: Optional[datetime]
    processing_date: datetime

    class Config:
        from_attributes = True


class SatelliteAnalysisResponse(BaseModel):
    farm_id: str
    ndvi_current: Optional[float]
    ndvi_change: Optional[float]
    land_health: Optional[float]
    vegetation_trend: str
    water_stress: Optional[float]
    analysis_date: datetime
    historical_data: List[SatelliteDataResponse]
