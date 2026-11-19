from app.keitaro import Keitaro
from app.settings import get_settings


def get_keitaro() -> Keitaro:
    settings = get_settings()
    return Keitaro({"url": settings.keitaro_url, "api_key": settings.keitaro_api_key})
