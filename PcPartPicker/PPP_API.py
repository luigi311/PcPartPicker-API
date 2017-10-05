from json import loads as jsonloads
from bs4 import BeautifulSoup
from ._PPP_data import lookup
from requests import get

base_url = "https://uk.pcpartpicker.com/products/{}/fetch?page={}"

def _get_page(item_type, page_num, return_pagenum=False):
    """
    item_type = item type, for example, "cpu"
    page_num = page number, for example, 1
    return_pagenum = whether to return the number of pages or the html soup
    """
    r = get(base_url.format(item_type, page_num))
    parsed = jsonloads(r.content.decode("utf-8"))
    if return_pagenum:
        return parsed["result"]["paging_data"]["page_blocks"][-1]["page"]
    return BeautifulSoup(parsed["result"]["html"], "html.parser")

def get_total_pages(item_type):
    return _get_page(item_type, 1, True)

def get_item(item_type, single_page=False):
    """
    item_type = Any item in data.lookup
    single_page = Page number. False by default (False means all pages)
    """
    if item_type not in lookup:
        raise ValueError("item_type not valid")

    if single_page:
        start_page_num, total_pages = single_page, single_page
    else:
        start_page_num, total_pages = 1, _get_page(item_type, 1, True)

    parsed_html = []
    for page_num in range(start_page_num, total_pages+1):
        soup = _get_page(item_type, page_num)
        for row in soup.findAll("tr"):
            row_elements = {}
            for count, x in enumerate(row):
                try:
                    row_elements[lookup[item_type][count]] =  x.get_text().strip()
                except KeyError:
                    pass
            parsed_html.append(row_elements)

    return parsed_html
