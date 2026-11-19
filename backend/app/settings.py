from functools import cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    keitaro_url: str
    keitaro_api_key: str
    campaign_prefix: str


@cache
def get_settings() -> Settings:
    return Settings()
