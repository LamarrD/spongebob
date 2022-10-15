
from backend.functions.character_get import handler


def test_get_character(test_client, dynamodb):
    """Test get character"""

    # Get character
    response = handler("karen_plankton")
    assert response.status_code == 200