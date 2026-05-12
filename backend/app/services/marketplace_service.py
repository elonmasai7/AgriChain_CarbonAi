import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.marketplace import MarketplaceListing, CarbonPurchase
from app.repositories.marketplace_repo import MarketplaceRepository, PurchaseRepository
from app.repositories.carbon_repo import CarbonScoreRepository
from app.repositories.farm_repo import FarmRepository
from app.services.blockchain_service import BlockchainService
from app.schemas.marketplace import ListingCreate, PurchaseRequest, MarketplaceFilter


class MarketplaceService:
    def __init__(self, db: Session):
        self.repo = MarketplaceRepository(db)
        self.purchase_repo = PurchaseRepository(db)
        self.carbon_repo = CarbonScoreRepository(db)
        self.farm_repo = FarmRepository(db)
        self.blockchain = BlockchainService()

    def create_listing(self, seller_id: str, data: ListingCreate) -> MarketplaceListing:
        score = self.carbon_repo.get_by_id(data.carbon_asset_id)
        if not score:
            raise HTTPException(status_code=404, detail="Carbon asset not found")
        if str(score.farmer_id) != seller_id:
            raise HTTPException(status_code=403, detail="Not your carbon asset")

        farm = self.farm_repo.get_by_id(score.farm_id)

        listing = MarketplaceListing(
            farm_id=score.farm_id,
            carbon_asset_id=data.carbon_asset_id,
            seller_id=seller_id,
            price_per_tonne=data.price_per_tonne,
            total_tonnes=min(data.total_tonnes, score.carbon_offset_tonnes),
            available_tonnes=min(data.total_tonnes, score.carbon_offset_tonnes),
            currency=data.currency,
            esg_score=score.sustainability_score,
            verification_badge=farm.is_verified if farm else False,
            description=data.description,
        )
        return self.repo.create_listing(listing)

    def get_listing(self, listing_id: str) -> dict:
        listing = self.repo.get_listing_by_id(listing_id)
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        farm = self.farm_repo.get_by_id(listing.farm_id)
        result = {
            "id": str(listing.id),
            "farm_id": str(listing.farm_id),
            "carbon_asset_id": str(listing.carbon_asset_id),
            "seller_id": str(listing.seller_id),
            "price_per_tonne": listing.price_per_tonne,
            "total_tonnes": listing.total_tonnes,
            "available_tonnes": listing.available_tonnes,
            "currency": listing.currency,
            "status": listing.status,
            "esg_score": listing.esg_score,
            "verification_badge": listing.verification_badge,
            "farm_name": farm.name if farm else None,
            "description": listing.description,
            "created_at": listing.created_at,
        }
        return result

    def list_active(self, filters: MarketplaceFilter) -> dict:
        skip = (filters.page - 1) * filters.per_page
        listings = self.repo.list_active_listings(skip, filters.per_page, filters.model_dump(exclude_none=True))
        total = self.repo.count_active()
        farm_ids = {l.farm_id for l in listings}
        farms = {str(f.id): f for f in [self.farm_repo.get_by_id(fid) for fid in farm_ids] if f}

        result = []
        for l in listings:
            farm = farms.get(str(l.farm_id))
            result.append({
                "id": str(l.id),
                "farm_id": str(l.farm_id),
                "carbon_asset_id": str(l.carbon_asset_id),
                "seller_id": str(l.seller_id),
                "price_per_tonne": l.price_per_tonne,
                "total_tonnes": l.total_tonnes,
                "available_tonnes": l.available_tonnes,
                "currency": l.currency,
                "status": l.status,
                "esg_score": l.esg_score,
                "verification_badge": l.verification_badge,
                "farm_name": farm.name if farm else None,
                "description": l.description,
                "created_at": l.created_at,
            })

        return {"listings": result, "total": total, "page": filters.page, "per_page": filters.per_page}

    def purchase(self, buyer_id: str, data: PurchaseRequest) -> CarbonPurchase:
        listing = self.repo.get_listing_by_id(data.listing_id)
        if not listing or listing.status != "active":
            raise HTTPException(status_code=404, detail="Listing not available")
        if data.tonnes > listing.available_tonnes:
            raise HTTPException(status_code=400, detail="Not enough tonnes available")

        total_price = listing.price_per_tonne * data.tonnes

        purchase = CarbonPurchase(
            listing_id=data.listing_id,
            buyer_id=buyer_id,
            tonnes_purchased=data.tonnes,
            total_price=total_price,
            currency=listing.currency,
        )

        tx = self.blockchain.record_purchase(
            str(purchase.id), str(buyer_id), str(listing.seller_id), data.tonnes, total_price
        )
        purchase.transaction_hash = tx["transaction_hash"]
        purchase.status = "completed"
        purchase = self.purchase_repo.create(purchase)

        new_available = listing.available_tonnes - data.tonnes
        new_status = "sold_out" if new_available <= 0 else "active"
        self.repo.update_listing(data.listing_id, {"available_tonnes": new_available, "status": new_status})

        return purchase

    def retire_asset(self, purchase_id: str) -> CarbonPurchase:
        purchase = self.purchase_repo.get_by_id(purchase_id)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        if purchase.is_retired:
            raise HTTPException(status_code=400, detail="Already retired")
        return self.purchase_repo.retire_purchase(purchase_id)

    def get_buyer_purchases(self, buyer_id: str) -> list:
        return self.purchase_repo.get_by_buyer(buyer_id)

    def get_seller_listings(self, seller_id: str) -> list:
        return self.repo.get_by_seller(seller_id)
