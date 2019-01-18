import requests
from bs4 import BeautifulSoup
import json

ROOT_URL = "https://stackoverflow.com"

SOF_TAG_URL = ROOT_URL + "/tags?page={}&tab=popular"
tags = {}

for i in range(1, 6):
    url = SOF_TAG_URL.format(i)
    html = requests.get(url).content

    soup = BeautifulSoup(html, 'lxml')

    for tag_html in soup.select('div.grid-layout--cell.tag-cell > a'):
        tags[tag_html.get_text()] = ROOT_URL + tag_html['href']

with open('data/tags.json', 'w', encoding='utf8') as fp:
    json.dump(tags, fp, ensure_ascii=False)
