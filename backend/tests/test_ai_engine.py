import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../ai-engine'))

from models.carbon_estimator import CarbonEstimator
from services.fraud_detector import FraudDetector
from services.sustainability_advisor import SustainabilityAdvisor


def test_carbon_estimator():
    estimator = CarbonEstimator()
    result = estimator.predict({
        "area_hectares": 5.0,
        "latitude": -1.2921,
        "longitude": 36.8219,
        "crop_types": "maize, beans",
        "soil_type": "loam",
        "irrigation_type": "drip",
        "fertilizer_usage": "organic",
        "sustainability_practices": "agroforestry, cover cropping, crop rotation",
    })
    assert result["carbon_offset_tonnes"] > 0
    assert 0 <= result["sustainability_score"] <= 100
    assert 0 < result["confidence"] <= 1.0


def test_carbon_estimator_different_crops():
    estimator = CarbonEstimator()
    coffee = estimator.predict({"area_hectares": 1, "crop_types": "coffee", "latitude": 0, "longitude": 0})
    maize = estimator.predict({"area_hectares": 1, "crop_types": "maize", "latitude": 0, "longitude": 0})
    assert coffee["carbon_offset_tonnes"] > maize["carbon_offset_tonnes"]


def test_fraud_detector():
    detector = FraudDetector()
    result = detector.calculate_fraud_risk({
        "area_hectares": 5.0,
        "latitude": -1.2921,
        "longitude": 36.8219,
        "crop_types": "maize",
        "farmer_id": "farmer1",
    }, carbon_score=18.5, existing_farms=[])
    assert "fraud_score" in result
    assert result["risk_level"] in ("low", "medium", "high")


def test_fraud_detector_large_area():
    detector = FraudDetector()
    result = detector.calculate_fraud_risk({
        "area_hectares": 50000,
        "latitude": 0,
        "longitude": 0,
        "farmer_id": "farmer1",
    }, carbon_score=100000, existing_farms=[])
    assert result["fraud_score"] > 0.3


def test_sustainability_advisor():
    advisor = SustainabilityAdvisor()
    recs = advisor.get_recommendations({
        "crop_types": "maize",
        "irrigation_type": "flood",
        "sustainability_practices": "",
    })
    assert len(recs) > 0
    assert any("crop_rotation" in r["topic"] for r in recs)


def test_advisor_multilingual():
    advisor = SustainabilityAdvisor()
    recs_en = advisor.get_recommendations({"crop_types": "maize"}, "en")
    recs_sw = advisor.get_recommendations({"crop_types": "maize"}, "sw")
    assert len(recs_en) > 0
    assert len(recs_sw) > 0
