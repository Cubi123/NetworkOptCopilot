from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )

    def model_post_init(self, __context):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is required. Check backend/.env.")


settings = Settings()