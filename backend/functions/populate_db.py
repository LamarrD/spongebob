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

    res2 = requests.get(f"{base_url}/wiki/List_of_characters/Supporting")
    soup = BeautifulSoup(res2.text, "html.parser")
    supporting_char_divs = soup.find_all("div", {"class": "bounceme"})[:25]
    supporting_char_ids = [support.attrs["id"] for support in supporting_char_divs]
    char_ids = ["fred"] + main_char_ids + supporting_char_ids

    table_data = []
    likes = 1000

    for char_id in char_ids:
        char_link = f"{base_url}/wiki/{char_id}"
        res = requests.get(char_link)
        char_soup = BeautifulSoup(res.text, "html.parser")
        full_name = char_soup.find_all("h2", {"data-source": "name"})[0].text
        default_image = char_soup.find_all( attrs={"data-source": "image"})[0].find_all("img")[0]
        open(f"./frontend/public/img/{char_id.lower()}.webp", 'wb').write(requests.get(default_image.attrs['src']).content)


        species = None
        try:
            species =  char_soup.find_all("div", {"data-source": "species"})[0] .find_all("div")[0] .text
        except:
            species = "Unknown"

        likes = likes - randrange(20)
        data = {
            "id": char_id.lower(),
            "full_name": full_name,
            "species": species,
            "link": char_link,
            "gallery_link": f"{base_url}/wiki/{char_id}/gallery",
            "likes": likes,
        }
        table_data.append({"pk": "character", "sk": char_id.lower(), "data": data})
    
    
        char_link = f"{data['link']}"
        res = requests.get(char_link)
        char_soup = BeautifulSoup(res.text, "html.parser")
        description_h2 = None
        try:
            description_h2 = char_soup.select('span#Description')[0].parent
        except:
            description_h2 = char_soup.select('span#History')[0].parent

        facts = []
        next = description_h2.next_sibling

        while next.name != "h2":
            if next.name == 'p':
                facts.append(next.text.strip())
            next = next.nextSibling
        
        table_data.append( { "pk": "facts", "sk": char_id.lower(), "data": { "facts": json.dumps(facts) } } )
    
    
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
