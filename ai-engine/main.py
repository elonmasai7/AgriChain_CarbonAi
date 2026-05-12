import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from models.carbon_estimator import estimator
from services.satellite_analyzer import analyzer
from services.fraud_detector import detector
from services.sustainability_advisor import advisor
from services.weather_analyzer import weather_analyzer

app = FastAPI(title="AgriChain AI Engine", version="1.0.0")


class FarmData(BaseModel):
    area_hectares: float
    latitude: float
    longitude: float
    crop_types: Optional[str] = ""
    soil_type: Optional[str] = ""
    irrigation_type: Optional[str] = ""
    fertilizer_usage: Optional[str] = ""
    sustainability_practices: Optional[str] = ""
    rainfall_annual: Optional[float] = 800
    temperature_avg: Optional[float] = 25


class SatelliteRequest(BaseModel):
    lat: float
    lon: float
    area: float = 1
    ndvi_series: Optional[List[float]] = None


class FraudRequest(BaseModel):
    farm_data: FarmData
    carbon_score: float
    existing_farms: Optional[List[dict]] = []


class AdvisorRequest(BaseModel):
    farm_data: FarmData
    language: str = "en"


@app.post("/v1/estimate-carbon")
def estimate_carbon(data: FarmData):
    result = estimator.predict(data.model_dump())
    return result


@app.post("/v1/analyze-satellite")
def analyze_satellite(data: SatelliteRequest):
    ndvi_series = data.ndvi_series or [0.3, 0.35, 0.4]
    result = analyzer.analyze_farm_health(data.lat, data.lon, data.area, ndvi_series)
    return result


@app.post("/v1/detect-fraud")
def detect_fraud(data: FraudRequest):
    farm_dict = data.farm_data.model_dump()
    farm_dict["farmer_id"] = "analysis"
    result = detector.calculate_fraud_risk(farm_dict, data.carbon_score, data.existing_farms)
    return result


@app.post("/v1/get-recommendations")
def get_recommendations(data: AdvisorRequest):
    result = advisor.get_recommendations(data.farm_data.model_dump(), data.language)
    return {"recommendations": result}


@app.post("/v1/predict-weather")
def predict_weather(lat: float, lon: float, days: int = 7):
    result = weather_analyzer.predict_rainfall(lat, lon, days)
    return result


@app.get("/v1/health")
def health():
    return {"status": "healthy", "model_loaded": estimator.model is not None}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
