from typing import Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "PharmaShield"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "sqlite:///./pharmashield.db"

    JWT_SECRET: str = "pharmashield_hackathon_super_secret_jwt_key_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    AI_API_KEY: str = ""
    AI_MODEL_NAME: str = "gemini-1.5-pro"

    # SAP Configuration
    SAP_BASE_URL: str = "https://mock-sap.pharmashield.local"
    SAP_MODE: str = "MOCK"

    # Chico State SAP Gateway OData Configuration (Techunter)
    SAP_ODATA_BASE_URL: str = (
        "https://merida.cob.csuchico.edu:8038/"
        "sap/opu/odata/sap/ZPS_GATEWAY_SRV"
    )
    SAP_USER: str = ""
    SAP_PASSWORD: str = ""

    # SAP BTP / S4HANA RAP Integration Configuration
    SAP_ODATA_URL: str = (
        "https://my-sap-btp-tenant.s4hana.ondemand.com/sap/opu/odata4/sap/zui_pharmashield_gov_o4/srvd/sap/zui_pharmashield/0001"
    )
    SAP_CLIENT_ID: str = ""
    SAP_CLIENT_SECRET: str = ""
    SAP_TOKEN_URL: str = ""
    SAP_COMM_USER: str = ""
    SAP_COMM_PASSWORD: str = ""

    CORS_ORIGINS: Union[list[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> list[str]:
        if isinstance(v, str):
            v_stripped = v.strip()
            if v_stripped.startswith("[") and v_stripped.endswith("]"):
                import json
                try:
                    return json.loads(v_stripped)
                except Exception:
                    pass
            return [i.strip() for i in v_stripped.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
