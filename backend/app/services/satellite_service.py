import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional

from app.models.satellite import SatelliteData
from app.repositories.satellite_repo import SatelliteRepository
from app.repositories.farm_repo import FarmRepository


class SatelliteService:
    def __init__(self, db: Session):
        self.repo = SatelliteRepository(db)
        self.farm_repo = FarmRepository(db)

    def analyze_farm(self, farm_id: str) -> dict:
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")

        latest = self.repo.get_latest_by_farm(farm_id)
        historical = self.repo.get_by_farm(farm_id)
        ndvi_series = self.repo.get_ndvi_timeseries(farm_id)

        ndvi_change = None
        vegetation_trend = "stable"
        if len(ndvi_series) >= 2:
            ndvi_change = ndvi_series[-1]["ndvi"] - ndvi_series[0]["ndvi"]
            if ndvi_change and ndvi_change > 0.1:
                vegetation_trend = "improving"
            elif ndvi_change and ndvi_change < -0.1:
                vegetation_trend = "degrading"

        if not latest:
            sat_data = self._fetch_satellite_data(farm.latitude, farm.longitude)
            latest = self.repo.create(sat_data)
            historical = [latest]

        return {
            "farm_id": farm_id,
            "ndvi_current": latest.ndvi_value,
            "ndvi_change": ndvi_change,
            "land_health": latest.land_health_score,
            "vegetation_trend": vegetation_trend,
            "water_stress": latest.water_stress_index,
            "analysis_date": datetime.now(timezone.utc),
            "historical_data": historical,
        }

    def _fetch_satellite_data(self, lat: float, lon: float) -> SatelliteData:
        import random
        import math
        base_ndvi = 0.3 + 0.5 * abs(math.sin(lat) * math.cos(lon))
        return SatelliteData(
            id=uuid.uuid4(),
            farm_id=None,
            source="simulation",
            ndvi_value=round(base_ndvi + random.uniform(-0.1, 0.1), 4),
            evi_value=round(base_ndvi * 1.2 + random.uniform(-0.1, 0.1), 4),
            land_health_score=round(50 + random.uniform(-10, 30), 2),
            water_stress_index=round(random.uniform(0, 0.8), 4),
            vegetation_fraction=round(base_ndvi * random.uniform(0.8, 1.2), 4),
            acquisition_date=datetime.now(timezone.utc),
        )

    def get_ndvi_timeseries(self, farm_id: str) -> list:
        return self.repo.get_ndvi_timeseries(farm_id)

    def add_satellite_data(self, farm_id: str, data: dict) -> SatelliteData:
        sat = SatelliteData(
            farm_id=farm_id,
            source=data.get("source", "api"),
            image_url=data.get("image_url"),
            ndvi_value=data.get("ndvi_value"),
            evi_value=data.get("evi_value"),
            land_health_score=data.get("land_health_score"),
            water_stress_index=data.get("water_stress_index"),
            vegetation_fraction=data.get("vegetation_fraction"),
            acquisition_date=data.get("acquisition_date", datetime.now(timezone.utc)),
        )
        return self.repo.create(sat)
