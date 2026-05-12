import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class WeatherAnalyzer:
    def __init__(self):
        self.seasonal_patterns = {
            "short_rains": {"months": [3, 4, 5], "avg_mm": 300},
            "long_rains": {"months": [10, 11, 12], "avg_mm": 500},
            "dry_season": {"months": [1, 2, 6, 7, 8, 9], "avg_mm": 50},
        }

    def predict_rainfall(self, lat: float, lon: float, days_ahead: int = 30) -> Dict[str, Any]:
        month = datetime.utcnow().month
        season = "short_rains" if month in [3, 4, 5] else "long_rains" if month in [10, 11, 12] else "dry_season"
        base_mm = self.seasonal_patterns[season]["avg_mm"]

        lat_factor = abs(lat) / 90
        seasonal_factor = 1.0 + np.sin((month - 3) * np.pi / 6) * 0.5

        daily_forecast = []
        for day in range(min(days_ahead, 7)):
            daily_mm = base_mm / 30 * (0.5 + np.random.random() * 0.8) * seasonal_factor * (1 + lat_factor)
            daily_forecast.append({
                "day": day + 1,
                "precipitation_mm": round(max(0, daily_mm * (1 - np.random.random() * 0.3)), 1),
                "confidence": round(0.7 - day * 0.05, 2),
            })

        return {
            "season": season,
            "total_forecast_mm": round(sum(d["precipitation_mm"] for d in daily_forecast), 1),
            "daily_forecast": daily_forecast,
            "latitude_factor": round(lat_factor, 2),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def calculate_drought_risk(self, rainfall_history: List[float], temperature_history: List[float]) -> Dict[str, Any]:
        if len(rainfall_history) < 3:
            return {"drought_risk": "insufficient_data", "risk_score": 0}

        avg_rainfall = np.mean(rainfall_history[-3:])
        avg_temp = np.mean(temperature_history[-3:]) if temperature_history else 28

        risk_score = max(0, 1.0 - avg_rainfall / 500 + (avg_temp - 25) / 50)
        risk_level = "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low"

        return {
            "drought_risk": risk_level,
            "risk_score": round(risk_score, 4),
            "avg_rainfall_3months": round(avg_rainfall, 1),
            "avg_temperature": round(avg_temp, 1),
        }

    def growing_season_analysis(self, lat: float, rainfall_forecast: Dict) -> Dict[str, Any]:
        total_rainfall = rainfall_forecast.get("total_forecast_mm", 0)

        if total_rainfall > 400:
            suitability = "excellent"
        elif total_rainfall > 250:
            suitability = "good"
        elif total_rainfall > 100:
            suitability = "marginal"
        else:
            suitability = "poor"

        return {
            "growing_season_suitability": suitability,
            "total_rainfall_forecast_mm": total_rainfall,
            "recommended_crops": self._recommend_crops(suitability, lat),
        }

    def _recommend_crops(self, suitability: str, lat: float) -> List[str]:
        if suitability == "excellent":
            return ["maize", "beans", "vegetables", "coffee"]
        elif suitability == "good":
            return ["maize", "sorghum", "millet", "cassava"]
        elif suitability == "marginal":
            return ["sorghum", "millet", "cowpeas"]
        else:
            return ["millet", "cowpeas", "cactus pear"]


analyzer = WeatherAnalyzer()
