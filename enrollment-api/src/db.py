import boto3

from src.config import settings


def get_dynamodb_client():
    return boto3.resource("dynamodb")


sqs = boto3.client("sqs")

dynamodb_client = get_dynamodb_client()
enrollments_table = dynamodb_client.Table(settings.enrollment_table)
age_groups_table = dynamodb_client.Table(settings.age_groups_table)
