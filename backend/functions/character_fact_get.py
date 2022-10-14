import boto3
import os
import json
import random
import requests
from bs4 import BeautifulSoup
from helper import DecimalEncoder


table_name = os.getenv("TABLE_NAME")
table = boto3.resource("dynamodb").Table(table_name)


def handler(event, context):
    """Get a random fact about the character"""
    response = table.get_item(
        Key={"pk": "character", "sk": event["pathParameters"]["character"]}
    )

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
    char_link = f"{character['link']}"
    res = requests.get(char_link)
    char_soup = BeautifulSoup(res.text, "html.parser")
    description_h2 = char_soup.select('span#Description')[0].parent
    facts = []
    next = description_h2.next_sibling

    while next.name != "h2":
        if next.name == 'p':
            facts.append(next.text.strip())
        next = next.nextSibling
    
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

print(handler( { "pathParameters": { "character": "gary_the_snail" } },None ))