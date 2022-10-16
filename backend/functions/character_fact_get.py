import boto3
import os
import json
import random


table_name = os.getenv("TABLE_NAME")
table = boto3.resource("dynamodb").Table(table_name)


def handler(event, context):
    """Get a random fact about the character"""
    response = table.get_item( Key={"pk": "facts", "sk": event["pathParameters"]["character"].lower()} )

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

    facts = json.loads(response["Item"]["data"]["facts"])
    random_fact = random.choice(facts)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": random_fact
    }
