from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.services.auth_service import AuthService
from app.services.farm_service import FarmService
from app.services.carbon_service import CarbonService
from app.services.fraud_service import FraudService
from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["Administration"])


@router.get("/dashboard", dependencies=[Depends(require_role("admin"))])
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    auth_service = AuthService(db)
    farm_service = FarmService(db)
    carbon_service = CarbonService(db)
    fraud_service = FraudService(db)

    return {
        "total_farmers": auth_service.get_user_count_by_role("farmer"),
        "total_buyers": auth_service.get_user_count_by_role("buyer"),
        "total_farms": len(farm_service.get_all_farms()),
        "pending_verifications": len(farm_service.list_pending()),
        "pending_carbon_reviews": len(carbon_service.get_pending_reviews()),
        "open_fraud_alerts": len(fraud_service.get_alerts("open")),
        "platform_status": "operational",
    }


@router.get("/audit-logs", dependencies=[Depends(require_role("admin"))])
def get_audit_logs(entity_type: str = None, entity_id: str = None,
                   db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if entity_type and entity_id:
        service = FraudService(db)
        return service.get_audit_logs(entity_type, entity_id)
    return []


@router.get("/farms/pending", dependencies=[Depends(require_role("admin", "auditor"))])
def get_pending_farms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FarmService(db)
    return service.list_pending()


@router.post("/farms/{farm_id}/verify", dependencies=[Depends(require_role("admin", "auditor"))])
def verify_farm(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FarmService(db)
    return service.verify_farm(farm_id)


@router.get("/blockchain/transactions", dependencies=[Depends(require_role("admin"))])
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from app.repositories.carbon_repo import CarbonScoreRepository
    from app.models.blockchain import BlockchainTransaction
    return db.query(BlockchainTransaction).order_by(BlockchainTransaction.created_at.desc()).limit(50).all()
