import re
import os
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import threading
import pandas as pd
import logging

# find all urls, mathcing templates for further parsing
def get_soup(url):
    """ takes a url or link and returns BeautifulSoup object """
    base_url = 'https://www.seadoopartshouse.com'
    if not url.startswith('http'):
        url = base_url + url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup

def find_links(soup, template):
    """
    searching all <a>-tager objects and extracts href attr
    takes:
        soup: BeautifulSoup object
        tempplate: regular expression for comparison with href attr
    returns:
        list of links, which match template
    """
    list_of_links = [x.get('href') for x in soup.find_all('a')]
    return [x for x in list_of_links if re.fullmatch(template, x)]


# looking for urls
#
# on every step format of links quite similar and saves to new list(),
# so we can save those lists to a different files on hard drive for next
# operations
"""
# ALL THIS OPERATIONS ALREADY DONE
# step 1
base_url = 'https://www.seadoopartshouse.com'
p = get_soup(base_url)
links_step1 = find_links(p, '.*\/(oemparts)\/.\/(.+)(watercraft|boat)(.*)(\d{4})\/(parts)')
# found 41 links for 1.27 s

# step 2
links_step2 = []
for lnk in links_step1:
    p = get_soup(lnk)
    links_step2.extend(find_links(p, '.*\/(oemparts)\/l?\/(sea)\/(.{24})\/\d{4}-(.*)'))
# found 536 links for 35.8 s

# step 3
links_step3 = []
for lnk in links_step2:
    p = get_soup(lnk)
    links_step3.extend(find_links(p, '.*\/(oemparts)\/.?\/(sea)\/(.{24})\/(.*-?)*'))
# found 15332 links for 8 min 9 s


for i, list in enumerate([links_step1, links_step2, links_step3]):
    with open(path + f'\\urls_step_{i}.txt', 'w') as f:
        for item in links_step3:
            f.write(item + '\n')
"""

# extracting data from pages
def parts_data_cleaning(data):
    """ some cleaning on the extracted data """
    # ex: {'code': '409901800', 'name': 'Tubing 13 mm', 'price': '$2.95', 'ref': '830'}
    try:
        data['code'] = int(data['code'])
    except:
        data['code'] = ''
    try:
        data['price'] = float(data['price'].replace('$', '')) if data['price'].startswith('$') else int(data['price'])
    except:
        data['price'] = ''
    return data

def header_data_cleaning(data):
    """ some cleaning on the extracted data """
    # ex: {'oemparts': 'OEM Parts',  'producer': 'Sea-Doo',
    # 'vehicle': 'Watercraft', 'year': '2019',
    # 'model': '2019 Sea-Doo FISH PRO'}
    data['year'] = int(data['year'])
    data['model'] = ' '.join(data['model'].split()[2:])
    data['system'] = data['system'].split(sep=f' {data["model"]} ')[-1]
    return data


def extract_data(page):
    """ destination page parsing and collecting data """
    storage = []
    parts = ['ref', 'name', 'code', 'price'] # parts names to be written to DB
    # data to be extracted from header
    header = ['oemparts', 'producer', 'vehicle', 'year', 'model', 'system', '_']
    parts_data = page.find_all(class_='partlistrow')
    header_data = list(page.find_all(id='partheader')[0].stripped_strings)
    header_dict = header_data_cleaning(dict(zip(header, header_data)))
    for tag in parts_data:
        parts_dict = parts_data_cleaning(dict(zip(parts, list(tag.stripped_strings))))
        storage.append({**header_dict, **parts_dict})
    return storage


def thread_function(urls, general_storage, name):
    # page = BeautifulSoup(requests.get(url).content)
    url = urls.pop()
    # logging.info(f'thread {name:>5}: parsing new url')
    page = get_soup(url)
    data = extract_data(page)
    # logging.info(f'thread {name:>5}: data extracted')
    general_storage.extend(data)
    logging.info(f'thread {name:>5}: data added to storage')


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    general_storage = []
    with open('urls_for_parsing.txt', 'r') as f:
        links = f.read().splitlines()
        links_total = len(links)

    threads = []
    while links:
        for i in range(10):
            # url = links.pop()
            logging.info(f'thread {i+1:>5} ctrated and started')
            x = threading.Thread(target=thread_function, args=(links, general_storage, i+1))
            threads.append(x)
            x.start()
            logging.info(f'thread {i+1:>5} finished')
            logging.info(f'\n= REMAINING {len(links)} OUT OF {links_total} =\n')

        for idx, thread in enumerate(threads):
            thread.join()

    df = pd.DataFrame(general_storage)
    df.to_excel('seadoo_db_test.xlsx', index=False)
    logging.info(f'database saved')
