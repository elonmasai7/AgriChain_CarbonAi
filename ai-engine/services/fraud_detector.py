import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime


class FraudDetector:
    def __init__(self):
        self.anomaly_threshold = 2.5
        self.historical_data: List[Dict] = []

    def check_farm_duplication(self, lat: float, lon: float, farmer_id: str,
                               existing_farms: List[Dict]) -> Dict[str, Any]:
        for farm in existing_farms:
            if str(farm.get("farmer_id")) == farmer_id:
                continue
            f_lat = farm.get("latitude", 0)
            f_lon = farm.get("longitude", 0)
            distance = np.sqrt((lat - f_lat) ** 2 + (lon - f_lon) ** 2)
            if distance < 0.001:
                return {
                    "duplicate_detected": True,
                    "similar_farm_id": str(farm.get("id")),
                    "distance_km": round(distance * 111, 2),
                    "score": 0.9,
                }
        return {"duplicate_detected": False, "score": 0.0}

    def check_unrealistic_estimates(self, carbon_tonnes: float, area_hectares: float,
                                    crop_type: str) -> Dict[str, Any]:
        max_rates = {
            "maize": 8, "coffee": 12, "cocoa": 15, "teff": 5,
            "rice": 4, "mixed": 10, "vegetables": 6, "default": 10,
        }
        rate = carbon_tonnes / max(area_hectares, 0.01)
        max_rate = max_rates.get(crop_type.lower(), max_rates["default"])

        if rate > max_rate * 3:
            return {"unrealistic": True, "score": 0.8, "reason": f"Rate {rate:.1f} t/ha exceeds max {max_rate} t/ha"}
        elif rate > max_rate * 2:
            return {"unrealistic": True, "score": 0.5, "reason": f"Rate {rate:.1f} t/ha is unusually high"}
        return {"unrealistic": False, "score": 0.0, "rate": rate}

    def check_image_manipulation(self, image_metadata: Dict[str, Any]) -> Dict[str, Any]:
        red_flags = []
        score = 0.0

        if image_metadata.get("file_size", 0) < 1024:
            red_flags.append("Suspiciously small image file")
            score += 0.3
        if image_metadata.get("modified", False):
            red_flags.append("Image metadata shows modifications")
            score += 0.4
        if image_metadata.get("dimensions"):
            w, h = image_metadata["dimensions"]
            if w < 100 or h < 100:
                red_flags.append("Image resolution too low")
                score += 0.2

        return {
            "manipulation_detected": len(red_flags) > 0,
            "score": min(1.0, score),
            "flags": red_flags,
        }

    def calculate_fraud_risk(self, farm_data: Dict[str, Any], carbon_score: float,
                             existing_farms: List[Dict]) -> Dict[str, Any]:
        risks = []
        total_score = 0.0

        dup_check = self.check_farm_duplication(
            farm_data.get("latitude", 0), farm_data.get("longitude", 0),
            farm_data.get("farmer_id", ""), existing_farms
        )
        if dup_check["duplicate_detected"]:
            risks.append(dup_check)
            total_score += dup_check["score"]

        estimate_check = self.check_unrealistic_estimates(
            carbon_score, farm_data.get("area_hectares", 1),
            farm_data.get("crop_types", "default")
        )
        if estimate_check["unrealistic"]:
            risks.append(estimate_check)
            total_score += estimate_check["score"]

        area = farm_data.get("area_hectares", 0)
        if area > 10000:
            risks.append({"type": "suspicious_area", "score": 0.3, "reason": "Area exceeds 10,000 hectares"})
            total_score += 0.3
        if area <= 0:
            risks.append({"type": "invalid_area", "score": 0.5, "reason": "Invalid farm area"})
            total_score += 0.5

        overall_score = min(1.0, total_score)
        if overall_score >= 0.7:
            risk_level = "high"
        elif overall_score >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "fraud_score": round(overall_score, 4),
            "risk_level": risk_level,
            "risk_factors": risks,
            "needs_review": overall_score > 0.3,
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }


detector = FraudDetector()
