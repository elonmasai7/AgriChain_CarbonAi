from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.carbon import CarbonScore, SustainabilityReport


class CarbonScoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, score: CarbonScore) -> CarbonScore:
        self.db.add(score)
        self.db.commit()
        self.db.refresh(score)
        return score

    def get_by_id(self, score_id: str) -> Optional[CarbonScore]:
        return self.db.query(CarbonScore).filter(CarbonScore.id == score_id).first()

    def get_by_farm(self, farm_id: str) -> List[CarbonScore]:
        return self.db.query(CarbonScore).filter(CarbonScore.farm_id == farm_id).order_by(CarbonScore.created_at.desc()).all()

    def get_latest_by_farm(self, farm_id: str) -> Optional[CarbonScore]:
        return self.db.query(CarbonScore).filter(CarbonScore.farm_id == farm_id).order_by(CarbonScore.created_at.desc()).first()

    def get_by_farmer(self, farmer_id: str) -> List[CarbonScore]:
        return self.db.query(CarbonScore).filter(CarbonScore.farmer_id == farmer_id).order_by(CarbonScore.created_at.desc()).all()

    def get_pending_review(self) -> List[CarbonScore]:
        return self.db.query(CarbonScore).filter(CarbonScore.status == "pending").all()

    def update_status(self, score_id: str, status: str, reviewer_id: str) -> Optional[CarbonScore]:
        from datetime import datetime, timezone
        data = {"status": status, "reviewed_by": reviewer_id, "reviewed_at": datetime.now(timezone.utc)}
        self.db.query(CarbonScore).filter(CarbonScore.id == score_id).update(data)
        self.db.commit()
        return self.get_by_id(score_id)

    def get_total_carbon_by_farmer(self, farmer_id: str) -> float:
        result = self.db.query(CarbonScore).filter(
            CarbonScore.farmer_id == farmer_id,
            CarbonScore.status == "approved"
        ).all()
        return sum(s.carbon_offset_tonnes for s in result)


class SustainabilityReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, report: SustainabilityReport) -> SustainabilityReport:
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_by_farm(self, farm_id: str) -> List[SustainabilityReport]:
        return self.db.query(SustainabilityReport).filter(SustainabilityReport.farm_id == farm_id).all()
