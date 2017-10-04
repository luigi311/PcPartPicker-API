from bs4 import BeautifulSoup
from .data import lookup
import requests
import json

base_url = "https://uk.pcpartpicker.com/products/{}/fetch"

def print_first_page(item_type):
    parsed_html = []

    r = requests.get(base_url.format(item_type))
    c = r.content
    parsed_json = json.loads(c.decode("utf-8"))
    soup = BeautifulSoup(parsed_json["result"]["html"], "html.parser")

    for row in soup.findAll("tr"):
        row_elements = []
        for x in row:
            row_elements.append(x.get_text().strip())
        parsed_html.append(row_elements)

    for item in parsed_html:
        item_dict = lookup[item_type]
        for k in item_dict:
            print(item_dict[k] + ": " + item[k])
        print("\n")
