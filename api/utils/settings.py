from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Use this to build paths inside the project
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Class to hold application's config values."""

    DB_TYPE: str
    DB_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Load settings from the .env file
settings = Settings()
