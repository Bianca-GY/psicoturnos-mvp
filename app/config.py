import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "fake_key_for_testing")


settings = Settings()
