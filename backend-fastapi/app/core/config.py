from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "HelpDesk AI API"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgrespassword@db:5432/helpdesk_ai"
    )
    AI_API_KEY: str = "tu_api_key_aqui"
    AI_BASE_URL: str = "https://api.groq.com/openai/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
