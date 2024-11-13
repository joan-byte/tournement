from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    # API Settings desde .env
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Tournament API")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # Database settings desde .env
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "375CheyTac")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tournament")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    
    # Construir la URL de la base de datos
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}/{POSTGRES_DB}"
    )

    class Config:
        case_sensitive = True

settings = Settings()