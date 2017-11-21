from json import loads as jsonloads
from ._PPP_data import lookup
from bs4 import BeautifulSoup
from requests import get

base_url = "https://pcpartpicker.com/products/cpu/fetch?k={}&page={}"
sockets={27:"AM1", 3:"AM3" ,4:"AM3+",6:"AM3/AM2+", 
         33:"AM4", 8:"BGA413", 10:"BGA559", 
         25:"BGA1023", 32:"C32", 20:"FM1", 
         23:"FM2", 26:"FM2+", 31:"G34", 12:"LGA771",
         13:"LGA775", 24:"LGA1150", 30:"LGA1151", 
         14:"LGA1155", 15:"LGA1156", 37:"LGA1356",
         16:"LGA1366", 21:"LGA2011", 28:"LGA2011-3",
         35:"LGA2066", 18:"PGA988", 36:"TR4" }

def _get_page(socket, page_num, return_pagenum=False):
    """
    socket = part type, for example, "cpu"
    page_num = page number, for example, 1
    return_pagenum = whether to return the number of pages or the html soup
    """
    r = get(base_url.format(socket, page_num))
    parsed = jsonloads(r.content.decode("utf-8"))
    if return_pagenum:
        return parsed["result"]["paging_data"]["page_blocks"][-1]["page"]
    return BeautifulSoup(parsed["result"]["html"], "html.parser")

def get_total_pages(socket):
    return _get_page(socket, 1, True)

def get_part(socket, single_page=False):
    """
    socket = Any item in data.lookup
    single_page = Page number. False by default (False means all pages)
    """

    if single_page:
        start_page_num, total_pages = single_page, single_page
    else:
        start_page_num, total_pages = 1, _get_page(socket, 1, True)

    parsed_html = []
    for page_num in range(start_page_num, total_pages+1):
        soup = _get_page(socket, page_num)
        for row in soup.findAll("tr"):
            row_elements = {}
            for count, value in enumerate(row):
                text = value.get_text().strip()
                try:
                    row_elements[lookup[socket][count]] = text
                except KeyError:
                    if count == 1:
                        row_elements["name"] = text
                        row_elements["socket"] = sockets[socket]
                    elif count == len(row)-2:
                        row_elements["price"] = text
                    elif count == len(row)-3:
                        row_elements["ratings"] = text.replace("(", "").replace(")", "")
            parsed_html.append(row_elements)
            
    return parsed_html
