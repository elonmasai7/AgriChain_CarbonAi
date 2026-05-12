from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.schemas.fraud import FraudAnalysisRequest, FraudAnalysisResponse, FraudAlertUpdate
from app.services.fraud_service import FraudService
from app.models.user import User

router = APIRouter(prefix="/api/fraud", tags=["Fraud Detection"])


@router.post("/analyze/{farm_id}")
def analyze_farm(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FraudService(db)
    return service.analyze_farm(farm_id)


@router.get("/alerts", dependencies=[Depends(require_role("auditor", "admin"))])
def get_alerts(status: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FraudService(db)
    return service.get_alerts(status)


@router.get("/alerts/{farm_id}")
def get_farm_alerts(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FraudService(db)
    return service.get_farm_alerts(farm_id)


@router.patch("/alerts/{alert_id}", dependencies=[Depends(require_role("auditor", "admin"))])
def update_alert(alert_id: str, data: FraudAlertUpdate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    service = FraudService(db)
    return service.update_alert(alert_id, data.model_dump(exclude_unset=True))
