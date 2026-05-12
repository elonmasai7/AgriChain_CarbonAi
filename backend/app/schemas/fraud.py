from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FraudAlertResponse(BaseModel):
    id: str
    farm_id: str
    alert_type: str
    severity: str
    fraud_score: float
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FraudAlertUpdate(BaseModel):
    status: str
    assigned_auditor_id: Optional[str] = None


class FraudAnalysisRequest(BaseModel):
    farm_id: str


class FraudAnalysisResponse(BaseModel):
    fraud_score: float
    risk_level: str
    alerts: List[FraudAlertResponse]
    details: dict
