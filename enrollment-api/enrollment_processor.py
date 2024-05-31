import json
import logging
import os
import time

import boto3

logger = logging.getLogger(__name__)

sqs = boto3.client("sqs")

dynamodb_client = boto3.resource("dynamodb")
enrollments_table = dynamodb_client.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    for record in event["Records"]:
        body = record["body"]

        # Simulate processing time
        time.sleep(2)

        try:
            enrollment = json.loads(body)
            enrollments_table.put_item(Item=enrollment)
        except Exception as exc:
            logger.error("Failed to process enrollment: %s", exc)
            raise exc
