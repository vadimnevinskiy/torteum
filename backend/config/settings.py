from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    STATIC_DIR: Path = Path("static")
    ALLOWED_IMAGE_EXTENSION: set[str] = {".jpg", ".jpeg", ".png", ".webp"}
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5 MB

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def avatars_dir(self) -> Path:
        return self.STATIC_DIR / "avatars"

    @property
    def database_async_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )

    @property
    def database_sync_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )


settings = Settings()
