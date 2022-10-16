import json


def test_get_character(dynamodb_client):
    """Test get character"""
    from backend.functions.character_get import handler

    response = handler({"pathParameters": {"character": "karen_plankton"}}, None)
    body = json.loads(response["body"])
    assert response["statusCode"] == 200
    assert response["headers"] == {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
    }
    assert body["full_name"] == "Karen Plankton"
    assert body["species"] == "Computer"
    assert body["id"] == "karen_plankton"
    assert body["likes"].isdigit()


def test_get_character_doesnt_exist(dynamodb_client):
    from backend.functions.character_get import handler

    """Test get character that doesn't exist"""
    response = handler({"pathParameters": {"character": "not_a_character"}}, None)
    body = json.loads(response["body"])
    assert response["statusCode"] == 404
    assert response["headers"] == {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
    }
    assert body["error"] == "Character not found"
