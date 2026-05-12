from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.schemas.farm import FarmCreate, FarmUpdate, FarmResponse, FarmListResponse
from app.services.farm_service import FarmService
from app.models.user import User

router = APIRouter(prefix="/api/farms", tags=["Farms"])


@router.post("", response_model=FarmResponse)
def create_farm(data: FarmCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = FarmService(db)
    farm = service.create_farm(str(current_user.id), data)
    return farm


@router.get("", response_model=FarmListResponse)
def list_farms(page: int = 1, per_page: int = 20, verified: Optional[bool] = None,
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = FarmService(db)
    skip = (page - 1) * per_page

    if current_user.role.value == "farmer":
        farms = service.get_farmer_farms(str(current_user.id))
        total = len(farms)
        farms = farms[skip:skip + per_page]
    else:
        farms = service.get_all_farms(skip, per_page, verified)
        total = len(farms)

    return FarmListResponse(farms=farms, total=total, page=page, per_page=per_page)


@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FarmService(db)
    return service.get_farm(farm_id)


@router.patch("/{farm_id}", response_model=FarmResponse)
def update_farm(farm_id: str, data: FarmUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = FarmService(db)
    return service.update_farm(farm_id, str(current_user.id), data)


@router.post("/{farm_id}/images")
def upload_image(farm_id: str, file: UploadFile = File(...), image_type: str = Form(None),
                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = FarmService(db)
    contents = file.file.read()
    import os
    from app.core.config import settings
    upload_dir = os.path.join(settings.UPLOAD_DIR, farm_id)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    image = service.add_image(farm_id, file_path, image_type)
    return {"id": str(image.id), "url": file_path, "type": image_type}


@router.get("/{farm_id}/images")
def get_farm_images(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FarmService(db)
    return service.get_farm_images(farm_id)
