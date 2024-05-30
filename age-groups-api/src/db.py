import boto3

from src.config import settings


def get_dynamodb_client():
    return boto3.resource("dynamodb")


dynamodb_client = get_dynamodb_client()
age_groups_table = dynamodb_client.Table(settings.table_name)
