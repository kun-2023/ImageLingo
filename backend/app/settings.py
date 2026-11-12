from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT=Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    openai_api_key: SecretStr
    openai_model:str

    model_config=SettingsConfigDict(env_file=PROJECT_ROOT/".env")
