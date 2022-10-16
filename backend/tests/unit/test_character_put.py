import json
import os


def test_put_character_increment_like(dynamodb_client):
    """Test increase character's like"""
    from backend.functions.character_put import handler
    import boto3

    table_name = os.getenv("TABLE_NAME")
    table = boto3.resource("dynamodb").Table(table_name)
    res = table.get_item( Key={"pk": "character", "sk": "karen_plankton"} )
    current_likes = res['Item']['data']['likes']
    response = handler( 
        { "pathParameters": {"character": "karen_plankton"}, "queryStringParameters": {"increment": "true"}, }, 
        None, 
    )
    assert response["statusCode"] == 200
    assert response["headers"] == {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
    }
    body = json.loads(response["body"])
    assert int(body['likes']) == current_likes + 1



def test_put_character_decrement_like(dynamodb_client):
    """Test decrease character's like"""
    from backend.functions.character_put import handler
    import boto3

    table_name = os.getenv("TABLE_NAME")
    table = boto3.resource("dynamodb").Table(table_name)
    res = table.get_item( Key={"pk": "character", "sk": "patrick_star"} )
    current_likes = res['Item']['data']['likes']
    response = handler( 
        { "pathParameters": {"character": "patrick_star"}, "queryStringParameters": {"decrement": "true"}, }, 
        None, 
    )
    assert response["statusCode"] == 200
    assert response["headers"] == {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
    }
    body = json.loads(response["body"])
    assert int(body['likes']) == current_likes - 1
