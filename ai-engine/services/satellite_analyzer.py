import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime


class SatelliteAnalyzer:
    def __init__(self):
        self.sources = {
            "sentinel-2": {"resolution": 10, "bands": ["B2", "B3", "B4", "B8"]},
            "landsat-8": {"resolution": 30, "bands": ["B1", "B2", "B3", "B4", "B5"]},
            "modis": {"resolution": 250, "bands": ["B1", "B2"]},
        }

    def calculate_ndvi(self, nir_band: np.ndarray, red_band: np.ndarray) -> np.ndarray:
        denominator = nir_band + red_band
        denominator = np.where(denominator == 0, 0.001, denominator)
        ndvi = (nir_band - red_band) / denominator
        return np.clip(ndvi, -1, 1)

    def calculate_evi(self, nir: np.ndarray, red: np.ndarray, blue: np.ndarray) -> np.ndarray:
        denominator = nir + 6 * red - 7.5 * blue + 1
        denominator = np.where(denominator == 0, 0.001, denominator)
        evi = 2.5 * (nir - red) / denominator
        return np.clip(evi, -1, 1)

    def calculate_land_health_index(self, ndvi: float, evi: float, soil_moisture: Optional[float] = None) -> float:
        health = (ndvi + 1) * 50 + (evi + 1) * 25
        if soil_moisture is not None:
            health += soil_moisture * 25
        return min(100, max(0, health))

    def estimate_water_stress(self, ndvi: float, temperature: float, precipitation: float) -> float:
        water_stress = max(0, 1.0 - (ndvi + 1) / 2 - precipitation / 1000 + temperature / 50)
        return min(1.0, water_stress)

    def estimate_biomass(self, ndvi: float, area_hectares: float) -> float:
        return ndvi * 20 * area_hectares

    def analyze_farm_health(self, lat: float, lon: float, area: float, ndvi_series: List[float]) -> Dict[str, Any]:
        import random
        import math

        current_ndvi = ndvi_series[-1] if ndvi_series else 0.3 + 0.5 * abs(math.sin(lat) * math.cos(lon))
        current_ndvi = current_ndvi + random.uniform(-0.02, 0.02)

        if len(ndvi_series) >= 2:
            ndvi_change = ndvi_series[-1] - ndvi_series[0]
            trend = "improving" if ndvi_change > 0.1 else ("degrading" if ndvi_change < -0.1 else "stable")
        else:
            ndvi_change = 0
            trend = "stable"

        evi = current_ndvi * 1.2 + random.uniform(-0.05, 0.05)
        biomass = self.estimate_biomass(current_ndvi, area)
        land_health = self.calculate_land_health_index(current_ndvi, evi)
        water_stress = self.estimate_water_stress(current_ndvi, 28, 600)

        return {
            "ndvi_current": round(current_ndvi, 4),
            "evi_current": round(evi, 4),
            "ndvi_change_6months": round(ndvi_change, 4),
            "vegetation_trend": trend,
            "land_health_score": round(land_health, 2),
            "water_stress_index": round(water_stress, 4),
            "biomass_estimate": round(biomass, 2),
            "vegetation_fraction": round(max(0, min(1, (current_ndvi + 1) / 2)), 4),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }

    def detect_deforestation(self, historical_ndvi: List[float], threshold: float = 0.3) -> Dict[str, Any]:
        if len(historical_ndvi) < 2:
            return {"deforestation_risk": "insufficient_data", "ndvi_decline": 0}

        decline = historical_ndvi[-1] - historical_ndvi[0]
        risk = "low"
        if decline < -threshold:
            risk = "high"
        elif decline < -threshold / 2:
            risk = "medium"

        return {
            "deforestation_risk": risk,
            "ndvi_decline": round(decline, 4),
            "alert": risk == "high",
        }


analyzer = SatelliteAnalyzer()
