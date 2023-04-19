from config import URL, BROWSER_SETTINGS

from requests import get
from bs4 import BeautifulSoup


def get_all_countries() -> list:
    content = get(URL,
                  headers={'User-Agent': BROWSER_SETTINGS}, )
    page = BeautifulSoup(content.content, 'html.parser')

    col_countries = page.find_all('div', class_='col-sm-4')
    all_countries = []

    for colm in col_countries:
        for countries in colm.find_all('a'):
            all_countries.append((countries.get_text(), URL + countries.get('href')))

    return all_countries


def get_all_services(url: str) -> list:
    content = get(url,
                  headers={'User-Agent': BROWSER_SETTINGS}, )
    page = BeautifulSoup(content.content, 'html.parser')

    services = page.find('div', class_='nav_cat_list')

    return [(service.text, URL + service.get('href')) for service in services.find_all('a')]
