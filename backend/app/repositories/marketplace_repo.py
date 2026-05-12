from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List

from app.models.marketplace import MarketplaceListing, CarbonPurchase


class MarketplaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_listing(self, listing: MarketplaceListing) -> MarketplaceListing:
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    def get_listing_by_id(self, listing_id: str) -> Optional[MarketplaceListing]:
        return self.db.query(MarketplaceListing).filter(MarketplaceListing.id == listing_id).first()

    def list_active_listings(self, skip: int = 0, limit: int = 50, filters: dict = None) -> List[MarketplaceListing]:
        query = self.db.query(MarketplaceListing).filter(MarketplaceListing.status == "active")
        if filters:
            if filters.get("min_tonnes"):
                query = query.filter(MarketplaceListing.available_tonnes >= filters["min_tonnes"])
            if filters.get("max_price"):
                query = query.filter(MarketplaceListing.price_per_tonne <= filters["max_price"])
            if filters.get("min_esg_score"):
                query = query.filter(MarketplaceListing.esg_score >= filters["min_esg_score"])
            if filters.get("verified_only"):
                query = query.filter(MarketplaceListing.verification_badge == True)
        sort_by = getattr(MarketplaceListing, filters.get("sort_by", "created_at"), MarketplaceListing.created_at)
        if filters.get("sort_order", "desc") == "desc":
            query = query.order_by(desc(sort_by))
        else:
            query = query.order_by(sort_by)
        return query.offset(skip).limit(limit).all()

    def count_active(self) -> int:
        return self.db.query(MarketplaceListing).filter(MarketplaceListing.status == "active").count()

    def update_listing(self, listing_id: str, data: dict) -> Optional[MarketplaceListing]:
        self.db.query(MarketplaceListing).filter(MarketplaceListing.id == listing_id).update(data)
        self.db.commit()
        return self.get_listing_by_id(listing_id)

    def get_by_seller(self, seller_id: str) -> List[MarketplaceListing]:
        return self.db.query(MarketplaceListing).filter(MarketplaceListing.seller_id == seller_id).all()


class PurchaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, purchase: CarbonPurchase) -> CarbonPurchase:
        self.db.add(purchase)
        self.db.commit()
        self.db.refresh(purchase)
        return purchase

    def get_by_id(self, purchase_id: str) -> Optional[CarbonPurchase]:
        return self.db.query(CarbonPurchase).filter(CarbonPurchase.id == purchase_id).first()

    def get_by_buyer(self, buyer_id: str) -> List[CarbonPurchase]:
        return self.db.query(CarbonPurchase).filter(CarbonPurchase.buyer_id == buyer_id).order_by(desc(CarbonPurchase.created_at)).all()

    def get_by_listing(self, listing_id: str) -> List[CarbonPurchase]:
        return self.db.query(CarbonPurchase).filter(CarbonPurchase.listing_id == listing_id).all()

    def retire_purchase(self, purchase_id: str) -> Optional[CarbonPurchase]:
        from datetime import datetime, timezone
        data = {"is_retired": True, "retired_at": datetime.now(timezone.utc)}
        self.db.query(CarbonPurchase).filter(CarbonPurchase.id == purchase_id).update(data)
        self.db.commit()
        return self.get_by_id(purchase_id)
