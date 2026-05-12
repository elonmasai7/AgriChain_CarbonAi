from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "AgriChain Carbon AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql://agrichain:agrichain@localhost:5432/agrichain"
    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    CORS_ORIGINS: list[str] = ["*"]

    SENTRY_DSN: Optional[str] = None

    POLYGON_RPC_URL: str = "https://polygon-mumbai.infura.io/v3/your-project-id"
    CELO_RPC_URL: str = "https://alfajores-forno.celo-testnet.org"
    BASE_RPC_URL: str = "https://goerli.base.org"
    CONTRACT_CARBON_TOKEN: str = ""
    CONTRACT_CERTIFICATE_NFT: str = ""
    CONTRACT_FARM_REGISTRY: str = ""
    CONTRACT_MARKETPLACE: str = ""
    CONTRACT_MULTISIG: str = ""

    AI_MODEL_PATH: str = "ai-engine/models/carbon_estimator.pth"
    SATELLITE_API_KEY: str = ""
    OPENWEATHER_API_KEY: str = ""
    NASA_EARTHDATA_TOKEN: str = ""

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".tiff", ".geotiff", ".csv", ".json"]
    UPLOAD_DIR: str = "uploads"

    RATE_LIMIT_PER_MINUTE: int = 60
    FRAUD_DETECTION_THRESHOLD: float = 0.7

    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
