from config import path, Config
from driver import Driver
from urls_control import DataControl
from excel import Excel

from time import sleep


def main():
    # preparation chrome drivers
    config = Config(path / '.env')

    driver = Driver(path / 'drivers/chromedriver.exe', '')
    driver.log_in(config.email, config.password)

    data = DataControl()

    data.get_all_countries()
    data.draw_list(data.all_country)

    data.country_number[0] = input('Выберите город: ')
    data.country_number[0] = data.check_number(data.country_number)

    if data.country_number[0] is None:
        print('Вы ввели неверный номер')
        sleep(5)
        return

    if data.country_number[0] == data.country_number[1]:
        excel = Excel('data', [country[0] for country in data.all_country])

        column_sequence = 0

        for country in data.all_country:
            print(country[0])

            data.get_all_services(country[1])
            for service in data.all_service:
                driver.user_name = []
                driver.phone_number = []

                driver.url = service[1]
                driver.get_phone_and_name_service()

                excel.save_data(country[0], service[0], column_sequence, driver.user_name, driver.phone_number)
                column_sequence += 1
        excel.save()
        return

    data.country = data.all_country[data.country_number[0]]
    data.get_all_services(data.country[1])

    while True:
        if data.end is True:
            service = data.all_service[data.service_number[0]]
            excel = Excel('data', [data.country[0]])
            driver.url = service[1]
            driver.get_phone_and_name_service()

            excel.save_data(data.country[0], service[0], 0, driver.user_name, driver.phone_number)
            excel.save()
            return

        data.draw_list(data.all_service)
        print('n) начать парсинг')

        data.service_number[0] = input('Выберите сервис: ')
        data.service_number[0] = data.check_number(data.service_number, exception='n')

        if data.service_number[0] is None:
            print('Вы ввели неправильный номер')
            sleep(5)
            return

        if data.service_number[0] == -1:
            excel = Excel('data', [data.country[0]])
            driver.url = data.old_service_url
            driver.get_phone_and_name_service()

            excel.save_data(data.country[0], data.old_service_name, 0, driver.user_name, driver.phone_number)
            excel.save()
            return

        if data.service_number[0] == data.service_number[1]:
            excel = Excel('data', [data.country[0]])

            column_sequence = 0

            for service in data.all_service:
                driver.user_name = []
                driver.phone_number = []

                driver.url = service[1]
                driver.get_phone_and_name_service()

                excel.save_data(data.country[0], service[0], column_sequence, driver.user_name, driver.phone_number)
                column_sequence += 1
            excel.save()
            return

        if not data.end is True:
            data.old_service_name = data.all_service[data.service_number[0]][0]
            data.get_all_services(data.all_service[data.service_number[0]][1])


if __name__ == '__main__':
    main()
