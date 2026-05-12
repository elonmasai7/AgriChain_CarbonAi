import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any


class CarbonEstimator:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            "area_hectares", "latitude", "longitude",
            "crop_type_encoded", "soil_type_encoded",
            "irrigation_type_encoded", "fertilizer_type_encoded",
            "sustainable_practices_count", "rainfall_annual",
            "temperature_avg",
        ]

    def _encode_categorical(self, value: str, categories: list) -> int:
        if not value:
            return 0
        value = value.lower()
        for i, cat in enumerate(categories):
            if cat in value:
                return i + 1
        return 0

    def preprocess_input(self, farm_data: Dict[str, Any]) -> np.ndarray:
        crop_categories = ["maize", "coffee", "cocoa", "teff", "rice", "mixed", "vegetables", "fruits"]
        soil_categories = ["loam", "clay", "sandy", "silt", "peat", "chalk"]
        irrigation_categories = ["drip", "sprinkler", "flood", "rainfed", "furrow"]
        fertilizer_categories = ["organic", "chemical", "compost", "manure", "none"]

        practices_text = str(farm_data.get("sustainability_practices", "")).lower()
        practice_keywords = ["agroforestry", "cover crop", "no-till", "conservation",
                            "rotation", "mulching", "compost", "organic", "permaculture"]
        practice_count = sum(1 for kw in practice_keywords if kw in practices_text)

        features = [
            float(farm_data.get("area_hectares", 1)),
            float(farm_data.get("latitude", 0)),
            float(farm_data.get("longitude", 0)),
            self._encode_categorical(farm_data.get("crop_types", ""), crop_categories),
            self._encode_categorical(farm_data.get("soil_type", ""), soil_categories),
            self._encode_categorical(farm_data.get("irrigation_type", ""), irrigation_categories),
            self._encode_categorical(farm_data.get("fertilizer_usage", ""), fertilizer_categories),
            practice_count,
            float(farm_data.get("rainfall_annual", 800)),
            float(farm_data.get("temperature_avg", 25)),
        ]
        return np.array(features).reshape(1, -1)

    def predict(self, farm_data: Dict[str, Any]) -> Dict[str, float]:
        X = self.preprocess_input(farm_data)

        if self.model is not None:
            carbon_tonnes = float(self.model.predict(X)[0])
        else:
            area = float(farm_data.get("area_hectares", 1))
            base_rate = 2.5
            crop_type = str(farm_data.get("crop_types", "")).lower()
            if "coffee" in crop_type:
                base_rate = 4.5
            elif "cocoa" in crop_type:
                base_rate = 5.0
            elif "maize" in crop_type:
                base_rate = 3.2
            carbon_tonnes = base_rate * area

        noise = np.random.normal(0, carbon_tonnes * 0.02)
        carbon_tonnes = max(0, carbon_tonnes + noise)

        sustainability_score = min(100, max(0, (carbon_tonnes / max(farm_data.get("area_hectares", 1), 0.1)) * 12 + 20))
        confidence = min(0.95, 0.65 + (sustainability_score / 100) * 0.3)

        return {
            "carbon_offset_tonnes": round(carbon_tonnes, 2),
            "sustainability_score": round(sustainability_score, 2),
            "confidence": round(confidence, 4),
        }

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1,
        )
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        return self

    def save(self, path: str):
        joblib.dump({"model": self.model, "scaler": self.scaler}, path)

    def load(self, path: str):
        data = joblib.load(path)
        self.model = data["model"]
        self.scaler = data["scaler"]


estimator = CarbonEstimator()
