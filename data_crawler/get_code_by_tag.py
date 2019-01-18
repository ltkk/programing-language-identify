import requests
from bs4 import BeautifulSoup
from data_crawler.utils import load_json_file, save_list_to_file
from data_crawler.data_prep import CodePreprocess
from selenium import webdriver
import traceback
from time import sleep
from selenium.webdriver.firefox.options import Options
import os

options = Options()
options.add_argument('--headless')

URL_CONDITION = "?sort=votes&page={}&pagesize=15"
ROOT_URL = "https://stackoverflow.com"
tags = load_json_file('data/tags.json')

tags_class = load_json_file('data/lang_code.json')

driver = webdriver.Firefox()
driver.implicitly_wait(30)


def get_code_list(crawl_url, css_class, prep=True):
    blocks_code = []
    # html = requests.get(crawl_url).content
    driver.get(crawl_url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for block_code in soup.select('pre.' + css_class):
        block_code = block_code.get_text()
        if prep:
            block_code = CodePreprocess().preprocess(block_code)
        if len(block_code) > 50:
            blocks_code.append(block_code)
    return blocks_code


for tag, url in tags.items():
    tag_class = tags_class[tag]
    if tag_class + '.txt' in os.listdir('data'):
        print('Exist data for: ' + tag + ' Tag!')
        continue
    print('Crawl data for: ' + tag + ' Tag!')
    text_codes = []
    for i in range(1, 20):
        crawl_url = url + URL_CONDITION.format(i)
        html = requests.get(crawl_url)
        if html.status_code != 200:
            print('Too many requests error!...')
            sleep(100)
        soup = BeautifulSoup(html.content, 'lxml')
        soup = soup.select_one('div#questions')
        for link in soup.select('a.question-hyperlink'):
            try:
                # print(link['href'])
                text_codes += get_code_list(ROOT_URL + link['href'], tag_class)
            except:
                traceback.print_exc()
    save_list_to_file(text_codes, 'data/' + tag_class + '.txt')
    print('Crawl ' + str(len(text_codes)) + ' ' + tag + ' code Tag!')

driver.close()
