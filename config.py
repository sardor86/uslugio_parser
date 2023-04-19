from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path


BROWSER_SETTINGS = 'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                   'Chrome/51.0.2704.103 Safari/537.36'

URL = 'https://uslugio.com'
LOG_IN_URL = 'https://uslugio.com/users/login'

path = Path(__file__).parent


class BaseDriver(webdriver.Chrome):
    def __init__(self, driver_path: str, url: str) -> None:
        options = Options()
        options.add_argument(
            BROWSER_SETTINGS)

        super().__init__(executable_path=driver_path, chrome_options=options)
        print('Браузер готов')

        self.url = url

        self.phone_number = []
        self.user_name = []

    def __del__(self):
        self.close()
        self.quit()
        print('Браузер закрыт')
