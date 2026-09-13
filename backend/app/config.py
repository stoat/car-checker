from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://carchecker:carchecker@db:5432/carchecker"

    # DVLA Vehicle Enquiry Service
    dvla_api_key: str = ""
    dvla_ves_url: str = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

    # DVSA MOT History API
    dvsa_api_key: str = ""
    dvsa_client_id: str = ""
    dvsa_client_secret: str = ""
    dvsa_token_url: str = ""
    dvsa_scope: str = "https://tapi.dvsa.gov.uk/.default"
    dvsa_mot_url: str = "https://history.mot.api.gov.uk/v1/trade/vehicles/registration/{registration}"

    # Cache TTLs (seconds)
    vehicle_cache_ttl: int = 86400   # 24 hours
    mot_cache_ttl: int = 86400       # 24 hours
    valuation_cache_ttl: int = 21600  # 6 hours
    recall_cache_ttl: int = 86400    # 24 hours

    log_level: str = "INFO"


settings = Settings()
