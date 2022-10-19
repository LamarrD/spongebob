import requests


def test_characters_list_success():
    base_url = "https://api.myleg.org/"
    res = requests.get(f"{base_url}/characters/")
    character = res.json()[0]
    expected_keys = sorted(['full_name', 'gender', 'color', 'species', 'gallery_link', 'link', 'residence', 'job'])
    assert res.status_code == 200
    assert list(sorted(character.keys())) == expected_keys


if __name__ == "__main__":
    test_characters_list_success()