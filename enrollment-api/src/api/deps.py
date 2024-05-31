import secrets
from typing import Annotated

from boto3.dynamodb.conditions import Key
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.config import settings
from src.db import age_groups_table
from src.models import Enrollment

app = FastAPI()
security = HTTPBasic()


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = settings.user.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = settings.user_password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


def get_age_group(enrollment: Enrollment):
    """Check if the age of the enrollee falls within any of the age groups registered in the system."""

    age = enrollment.age

    response = age_groups_table.scan(
        FilterExpression=Key("min_age").lte(age) & Key("max_age").gte(age)
    )

    if "Items" in response and response["Items"]:
        return enrollment
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The age of the enrollee does not fall within any of the age groups registered in the system.",
        )
