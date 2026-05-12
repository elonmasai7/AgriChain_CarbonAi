import json
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.carbon import CarbonScore, SustainabilityReport
from app.repositories.carbon_repo import CarbonScoreRepository, SustainabilityReportRepository
from app.repositories.farm_repo import FarmRepository
from app.services.ai_service import AIService


class CarbonService:
    def __init__(self, db: Session):
        self.repo = CarbonScoreRepository(db)
        self.report_repo = SustainabilityReportRepository(db)
        self.farm_repo = FarmRepository(db)
        self.ai_service = AIService()

    def estimate_carbon(self, farm_id: str, force: bool = False) -> CarbonScore:
        if not force:
            existing = self.repo.get_latest_by_farm(farm_id)
            if existing and existing.status != "rejected":
                return existing

        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")

        ai_result = self.ai_service.estimate_carbon_sequestration({
            "crop_types": farm.crop_types,
            "area_hectares": farm.area_hectares,
            "soil_type": farm.soil_type,
            "irrigation_type": farm.irrigation_type,
            "fertilizer_usage": farm.fertilizer_usage,
            "sustainability_practices": farm.sustainability_practices,
            "latitude": farm.latitude,
            "longitude": farm.longitude,
        })

        score = CarbonScore(
            farm_id=farm_id,
            farmer_id=farm.farmer_id,
            carbon_offset_tonnes=ai_result["carbon_offset_tonnes"],
            sustainability_score=ai_result.get("sustainability_score"),
            environmental_health_score=ai_result.get("environmental_health_score"),
            ai_confidence_level=ai_result.get("confidence"),
            ndvi_avg=ai_result.get("ndvi_avg"),
            biomass_estimate=ai_result.get("biomass_estimate"),
            soil_carbon_estimate=ai_result.get("soil_carbon_estimate"),
            methodology_version="AC-CARBON-v1.0",
            input_parameters=json.dumps(ai_result.get("input_parameters", {})),
            raw_ai_output=json.dumps(ai_result),
        )
        return self.repo.create(score)

    def get_carbon_score(self, score_id: str) -> CarbonScore:
        score = self.repo.get_by_id(score_id)
        if not score:
            raise HTTPException(status_code=404, detail="Carbon score not found")
        return score

    def get_farm_scores(self, farm_id: str) -> list:
        return self.repo.get_by_farm(farm_id)

    def get_farmer_scores(self, farmer_id: str) -> list:
        return self.repo.get_by_farmer(farmer_id)

    def review_score(self, score_id: str, status: str, reviewer_id: str) -> CarbonScore:
        return self.repo.update_status(score_id, status, reviewer_id)

    def get_pending_reviews(self) -> list:
        return self.repo.get_pending_review()

    def get_total_carbon(self, farmer_id: str) -> float:
        return self.repo.get_total_carbon_by_farmer(farmer_id)

    def generate_report(self, farm_id: str) -> SustainabilityReport:
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")

        scores = self.repo.get_by_farm(farm_id)
        latest = scores[0] if scores else None

        recommendations = []
        if latest:
            if latest.sustainability_score and latest.sustainability_score < 50:
                recommendations.append("Increase crop diversity to improve soil health")
                recommendations.append("Consider implementing drip irrigation to reduce water usage")
            if latest.sustainability_score and latest.sustainability_score >= 70:
                recommendations.append("Your farm is performing well. Consider applying for premium carbon credits")

        report = SustainabilityReport(
            farm_id=farm_id,
            report_type="monthly",
            report_data=json.dumps({
                "scores": [{"id": str(s.id), "tonnes": s.carbon_offset_tonnes, "date": str(s.created_at)} for s in scores[:12]],
                "total_carbon": sum(s.carbon_offset_tonnes for s in scores),
                "average_score": sum(s.sustainability_score or 0 for s in scores) / len(scores) if scores else 0,
            }),
            recommendations=json.dumps(recommendations),
        )
        return self.report_repo.create(report)

    def get_farm_reports(self, farm_id: str) -> list:
        return self.report_repo.get_by_farm(farm_id)
