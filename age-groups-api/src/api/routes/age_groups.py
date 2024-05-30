import logging

from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException, status

from src.db import age_groups_table
from src.models import AgeGroup

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_age_group(age_group: AgeGroup) -> AgeGroup:
    """Send a POST request to this resource to create a new age group."""

    try:
        age_groups_table.put_item(Item=age_group.model_dump())
        return age_group.model_dump()
    except Exception as exc:
        logger.error("Failed to create a age group: %s", exc)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating an age group. Please try again later.",
        )


@router.delete("/{name}", status_code=status.HTTP_200_OK)
def delete_age_group(name: str) -> AgeGroup:
    """Send a DELETE request to this resource to delete an age group."""

    try:
        age_group = age_groups_table.delete_item(
            Key={"name": name},
            ReturnValues="ALL_OLD",
            ConditionExpression="attribute_exists(#n)",
            ExpressionAttributeNames={"#n": "name"},
        )
        return age_group["Attributes"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The age group with the name '{name}' was not found.",
            )
        else:
            raise
    except Exception as exc:
        logger.error("Failed to delete the age group: %s", exc)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the age group. Please try again later.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
def read_age_groups() -> list[AgeGroup]:
    """Send a GET request to this resource to retrieve all age groups."""

    try:
        response = age_groups_table.scan()
        return response["Items"]
    except Exception as exc:
        logger.error("Failed retrieve age groups: %s", exc)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving age groups. Please try again later.",
        )
