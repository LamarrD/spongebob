import json


def test_get_characters(dynamodb_client):
    """Test get character"""
    from backend.functions.characters_list import handler

    response = handler({"pathParameters": {"character": "karen_plankton"}}, None)
    data = json.load(open("table_data.json"))
    expected_character_names = [datum["data"]["full_name"] for datum in data if datum["pk"] == "character"]

    body = json.loads(response["body"])
    character_names = [character["full_name"] for character in body]
    assert response["statusCode"] == 200
    assert response["headers"] == {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
    }
    assert sorted(character_names) == sorted(expected_character_names)
