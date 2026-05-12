from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.schemas.carbon import CarbonEstimateRequest, CarbonScoreResponse, CarbonAnalysisResponse, SustainabilityReportResponse
from app.services.carbon_service import CarbonService
from app.models.user import User

router = APIRouter(prefix="/api/carbon", tags=["Carbon"])


@router.post("/estimate", response_model=CarbonScoreResponse)
def estimate_carbon(data: CarbonEstimateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = CarbonService(db)
    return service.estimate_carbon(data.farm_id, data.force_recalculate)


@router.get("/scores/{score_id}", response_model=CarbonScoreResponse)
def get_score(score_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CarbonService(db)
    return service.get_carbon_score(score_id)


@router.get("/farms/{farm_id}")
def get_farm_scores(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CarbonService(db)
    return service.get_farm_scores(farm_id)


@router.get("/my-scores", response_model=list[CarbonScoreResponse])
def get_my_scores(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = CarbonService(db)
    return service.get_farmer_scores(str(current_user.id))


@router.get("/pending", dependencies=[Depends(require_role("auditor", "admin"))])
def get_pending_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CarbonService(db)
    return service.get_pending_reviews()


@router.post("/review/{score_id}/{status}", dependencies=[Depends(require_role("auditor", "admin"))])
def review_score(score_id: str, status: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = CarbonService(db)
    return service.review_score(score_id, status, str(current_user.id))


@router.get("/total")
def get_total_carbon(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = CarbonService(db)
    total = service.get_total_carbon(str(current_user.id))
    return {"total_carbon_tonnes": total}


@router.post("/report/{farm_id}")
def generate_report(farm_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = CarbonService(db)
    return service.generate_report(farm_id)


@router.get("/reports/{farm_id}")
def get_reports(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CarbonService(db)
    return service.get_farm_reports(farm_id)
