from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.farm import Farm, FarmImage


class FarmRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, farm: Farm) -> Farm:
        self.db.add(farm)
        self.db.commit()
        self.db.refresh(farm)
        return farm

    def get_by_id(self, farm_id: str) -> Optional[Farm]:
        return self.db.query(Farm).filter(Farm.id == farm_id).first()

    def get_by_farmer(self, farmer_id: str, skip: int = 0, limit: int = 100) -> List[Farm]:
        return self.db.query(Farm).filter(Farm.farmer_id == farmer_id).offset(skip).limit(limit).all()

    def update(self, farm_id: str, data: dict) -> Optional[Farm]:
        self.db.query(Farm).filter(Farm.id == farm_id).update(data)
        self.db.commit()
        return self.get_by_id(farm_id)

    def delete(self, farm_id: str) -> bool:
        result = self.db.query(Farm).filter(Farm.id == farm_id).delete()
        self.db.commit()
        return result > 0

    def count_by_farmer(self, farmer_id: str) -> int:
        return self.db.query(Farm).filter(Farm.farmer_id == farmer_id).count()

    def list_all(self, skip: int = 0, limit: int = 100, verified: Optional[bool] = None) -> List[Farm]:
        query = self.db.query(Farm)
        if verified is not None:
            query = query.filter(Farm.is_verified == verified)
        return query.offset(skip).limit(limit).all()

    def list_pending_verification(self, skip: int = 0, limit: int = 100) -> List[Farm]:
        return self.db.query(Farm).filter(Farm.status == "pending").offset(skip).limit(limit).all()


class FarmImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, image: FarmImage) -> FarmImage:
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def get_by_farm(self, farm_id: str) -> List[FarmImage]:
        return self.db.query(FarmImage).filter(FarmImage.farm_id == farm_id).all()
