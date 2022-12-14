import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from helper import DecimalEncoder


table_name = os.getenv("TABLE_NAME")
table = boto3.resource("dynamodb").Table(table_name)


def handler(event, context):
    """List all characters"""
    response = table.query(KeyConditionExpression=Key("pk").eq("character"))
    characters = sorted([character["data"] for character in response["Items"]], key=lambda x: x["likes"], reverse=True)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(characters, cls=DecimalEncoder),
    }
