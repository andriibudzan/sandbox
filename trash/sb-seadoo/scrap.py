import re
import os
import requests
from bs4 import BeautifulSoup

from pprint import pprint

# tqmplates
template_db = {
    'year': {
        'vehicle': {
            'model': {
                'system': {
                    'part': {
                        'name': '',
                        'price': '',
                        'link': '',
                        'img_code': ''
                    }
                }
            }
        }
    }
}
template_db_img = {
    # 'V_M_S_P': file.zip
}


base_url = 'http://www.seadoopartshouse.com'
page = BeautifulSoup(requests.get(base_url).content, 'lxml')
tags = page.select('a.year-dd-link')
links = [tag.get('href') for tag in tags]
urls = [base_url + link for link in links]
# pprint(urls) # [list of urls]

urls_test = urls[:1]

 # url on a page with a models list by year
def get_data(url):
    steps_result = {}
    page = BeautifulSoup(requests.get(url).content, 'lxml')
    tags = page.select('a.pjq')
    links = [tag.get('href') for tag in tags]
    urls = [base_url + link for link in links] # url on a model systems gallery
    steps_result[1] = urls
    for url in urls:  # iterate over system parts urls
        page = BeautifulSoup(requests.get(url).content, 'lxml')
        tags = page.select('div.passname')
        links = [tag.get('href') for tag in tags]  # page with list of parts
        ulrs = [base_url + link for link in links]
        steps_result[2] = urls
        for url in urls:
            page = BeautifulSoup(requests.get(url).content, 'lxml')
            tags = page.select('div.partlistrow')
            links = [tag.get('href') for tag in tags]
            urls = [base_url + link for link in links]
            steps_result[3] = urls
            pprint(steps_result)
    return steps_result


ur = 'http://www.seadoopartshouse.com/oemparts/c/sea_doo_personal_watercraft_2018/parts'
z = get_data(ur)

pprint(z)
#
# for url in links:
#     page = BeautifulSoup(requests.get(base_url).content, 'lxml')
#     tags = page.select('a.pjq')
#     links = [base_url + tag.get('href') for tag in tags]
# pprint(links)
#


# if __name__ == '__main__':
    # pass




#

#     if url.startswith('http'):
#         response = requests.get(url)
#     else:
#         response = requests.get(base_url + url)
#     page = BeautifulSoup(response.content, 'lxml')
#
#     return page
#
# def get_tags(where):
#     pass
#
# def get_content(tag):
#     data = [tag.get(what) for tag in tags]
#     return data
#
#
# url = 'oemparts/a/sea/500cca84f870021b3c6a72cc/tower-and-bimini-top'
# links = parse_url(url, 'div.passemname a', 'href')
# pprint(links)
