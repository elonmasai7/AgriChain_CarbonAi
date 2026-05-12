import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.farm import Farm, FarmImage
from app.repositories.farm_repo import FarmRepository, FarmImageRepository
from app.schemas.farm import FarmCreate, FarmUpdate


class FarmService:
    def __init__(self, db: Session):
        self.repo = FarmRepository(db)
        self.image_repo = FarmImageRepository(db)

    def create_farm(self, farmer_id: str, data: FarmCreate) -> Farm:
        farm = Farm(
            farmer_id=farmer_id,
            name=data.name,
            description=data.description,
            country=data.country,
            region=data.region,
            latitude=data.latitude,
            longitude=data.longitude,
            area_hectares=data.area_hectares,
            crop_types=data.crop_types,
            irrigation_type=data.irrigation_type,
            fertilizer_usage=data.fertilizer_usage,
            soil_type=data.soil_type,
            sustainability_practices=data.sustainability_practices,
        )
        return self.repo.create(farm)

    def get_farm(self, farm_id: str) -> Farm:
        farm = self.repo.get_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")
        return farm

    def get_farmer_farms(self, farmer_id: str) -> list:
        return self.repo.get_by_farmer(farmer_id)

    def update_farm(self, farm_id: str, farmer_id: str, data: FarmUpdate) -> Farm:
        farm = self.repo.get_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")
        if str(farm.farmer_id) != farmer_id:
            raise HTTPException(status_code=403, detail="Not your farm")
        return self.repo.update(farm_id, data.model_dump(exclude_unset=True))

    def add_image(self, farm_id: str, image_url: str, image_type: str = None) -> FarmImage:
        image = FarmImage(farm_id=farm_id, image_url=image_url, image_type=image_type)
        return self.image_repo.create(image)

    def get_farm_images(self, farm_id: str) -> list:
        return self.image_repo.get_by_farm(farm_id)

    def list_pending(self) -> list:
        return self.repo.list_pending_verification()

    def verify_farm(self, farm_id: str) -> Farm:
        from datetime import datetime, timezone
        return self.repo.update(farm_id, {"is_verified": True, "status": "verified", "verification_date": datetime.now(timezone.utc)})

    def get_all_farms(self, skip: int = 0, limit: int = 100, verified: bool = None) -> list:
        return self.repo.list_all(skip, limit, verified)

    def get_farm_count_by_farmer(self, farmer_id: str) -> int:
        return self.repo.count_by_farmer(farmer_id)
