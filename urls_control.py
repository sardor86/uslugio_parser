from config import URL, BROWSER_SETTINGS

from requests import get
from bs4 import BeautifulSoup


class DataControl:
    def __init__(self):
        self.country = ''
        self.service = ''

        self.country_number = [0, 0]
        self.service_number = [0, 0]

        self.all_country = []
        self.all_service = []

        self.old_service_url = ''
        self.old_service_name = ''

        self.end = False

    def get_all_countries(self) -> None:
        content = get(URL,
                      headers={'User-Agent': BROWSER_SETTINGS}, )
        page = BeautifulSoup(content.content, 'html.parser')

        col_countries = page.find_all('div', class_='col-sm-4')
        all_countries = []

        for colm in col_countries:
            for countries in colm.find_all('a'):
                all_countries.append((countries.get_text(), URL + countries.get('href')))

        self.all_country = all_countries
        self.country_number[1] = len(all_countries)

    def get_all_services(self, url: str) -> None:
        if self.end == -1:
            self.end = True

        self.old_service_url = url

        content = get(url,
                      headers={'User-Agent': BROWSER_SETTINGS}, )
        page = BeautifulSoup(content.content, 'html.parser')

        services = page.find('div', class_='nav_cat_list')

        if not services is None:

            all_service = [(service.text, URL + service.get('href')) for service in services.find_all('a')]
            self.all_service = all_service
            self.service_number[1] = len(all_service)
        else:
            services = page.find_all('div', class_='col-sm-4')
            all_service = []
            for service in services:
                all_service_a = service.find_all('a')
                if not all_service_a is None:
                    for service_a in all_service_a:
                        all_service.append((service_a.text, URL + service_a.attrs['href']))

            if not services == []:
                self.all_service = all_service
                self.service_number[1] = len(all_service)
                if not self.end:
                    self.end = -1

    @classmethod
    def draw_list(cls, elements: list) -> None:
        index = 0

        for elem in elements:
            print(f'{index}) {elem[0]}')
            index += 1

        print(f'{index}) все')

    @classmethod
    def check_number(cls, number: list, exception: str = None) -> [int, None]:
        if number[0] == exception:
            return -1

        if not number[0].isdigit():
            return None
        result = int(number[0])

        if result < 0 or result > number[1]:
            return None

        return result

