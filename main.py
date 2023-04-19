from config import path
from driver import Driver
from services_and_countries import get_all_countries, get_all_services
from excel import Excel

from time import sleep


def draw_list(roster: list) -> None:
    index = 0

    for elem in roster:
        print(f'{index}) {elem[0]}')
        index += 1

    print(f'{index}) все')


def main():
    driver = Driver(path / 'drivers/chromedriver.exe', '')
    driver.log_in('', '')

    excel = Excel('data', [])

    all_countries = get_all_countries()
    max_countries_index = len(all_countries)

    draw_list(all_countries)

    country_number = input('Выберите город: ')

    if not country_number.isdigit():
        print('Вы неправильно написали номер города')
        sleep(5)
        return

    country_number = int(country_number)

    if country_number > max_countries_index:
        print('такого города нет')
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
    all_services = get_all_services(country[1])
    max_services_index = len(all_services)

    draw_list(all_services)

    service_number = input('Выберите сервис: ')

    if not service_number.isdigit():
        print('Вы неправильно написали номер города')
        sleep(5)
        return

    service_number = int(service_number)

    if service_number > max_services_index:
        print('такого сервиса нет')
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
