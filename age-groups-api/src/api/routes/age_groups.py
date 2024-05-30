import logging

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
