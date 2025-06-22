# Pull data to be parsed and chunked for RAG pattern

import requests
import json
from bs4 import BeautifulSoup
import re

# Gets the page links in dropdown menus on the main page. E.g. Armor, Shields, Characters, etc.
def get_page_links():
    main_url = "https://eldenring.wiki.fextralife.com"
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('a')
    pattern = r'^/'
    page_links = set()
    for link in links:
        if 'href' in link.attrs and 'target' in link.attrs and re.match(pattern, link['href']):
            page_links.add(main_url + link['href'])

    return page_links

# Gets the HTML of the pages within the dropdown menu links on the main wiki page
def get_page_links_html():
    page_links = get_page_links()
    count = 0
    page_html_dict = {}
    for link in page_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        match = re.search(r'/[^/]+$', link)
        dict_keys = match.group().replace('/', '').replace('+', '_').lower()
        page_html_dict[dict_keys] = {'link': link, 'html': soup}

    return page_html_dict


pages_html_dict = get_page_links_html()










