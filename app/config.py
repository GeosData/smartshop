from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "SmartShop"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://smartshop:smartshop@localhost:5432/smartshop"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Auth
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100


settings = Settings()
