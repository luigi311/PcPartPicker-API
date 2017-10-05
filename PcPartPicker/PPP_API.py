from json import loads as jsonloads
from bs4 import BeautifulSoup
from ._PPP_data import lookup
from requests import get

base_url = "https://uk.pcpartpicker.com/products/{}/fetch"

def get_item(item_type):
    if item_type not in lookup:
        raise ValueError("item_type not valid")

    parsed_html = []
    r = get(base_url.format(item_type))
    c = r.content
    parsed_json = jsonloads(c.decode("utf-8"))
    soup = BeautifulSoup(parsed_json["result"]["html"], "html.parser")

    for row in soup.findAll("tr"):
        row_elements = {}
        for count, x in enumerate(row):
            try:
                row_elements[lookup[item_type][count]] =  x.get_text().strip()
            except KeyError:
                pass
        parsed_html.append(row_elements)

    return parsed_html
