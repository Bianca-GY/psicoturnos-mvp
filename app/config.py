from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    MONGODB_URI: str = ""
    MONGODB_DB_NAME: str = "psicoturnos"
    MONGODB_COLLECTION_NAME: str = "appointments"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
