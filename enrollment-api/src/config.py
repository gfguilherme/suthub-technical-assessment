from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    enrollment_table: str = "Enrollment"
    age_groups_table: str = "AgeGroups"
    user: str = "user"
    user_password: str = "strongpassword"
    queue_url: str = ""


settings = Settings()
