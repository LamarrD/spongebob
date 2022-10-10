import requests
import boto3
import os
from bs4 import BeautifulSoup


table_name = os.getenv('TABLE_NAME')
table = boto3.resource('dynamodb').Table(table_name)


# Data sourced from SpongeBob's Fandom Wiki

def handler(event, context):
    base_url = "https://spongebob.fandom.com"
    res = requests.get(f"{base_url}/wiki/List_of_characters/Main")

    soup = BeautifulSoup(res.text, 'html.parser')
    main_char_divs = soup.find_all("div", {"class": "bounceme"})
    main_char_ids = [ main.attrs['id'] for main in main_char_divs ]

    for main_char_id in main_char_ids:
        char_link = f"{base_url}/wiki/{main_char_id}"
        res = requests.get(char_link)
        char_soup = BeautifulSoup(res.text, 'html.parser')

        data = {
            "full_name": char_soup.find_all('h2', {'data-source': 'name'})[0].text,
            "residence": char_soup.find_all('div', {'data-source': 'residence'})[0].find_all('div')[0].text,
            "job": char_soup.find_all('div', {'data-source': 'occupation(s)'})[0].find_all('div')[0].text,
            "gender": char_soup.find_all('div', {'data-source': 'gender'})[0].find_all('div')[0].text,
            "color": char_soup.find_all('div', {'data-source': 'color'})[0].find_all('div')[0].text,
            "species": char_soup.find_all('div', {'data-source': 'species'})[0].find_all('div')[0].text,
            "link": char_link,
            "gallery_link": f"{base_url}/wiki/{main_char_id}/gallery",
        }
        # Add to DynamoDB
        table.put_item(
            Item={
                "pk": "character",
                "sk": main_char_id.lower(),
                "data": data
            }
        )



if __name__ == "__main__":
    handler(None, None)