from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.fraud import FraudAlert, AuditLog


class FraudAlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, alert: FraudAlert) -> FraudAlert:
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_by_id(self, alert_id: str) -> Optional[FraudAlert]:
        return self.db.query(FraudAlert).filter(FraudAlert.id == alert_id).first()

    def get_by_farm(self, farm_id: str) -> List[FraudAlert]:
        return self.db.query(FraudAlert).filter(FraudAlert.farm_id == farm_id).order_by(FraudAlert.created_at.desc()).all()

    def list_open(self, skip: int = 0, limit: int = 100) -> List[FraudAlert]:
        return self.db.query(FraudAlert).filter(FraudAlert.status == "open").offset(skip).limit(limit).all()

    def update(self, alert_id: str, data: dict) -> Optional[FraudAlert]:
        self.db.query(FraudAlert).filter(FraudAlert.id == alert_id).update(data)
        self.db.commit()
        return self.get_by_id(alert_id)


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, log: AuditLog) -> AuditLog:
        self.db.add(log)
        self.db.commit()
        return log

    def list_by_entity(self, entity_type: str, entity_id: str) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).order_by(AuditLog.created_at.desc()).all()
