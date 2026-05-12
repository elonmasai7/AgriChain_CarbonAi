import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.advisor import AdvisorMessage, AdvisorRecommendation
from app.repositories.farm_repo import FarmRepository
from app.repositories.carbon_repo import CarbonScoreRepository
from app.services.ai_service import AIService


class AdvisorService:
    def __init__(self, db: Session):
        self.farm_repo = FarmRepository(db)
        self.carbon_repo = CarbonScoreRepository(db)
        self.ai_service = AIService()
        self.db = db

    def chat(self, user_id: str, message: str, language: str = "en") -> dict:
        user_msg = AdvisorMessage(user_id=user_id, role="user", content=message, language=language)
        self.db.add(user_msg)
        self.db.commit()

        keywords = {
            "crop": "crop_rotation",
            "water": "water_conservation",
            "soil": "soil_optimization",
            "disease": "disease_prevention",
            "climate": "climate_adaptation",
            "fertilizer": "soil_optimization",
            "carbon": "carbon_estimation",
            "sustainable": "sustainability",
        }

        detected_topic = "general"
        for kw, topic in keywords.items():
            if kw in message.lower():
                detected_topic = topic
                break

        templates = {
            "en": "Here is advice about {topic} for your farm. Consider implementing sustainable practices to improve your carbon score.",
            "sw": "Hapa ni ushauri kuhusu {topic} kwa shamba lako. Fikiria kutekeleza mazoea endelevu ili kuboresha alama yako ya kaboni.",
            "fr": "Voici un conseil sur {topic} pour votre ferme. Envisagez de mettre en œuvre des pratiques durables pour améliorer votre score carbone.",
        }

        response_text = templates.get(language, templates["en"]).format(topic=detected_topic)

        ai_msg = AdvisorMessage(user_id=user_id, role="assistant", content=response_text, language=language)
        self.db.add(ai_msg)
        self.db.commit()
        self.db.refresh(ai_msg)

        return {"id": str(ai_msg.id), "role": "assistant", "content": response_text, "language": language}

    def get_history(self, user_id: str) -> list:
        return self.db.query(AdvisorMessage).filter(
            AdvisorMessage.user_id == user_id
        ).order_by(AdvisorMessage.created_at.asc()).limit(50).all()

    def get_recommendations(self, farm_id: str, user_id: str) -> list:
        farm = self.farm_repo.get_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")
        if str(farm.farmer_id) != user_id:
            return self.db.query(AdvisorRecommendation).filter(
                AdvisorRecommendation.farm_id == farm_id
            ).order_by(AdvisorRecommendation.created_at.desc()).all()

        scores = self.carbon_repo.get_by_farm(farm_id)
        latest = scores[0] if scores else None

        existing = self.db.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.farm_id == farm_id
        ).count()

        if existing == 0:
            recs = []
            if latest and latest.sustainability_score and latest.sustainability_score < 50:
                recs.append(AdvisorRecommendation(
                    farm_id=farm_id, recommendation_type="improvement",
                    title="Increase Carbon Capture",
                    description="Plant additional trees and maintain cover crops to boost carbon sequestration",
                    priority="high", category="carbon",
                ))
            recs.append(AdvisorRecommendation(
                farm_id=farm_id, recommendation_type="general",
                title="Monitor Soil Health",
                description="Regular soil testing helps optimize fertilizer use and improves crop yields",
                priority="medium", category="soil",
            ))
            for r in recs:
                self.db.add(r)
            self.db.commit()

        return self.db.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.farm_id == farm_id
        ).order_by(AdvisorRecommendation.created_at.desc()).all()
