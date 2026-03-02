from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Aplicación
    APP_NAME: str = "Ingecon Findeter API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Base de datos
    DATABASE_URL: str = "postgresql://ingecon:ingecon@localhost:5432/ingecon_findeter"

    # Autenticación
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 horas
    ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
