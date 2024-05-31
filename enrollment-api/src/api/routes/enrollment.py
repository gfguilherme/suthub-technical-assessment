import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.deps import get_age_group, get_current_user
from src.config import settings
from src.db import enrollments_table, sqs
from src.models import Enrollment

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)]
)
def create_enrollment(enrollment: Enrollment = Depends(get_age_group)) -> Enrollment:
    """Send a POST request to this  resource to create a new enrollment."""

    try:
        sqs.send_message(
            QueueUrl=settings.queue_url,
            MessageBody=enrollment.model_dump_json(),
        )
        return enrollment
    except Exception as exc:
        logger.error(f"Failed to send message to SQS: {exc}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the enrolment. Please try again later.",
        )


@router.get(
    "/{CPF}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)]
)
def read_enrollment(CPF: str) -> Enrollment:
    """Send a GET request to this resource to retrieve an enrollment by CPF."""

    try:
        response = enrollments_table.get_item(Key={"CPF": CPF})

        if "Item" not in response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found or not yet processed. Please try again later.",
            )

        return response["Item"]
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        logger.error(f"Failed to retrieve enrollment from DynamoDB: {exc}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the enrolment. Please try again later.",
        )
