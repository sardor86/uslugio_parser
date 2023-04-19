from config import BaseDriver, LOG_IN_URL

from time import sleep
from tqdm import tqdm

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Driver(BaseDriver):
    def scroll_down(self, down_counter: int) -> None:
        for i in range(down_counter):
            self.find_element(By.TAG_NAME, "html").send_keys(Keys.DOWN)

    def get_phone_and_name_service(self):
        self.get(self.url)
        self.scroll_down(500)

        content = self.find_elements(By.CLASS_NAME, 'items_n')

        for data in tqdm(content):
            while True:
                try:
                    bottom = data.find_element(By.CLASS_NAME, 'item-bottom')
                    bottom.find_element(By.CLASS_NAME, 'showphone1').click()

                    self.user_name.append(data.find_element(By.CLASS_NAME,
                                                            'phoneline').find_element(By.TAG_NAME, 'span').text)
                    self.phone_number.append(bottom.find_element(By.TAG_NAME, 'a').text)
                    sleep(.5)
                    break
                except NoSuchElementException:
                    sleep(.5)

    def log_in(self, email: str, password: str) -> bool:
        self.get(LOG_IN_URL)
        sleep(3)

        self.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/form/div[1]/input').send_keys(email)
        self.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/form/div[2]/input').send_keys(password)

        self.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/form/button').click()

        try:
            self.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/form/div[3]/ul/li')
            return False
        except NoSuchElementException:
            sleep(2)
            return True
