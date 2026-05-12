from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ListingCreate(BaseModel):
    carbon_asset_id: str
    price_per_tonne: float = Field(gt=0)
    total_tonnes: float = Field(gt=0)
    currency: str = "USDC"
    description: Optional[str] = None


class ListingUpdate(BaseModel):
    price_per_tonne: Optional[float] = None
    status: Optional[str] = None


class ListingResponse(BaseModel):
    id: str
    farm_id: str
    carbon_asset_id: str
    seller_id: str
    price_per_tonne: float
    total_tonnes: float
    available_tonnes: float
    currency: str
    status: str
    esg_score: Optional[float]
    verification_badge: bool
    description: Optional[str]
    farm_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PurchaseRequest(BaseModel):
    listing_id: str
    tonnes: float = Field(gt=0)


class PurchaseResponse(BaseModel):
    id: str
    listing_id: str
    buyer_id: str
    tonnes_purchased: float
    total_price: float
    currency: str
    transaction_hash: Optional[str]
    status: str
    is_retired: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MarketplaceFilter(BaseModel):
    min_tonnes: Optional[float] = None
    max_price: Optional[float] = None
    min_esg_score: Optional[float] = None
    verified_only: bool = False
    country: Optional[str] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
    page: int = 1
    per_page: int = 20
