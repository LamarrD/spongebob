

def test_get_character_fact(dynamodb_client):
    """Test get character fact"""
    from backend.functions.character_fact_get import handler

    response = handler({"pathParameters": {"character": "karen_plankton"}}, None)
    assert response["statusCode"] == 200
    assert response["headers"] == {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
    }
    assert type(response['body']) is str
    assert len(response['body']) != 0
