import boto3
import os
import json
from backend.functions.helper import DecimalEncoder


table_name = os.getenv("TABLE_NAME")
table = boto3.resource("dynamodb").Table(table_name)


def handler(event, context):
    """Increment character's likes/dislikes"""
    character = event["pathParameters"]["character"]
    increment = event["queryStringParameters"].get("increment") == "true"
    decrement = event["queryStringParameters"].get("decrement") == "true"

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
    if increment:
        character["likes"] += 1
    elif decrement:
        character["likes"] -= 1

    table.put_item( Item={"pk": "character", "sk": character["id"], "data": character} )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(character, cls=DecimalEncoder),
    }
