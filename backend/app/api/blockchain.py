from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.blockchain_service import BlockchainService
from app.models.user import User

router = APIRouter(prefix="/api/blockchain", tags=["Blockchain"])


@router.post("/mint/{score_id}")
def mint_carbon_asset(score_id: str, chain: str = "polygon",
                      current_user: User = Depends(get_current_user)):
    service = BlockchainService()
    result = service.mint_carbon_asset(score_id, current_user.wallet_address or "0x0000000000000000000000000000000000000000", chain)
    return result


@router.get("/verify/{tx_hash}")
def verify_transaction(tx_hash: str):
    service = BlockchainService()
    return service.verify_transaction(tx_hash)


@router.get("/certificate/{token_id}")
def get_certificate(token_id: int):
    service = BlockchainService()
    return service.get_certificate_metadata(token_id)
