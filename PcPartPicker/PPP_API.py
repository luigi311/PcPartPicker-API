from json import loads as jsonloads
from ._PPP_data import lookup
from bs4 import BeautifulSoup
from requests import get

base_url = "https://uk.pcpartpicker.com/products/{}/fetch?page={}"

def _get_page(part_type, page_num, return_pagenum=False):
    """
    part_type = part type, for example, "cpu"
    page_num = page number, for example, 1
    return_pagenum = whether to return the number of pages or the html soup
    """
    r = get(base_url.format(part_type, page_num))
    parsed = jsonloads(r.content.decode("utf-8"))
    if return_pagenum:
        return parsed["result"]["paging_data"]["page_blocks"][-1]["page"]
    return BeautifulSoup(parsed["result"]["html"], "html.parser")

def get_total_pages(part_type):
    return _get_page(part_type, 1, True)

def get_part(part_type, single_page=False):
    """
    part_type = Any item in data.lookup
    single_page = Page number. False by default (False means all pages)
    """
    if part_type not in lookup:
        raise ValueError("part_type not valid")

    if single_page:
        start_page_num, total_pages = single_page, single_page
    else:
        start_page_num, total_pages = 1, _get_page(part_type, 1, True)

    parsed_html = []
    for page_num in range(start_page_num, total_pages+1):
        soup = _get_page(part_type, page_num)
        for row in soup.findAll("tr"):
            row_elements = {}
            for count, value in enumerate(row):
                text = value.get_text().strip()
                try:
                    row_elements[lookup[part_type][count]] = text
                except KeyError:
                    if count == 1:
                        row_elements["name"] = text
                    elif count == len(row)-2:
                        row_elements["price"] = text
                    elif count == len(row)-3:
                        row_elements["ratings"] = text.replace("(", "").replace(")", "")
            parsed_html.append(row_elements)
    return parsed_html
