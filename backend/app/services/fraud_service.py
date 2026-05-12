import json
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.fraud import FraudAlert, AuditLog
from app.repositories.fraud_repo import FraudAlertRepository, AuditLogRepository
from app.repositories.farm_repo import FarmRepository
from app.repositories.carbon_repo import CarbonScoreRepository
from app.services.ai_service import AIService


class FraudService:
    def __init__(self, db: Session):
        self.alert_repo = FraudAlertRepository(db)
        self.audit_repo = AuditLogRepository(db)
        self.farm_repo = FarmRepository(db)
        self.carbon_repo = CarbonScoreRepository(db)
        self.ai_service = AIService()

    def analyze_farm(self, farm_id: str) -> dict:
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")

        scores = self.carbon_repo.get_by_farm(farm_id)
        latest_score = scores[0] if scores else None
        total_carbon = sum(s.carbon_offset_tonnes for s in scores) if scores else 0

        farm_data = {
            "area_hectares": farm.area_hectares,
            "crop_types": farm.crop_types,
            "soil_type": farm.soil_type,
        }
        anomaly_result = self.ai_service.detect_anomalies(farm_data, total_carbon)

        existing_alerts = self.alert_repo.get_by_farm(farm_id)
        fraud_score = max(
            [a.fraud_score for a in existing_alerts] + [anomaly_result["fraud_score"]]
        )

        if fraud_score >= 0.5 and not any(a.status == "open" for a in existing_alerts):
            alert = FraudAlert(
                farm_id=farm_id,
                alert_type=anomaly_result.get("risk_level", "medium"),
                severity=anomaly_result["risk_level"],
                fraud_score=fraud_score,
                description=json.dumps(anomaly_result["anomalies"]),
                evidence=json.dumps(anomaly_result["details"]),
            )
            self.alert_repo.create(alert)

        return {
            "fraud_score": fraud_score,
            "risk_level": anomaly_result["risk_level"],
            "alerts": existing_alerts,
            "details": anomaly_result["details"],
        }

    def get_alerts(self, status: str = None) -> list:
        if status:
            return [a for a in self.alert_repo.list_open() if a.status == status]
        return self.alert_repo.list_open()

    def get_farm_alerts(self, farm_id: str) -> list:
        return self.alert_repo.get_by_farm(farm_id)

    def update_alert(self, alert_id: str, data: dict) -> FraudAlert:
        if data.get("status") == "resolved":
            data["resolved_at"] = datetime.now(timezone.utc)
        return self.alert_repo.update(alert_id, data)

    def log_audit(self, entity_type: str, entity_id: str, action: str, performed_by: str, details: str = None, ip: str = None):
        log = AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            performed_by=performed_by,
            details=details,
            ip_address=ip,
        )
        return self.audit_repo.create(log)

    def get_audit_logs(self, entity_type: str, entity_id: str) -> list:
        return self.audit_repo.list_by_entity(entity_type, entity_id)
