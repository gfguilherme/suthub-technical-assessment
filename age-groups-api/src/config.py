from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    table_name: str = "AgeGroups"
    configuration_user: str = "admin"
    configuration_password: str = "try2crack"


settings = Settings()
