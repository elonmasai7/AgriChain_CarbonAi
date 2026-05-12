import json
import random
import math
from typing import Optional


class AIService:
    def __init__(self):
        self.model_loaded = False

    def estimate_carbon_sequestration(self, farm_data: dict) -> dict:
        crop_types = (farm_data.get("crop_types") or "").lower()
        area = farm_data.get("area_hectares", 1)
        soil_type = (farm_data.get("soil_type") or "").lower()
        irrigation = (farm_data.get("irrigation_type") or "").lower()
        fertilizer = (farm_data.get("fertilizer_usage") or "").lower()
        practices = (farm_data.get("sustainability_practices") or "").lower()
        lat = farm_data.get("latitude", 0)

        carbon_base = 2.5
        if "maize" in crop_types or "corn" in crop_types:
            carbon_base = 3.2
        elif "coffee" in crop_types:
            carbon_base = 4.5
        elif "cocoa" in crop_types:
            carbon_base = 5.0
        elif "teff" in crop_types:
            carbon_base = 2.0
        elif "rice" in crop_types:
            carbon_base = 1.8
        elif "mixed" in crop_types or "diverse" in crop_types:
            carbon_base = 4.0

        soil_factor = 1.0
        if "loam" in soil_type:
            soil_factor = 1.3
        elif "clay" in soil_type:
            soil_factor = 1.2
        elif "sandy" in soil_type:
            soil_factor = 0.7
        elif "organic" in soil_type or "peat" in soil_type:
            soil_factor = 1.5

        irrigation_factor = 1.0
        if "drip" in irrigation:
            irrigation_factor = 1.2
        elif "sprinkler" in irrigation:
            irrigation_factor = 1.0
        elif "flood" in irrigation or "traditional" in irrigation:
            irrigation_factor = 0.8
        elif "rainfed" in irrigation or "none" in irrigation:
            irrigation_factor = 0.9

        fertilizer_factor = 1.0
        if "organic" in fertilizer or "compost" in fertilizer or "natural" in fertilizer:
            fertilizer_factor = 1.4
        elif "chemical" in fertilizer or "synthetic" in fertilizer:
            fertilizer_factor = 0.8
        elif "none" in fertilizer or "no" in fertilizer:
            fertilizer_factor = 1.1

        practice_bonus = 1.0
        practice_keywords = ["agroforestry", "cover crop", "no-till", "conservation", "rotation",
                             "mulching", "compost", "organic", "permaculture", "silvopasture"]
        for kw in practice_keywords:
            if kw in practices:
                practice_bonus += 0.1

        climate_factor = 0.8 + 0.4 * abs(math.sin(math.radians(lat)))
        biodiversity_factor = 1.0 + (practice_bonus - 1.0) * 0.5

        carbon_per_hectare = carbon_base * soil_factor * irrigation_factor * fertilizer_factor * practice_bonus * climate_factor * biodiversity_factor
        total_carbon = round(carbon_per_hectare * area, 2)

        noise = random.uniform(-0.05, 0.05)
        sustainability_score = round(min(100, max(0, (carbon_per_hectare / 6.0) * 100 + noise * 100)), 2)
        environmental_health = round(min(100, max(0, sustainability_score * random.uniform(0.85, 1.0))), 2)

        ndvi_avg = round(0.3 + (sustainability_score / 100) * 0.5 + random.uniform(-0.05, 0.05), 4)
        biomass = round(total_carbon * 2.5 * random.uniform(0.9, 1.1), 2)
        soil_carbon = round(total_carbon * 0.6 * random.uniform(0.8, 1.2), 2)

        confidence = round(min(0.95, 0.7 + (sustainability_score / 100) * 0.25), 4)

        return {
            "carbon_offset_tonnes": total_carbon,
            "sustainability_score": sustainability_score,
            "environmental_health_score": environmental_health,
            "confidence": confidence,
            "ndvi_avg": ndvi_avg,
            "biomass_estimate": biomass,
            "soil_carbon_estimate": soil_carbon,
            "input_parameters": {
                "crop_types": crop_types,
                "area_hectares": area,
                "soil_type": soil_type,
                "irrigation": irrigation,
                "fertilizer": fertilizer,
                "sustainable_practices_count": sum(1 for kw in practice_keywords if kw in practices),
            },
        }

    def detect_anomalies(self, farm_data: dict, carbon_score: float) -> dict:
        anomalies = []
        fraud_score = 0.0

        area = farm_data.get("area_hectares", 0)
        if area > 10000:
            anomalies.append("Suspiciously large farm area")
            fraud_score += 0.3
        if area <= 0:
            anomalies.append("Invalid farm area")
            fraud_score += 0.5

        if carbon_score > 50000:
            anomalies.append("Carbon estimate exceeds realistic threshold")
            fraud_score += 0.3
        elif carbon_score > 10000:
            fraud_score += 0.1

        if fraud_score > 0.5:
            risk_level = "high"
        elif fraud_score > 0.2:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "fraud_score": round(fraud_score, 4),
            "risk_level": risk_level,
            "anomalies": anomalies,
            "details": {
                "data_completeness": random.uniform(0.7, 1.0),
                "historical_consistency": random.uniform(0.6, 1.0),
                "geo_plausibility": random.uniform(0.8, 1.0),
            },
        }

    def generate_sustainability_advice(self, farm_data: dict, language: str = "en") -> dict:
        crop_types = (farm_data.get("crop_types") or "").lower()
        soil_type = (farm_data.get("soil_type") or "").lower()
        practices = (farm_data.get("sustainability_practices") or "").lower()

        recommendations = []
        if "maize" in crop_types or "corn" in crop_types:
            recommendations.append("Rotate maize with legumes to fix nitrogen naturally")
        if "sandy" in soil_type:
            recommendations.append("Add organic matter to improve water retention in sandy soil")
        if "agroforestry" not in practices:
            recommendations.append("Plant shade trees to improve biodiversity and carbon capture")
        if "cover crop" not in practices:
            recommendations.append("Use cover crops during off-seasons to prevent soil erosion")
        if "no-till" not in practices and "conservation" not in practices:
            recommendations.append("Adopt no-till farming to preserve soil structure and carbon")

        translations = {
            "sw": {
                "title": "Mapendekezo ya Kilimo Endelevu",
                "intro": "Kulingana na data ya shamba lako, hapa kuna mapendekezo:",
            },
            "fr": {
                "title": "Recommandations d'Agriculture Durable",
                "intro": "Sur la base des données de votre ferme, voici des recommandations :",
            },
        }

        lang_data = translations.get(language, {})
        return {
            "title": lang_data.get("title", "Sustainability Recommendations"),
            "introduction": lang_data.get("intro", "Based on your farm data, here are recommendations:"),
            "recommendations": recommendations[:5],
            "language": language,
        }
