from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.satellite_service import SatelliteService
from app.models.user import User

router = APIRouter(prefix="/api/satellite", tags=["Satellite"])


@router.get("/analyze/{farm_id}")
def analyze_farm(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SatelliteService(db)
    return service.analyze_farm(farm_id)


@router.get("/ndvi/{farm_id}")
def get_ndvi_timeseries(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SatelliteService(db)
    return service.get_ndvi_timeseries(farm_id)


@router.post("/data/{farm_id}")
def add_satellite_data(farm_id: str, data: dict, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    service = SatelliteService(db)
    return service.add_satellite_data(farm_id, data)
