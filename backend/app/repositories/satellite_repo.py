from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.satellite import SatelliteData


class SatelliteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SatelliteData) -> SatelliteData:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def get_by_farm(self, farm_id: str, limit: int = 50) -> List[SatelliteData]:
        return self.db.query(SatelliteData).filter(
            SatelliteData.farm_id == farm_id
        ).order_by(SatelliteData.acquisition_date.desc()).limit(limit).all()

    def get_latest_by_farm(self, farm_id: str) -> Optional[SatelliteData]:
        return self.db.query(SatelliteData).filter(
            SatelliteData.farm_id == farm_id
        ).order_by(SatelliteData.acquisition_date.desc()).first()

    def get_ndvi_timeseries(self, farm_id: str) -> List[dict]:
        results = self.db.query(SatelliteData).filter(
            SatelliteData.farm_id == farm_id,
            SatelliteData.ndvi_value.isnot(None)
        ).order_by(SatelliteData.acquisition_date.asc()).all()
        return [{"date": r.acquisition_date, "ndvi": r.ndvi_value} for r in results]
