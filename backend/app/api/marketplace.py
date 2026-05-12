from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.marketplace import ListingCreate, ListingResponse, PurchaseRequest, PurchaseResponse, MarketplaceFilter
from app.services.marketplace_service import MarketplaceService
from app.models.user import User

router = APIRouter(prefix="/api/marketplace", tags=["Marketplace"])


@router.post("/listings")
def create_listing(data: ListingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MarketplaceService(db)
    listing = service.create_listing(str(current_user.id), data)
    return listing


@router.get("/listings")
def list_listings(
    min_tonnes: float = None, max_price: float = None, min_esg_score: float = None,
    verified_only: bool = False, country: str = None, sort_by: str = "created_at",
    sort_order: str = "desc", page: int = 1, per_page: int = 20,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    service = MarketplaceService(db)
    filters = MarketplaceFilter(
        min_tonnes=min_tonnes, max_price=max_price, min_esg_score=min_esg_score,
        verified_only=verified_only, country=country, sort_by=sort_by,
        sort_order=sort_order, page=page, per_page=per_page,
    )
    return service.list_active(filters)


@router.get("/listings/{listing_id}")
def get_listing(listing_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = MarketplaceService(db)
    return service.get_listing(listing_id)


@router.post("/purchase")
def purchase_carbon(data: PurchaseRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MarketplaceService(db)
    return service.purchase(str(current_user.id), data)


@router.post("/retire/{purchase_id}")
def retire_asset(purchase_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MarketplaceService(db)
    return service.retire_asset(purchase_id)


@router.get("/purchases")
def get_purchases(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MarketplaceService(db)
    return service.get_buyer_purchases(str(current_user.id))


@router.get("/my-listings")
def get_my_listings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MarketplaceService(db)
    return service.get_seller_listings(str(current_user.id))
