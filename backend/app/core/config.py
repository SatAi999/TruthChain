import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TRUTHCHAIN"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./truthchain.db")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3005,https://truthchain.vercel.app")
    
    # Upload limits
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".txt", ".csv", ".xlsx", ".json", ".png", ".jpg", ".jpeg"}

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()
