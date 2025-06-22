# Pull data to be parsed and chunked for RAG pattern
import asyncio
import aiohttp
import requests
import json
from bs4 import BeautifulSoup
import re

# Gets the page links in dropdown menus on the main page. E.g. Armor, Shields, Characters, etc.
async def get_page_links(session, main_url):
    async with session.get(main_url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        links = soup.select('a')
        pattern = r'^/'
        page_links = set()
        for link in links:
            if 'href' in link.attrs and 'target' in link.attrs and re.match(pattern, link['href']):
                page_links.add(main_url + link['href'])

        return page_links

# Gets the HTML of the pages within the dropdown menu links on the main wiki page
async def get_page_links_html(session, link):
    async with session.get(link) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        match = re.search(r'/[^/]+$', link)
        dict_key = match.group().replace('/', '').replace('+', '_').lower()

        return {dict_key: {'link': link, 'html': soup}}

# Main function to control asynchronous behavior. May need to adjust accordingly based on if we pull data from more child endpoints E.g Specific weapons inside the 'Weapons' page
async def main():
    async with aiohttp.ClientSession() as session:
        main_url = "https://eldenring.wiki.fextralife.com"
        page_links = await get_page_links(session, main_url)
        tasks = []
        page_html_dict = {}
        for link in page_links:
            task = asyncio.create_task(get_page_links_html(session, link))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        page_html_dict = {}
        for result in results:
            page_html_dict.update(result)
    
    print(page_html_dict.keys())



def extract_page_data(pages):
    for k, v in pages.items():
        print(k)


asyncio.run(main())

# pages_html_dict = get_page_links_html()

# extract_page_data(pages_html_dict)










