import requests

base_url = "https://api.myleg.org/"

def test_character_get_success():
    res = requests.get(f"{base_url}/character/spongebob_squarepants_(character)")
    expected_data = {
        "color": "Light yellow with olive-green holes",
        "full_name": "SpongeBob SquarePants",
        "gallery_link": "https://spongebob.fandom.com/wiki/SpongeBob_SquarePants_(character)/gallery",
        "gender": "Male",
        "job": "Krusty Krab fry cookOccasional cashier, waiter, and janitor[3]Manager of the Krusty Krab 2[4]",
        "link": "https://spongebob.fandom.com/wiki/SpongeBob_SquarePants_(character)",
        "residence": "SpongeBob's house (after moving[1] from Harold and Margaret SquarePants' house),[2] Bikini Bottom, Pacific Ocean",
        "species": "Sea sponge (Aplysina fistularis)[7]"
    }
    assert res.status_code == 200
    assert res.json() == expected_data


def test_character_get_not_found():
    res = requests.get(f"{base_url}/character/non-existant-character")
    assert res.status_code == 404


if __name__ == "__main__":
    test_character_get_success()
    test_character_get_not_found()