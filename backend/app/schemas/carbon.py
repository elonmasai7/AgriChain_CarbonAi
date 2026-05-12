from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CarbonScoreResponse(BaseModel):
    id: str
    farm_id: str
    farmer_id: str
    carbon_offset_tonnes: float
    sustainability_score: Optional[float]
    environmental_health_score: Optional[float]
    ai_confidence_level: Optional[float]
    ndvi_avg: Optional[float]
    biomass_estimate: Optional[float]
    soil_carbon_estimate: Optional[float]
    methodology_version: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CarbonEstimateRequest(BaseModel):
    farm_id: str
    force_recalculate: bool = False


class CarbonAnalysisResponse(BaseModel):
    score: CarbonScoreResponse
    recommendations: List[str]
    fraud_risk: Optional[float]


class SustainabilityReportResponse(BaseModel):
    id: str
    farm_id: str
    report_type: str
    recommendations: Optional[str]
    generated_at: datetime

    class Config:
        from_attributes = True
