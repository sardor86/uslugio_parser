from config import path, Config
from driver import Driver
from urls_control import get_all_countries, get_all_services
from excel import Excel

from time import sleep


def draw_list(roster: list) -> None:
    index = 0

    for elem in roster:
        print(f'{index}) {elem[0]}')
        index += 1

    print(f'{index}) все')


class Number:
    def __init__(self, number: str, max_number: int, all_countries: list, exception: str = None) -> None:
        self.all_countries = all_countries
        self.number = number
        self.max_number = max_number
        self.exception = exception

    def check_number(self) -> [int, None]:
        if self.number == self.exception:
            return -1

        if not self.number.isdigit():
            return None
        self.number = int(self.number)

        if self.number < 0 or self.number > self.max_number:
            return None

        return self.number

    def draw_list(self) -> None:
        index = 0

        for elem in self.all_countries:
            print(f'{index}) {elem[0]}')
            index += 1

        print(f'{index}) все')


def main():
    # preparation chrome drivers
    config = Config(path / '.env')

    driver = Driver(path / 'drivers/chromedriver.exe', '')
    driver.log_in(config.email, config.password)

    # get country
    all_countries = get_all_countries()
    max_countries_index = len(all_countries)

    draw_list(all_countries)

    country_number = input('Выберите город: ')

    country_number = check_number(country_number, max_countries_index)

    if country_number is None:
        print('Вы неправильно написали номер города')
        sleep(5)
        return

    if country_number == max_countries_index:
        all_countries = get_all_countries()

        excel = Excel('data', [country[0] for country in all_countries])

        column_sequence = 0

        for country in all_countries:
            print(country[0])
            for service in get_all_services(country[1]):
                print(service[0])
                driver.url = service[1]
                driver.get_phone_and_name_service()

                excel.save_data(country[0], service[0], column_sequence, driver.user_name, driver.phone_number)

                column_sequence += 1

        excel.save()

        return

    country = all_countries[country_number]

    # get service
    all_services = get_all_services(country[1])
    max_services_index = len(all_services)

    draw_list(all_services)

    service_number = input('Выберите сервис: ')

    service_number = check_number(service_number, max_services_index)

    if service_number is None:
        print('Вы неправильно написали номер сервиса')
        sleep(5)
        return

    if service_number == max_services_index:

        excel = Excel('data', [country[0]])

        column_sequence = 0

        for service in get_all_services(country[1]):
            print(service[0])
            driver.url = service[1]

            driver.get_phone_and_name_service()

            excel.save_data(country[0], service[0], column_sequence, driver.user_name, driver.phone_number)

            column_sequence += 1
        excel.save()

    else:
        service = get_all_services(country[1])[service_number]

        excel = Excel('data', [country[0]])

        driver.url = service[1]

        driver.get_phone_and_name_service()

        excel.save_data(country[0], service[0], 0, driver.user_name, driver.phone_number)
        excel.save()


if __name__ == '__main__':
    main()
