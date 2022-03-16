from typing import List
from pydantic import BaseSettings
from pydantic import SecretStr


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "FastAPI example application"
    DEBUG: bool = True
    VERSION: str = "0.0.1"
    ENVIRONMENT: str = 'dev'
    ALLOWED_HOSTS: List[str] = ["*"]
    # ENVIRONMENT: str = 'prod'
    # ENVIRONMENT: str = 'local'


app_settings = AppSettings()
