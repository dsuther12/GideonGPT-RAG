# Pull data to be parsed and chunked for RAG pattern

import requests
import json
from bs4 import BeautifulSoup
import re


response = requests.get("https://eldenring.wiki.fextralife.com/Elden+Ring+Wiki")
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.select('a')

pattern = r'^/'
for link in links:
    if 'href' in link.attrs and 'target' in link.attrs:
        if re.match(pattern, link['href']):
            print(link['href'])




