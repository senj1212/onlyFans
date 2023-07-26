from selenium import webdriver
from selenium.webdriver.common.by import By
import threading


class Authorization:
    def __init__(self, dataConfig, driver=None):
        self.driver = driver if driver is not None else self.__createDriver()
        self.dc = dataConfig
        self.email = None
        self.authCheck = False

    def __createDriver(self):
        driver = webdriver.Firefox(
            executable_path="drivers/geckodriver")
        driver.implicitly_wait(10)
        return driver

    def auth(self, user_data):
        self.email = user_data[0]

        self.driver.get(self.dc.urls["main"])

        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")
        btn_auth = self.driver.find_element(By.XPATH, self.dc.xpath['btnAuth'])

        email_input.send_keys(user_data[0])
        password_input.send_keys(user_data[1])
        btn_auth.click()
        self.waitAuth()

    def waitAuth(self):
        t = threading.Thread(target=self.__waitAuth)
        t.start()

    def __waitAuth(self):
        while not self.authCheck:
            for cookie in self.driver.get_cookies():
                if "auth_id" == cookie['name']:
                    self.authCheck = True
                    break
