import requests
import boto3
import os
import json
from bs4 import BeautifulSoup
from random import randrange


# Data sourced from SpongeBob's Fandom Wiki
def get_data():
    print("Getting data...")
    base_url = "https://spongebob.fandom.com"
    res = requests.get(f"{base_url}/wiki/List_of_characters/Main")

    soup = BeautifulSoup(res.text, "html.parser")
    main_char_divs = soup.find_all("div", {"class": "bounceme"})
    main_char_ids = [main.attrs["id"] for main in main_char_divs]
    table_data = []

    for main_char_id in main_char_ids:
        char_link = f"{base_url}/wiki/{main_char_id}"
        res = requests.get(char_link)
        char_soup = BeautifulSoup(res.text, "html.parser")

        data = {
            "id": main_char_id.lower(),
            "full_name": char_soup.find_all("h2", {"data-source": "name"})[0].text,
            "residence": char_soup.find_all("div", {"data-source": "residence"})[0]
            .find_all("div")[0]
            .text,
            "job": char_soup.find_all("div", {"data-source": "occupation(s)"})[0]
            .find_all("div")[0]
            .text,
            "gender": char_soup.find_all("div", {"data-source": "gender"})[0]
            .find_all("div")[0]
            .text,
            "color": char_soup.find_all("div", {"data-source": "color"})[0]
            .find_all("div")[0]
            .text,
            "species": char_soup.find_all("div", {"data-source": "species"})[0]
            .find_all("div")[0]
            .text,
            "default_image": char_soup.find_all("div", {"data-source": "image"})[0]
            .find_all("img")[0]
            .attrs["src"],
            "link": char_link,
            "gallery_link": f"{base_url}/wiki/{main_char_id}/gallery",
            "likes": randrange(1000),
        }
        table_data.append({"pk": "character", "sk": main_char_id.lower(), "data": data})
    
    
        char_link = f"{data['link']}"
        res = requests.get(char_link)
        char_soup = BeautifulSoup(res.text, "html.parser")
        description_h2 = char_soup.select('span#Description')[0].parent
        facts = []
        next = description_h2.next_sibling

        while next.name != "h2":
            if next.name == 'p':
                facts.append(next.text.strip())
            next = next.nextSibling
        
        table_data.append( { "pk": "facts", "sk": main_char_id.lower(), "data": { "facts": json.dumps(facts) } } )
    
    
    json.dump(table_data, open("table_data.json", "w"))


def add_data_to_table():
    print("Adding data to table...")
    table_name = os.getenv("TABLE_NAME")
    table = boto3.resource("dynamodb").Table(table_name)
    table_data = json.load(open("table_data.json"))
    for item in table_data:
        table.put_item(Item=item)


def main():
    if not os.path.isfile("table_data.json"):
        get_data()
    add_data_to_table()

if __name__ == "__main__":
    main()
