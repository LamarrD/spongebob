import boto3
import os
import json
from boto3.dynamodb.conditions import Key


table_name = os.getenv('TABLE_NAME')
table = boto3.resource('dynamodb').Table(table_name)

def handler(event, context):
    """List all characters"""
    print("Hello World")
    response = table.query(
        KeyConditionExpression=Key('pk').eq('character')
    )
    characters = [character['data'] for character in response['Items']]

    return {
        "statusCode": 200,
        'headers': {'Content-Type': 'application/json'},
        "body": json.dumps(characters)
    }

