from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    KNOWLEDGE_DIR: Path = PROJECT_ROOT / "data" / "knowledge"
    ORIGIN_DATA_DIR: Path = PROJECT_ROOT / "originData"
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
