import boto3
import os
import json
from helper import DecimalEncoder


table_name = os.getenv("TABLE_NAME")
table = boto3.resource("dynamodb").Table(table_name)


def handler(event, context):
    """List specific character"""
    response = table.get_item( Key={"pk": "character", "sk": event["pathParameters"]["character"]} )

    if "Item" not in response:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": "Character not found"}),
        }

    character = response["Item"]["data"]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(character, cls=DecimalEncoder),
    }
