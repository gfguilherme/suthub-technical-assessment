from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    table_name: str = "AgeGroups"
    configuration_user: str = "admin"
    configuration_password: str = "try2crack"
    aws_sam_stack_name: str = "age-groups-api-stack"


settings = Settings()
