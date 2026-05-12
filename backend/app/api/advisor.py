from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.advisor import AdvisorMessageRequest, AdvisorMessageResponse, AdvisorRecommendationResponse
from app.services.advisor_service import AdvisorService
from app.models.user import User

router = APIRouter(prefix="/api/advisor", tags=["Advisor"])


@router.post("/chat")
def chat(data: AdvisorMessageRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AdvisorService(db)
    return service.chat(str(current_user.id), data.content, data.language)


@router.get("/history")
def get_chat_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AdvisorService(db)
    return service.get_history(str(current_user.id))


@router.get("/recommendations/{farm_id}")
def get_recommendations(farm_id: str, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    service = AdvisorService(db)
    return service.get_recommendations(farm_id, str(current_user.id))
