import warnings

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://ulpan:ulpan@db:5432/ulpan"
    REDIS_URL: str = "redis://redis:6379/0"

    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost", "http://localhost:5173"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

if settings.JWT_SECRET_KEY == "change-me":
    warnings.warn(
        "JWT_SECRET_KEY is set to the insecure default 'change-me'. "
        "Set a strong secret in .env before deploying to production!",
        stacklevel=1,
    )
