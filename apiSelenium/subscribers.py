from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Subscriber:
    def __init__(self, driver, data):
        self.data = data
        self.driver = driver
        self.subs = {}
        self.__counter = 0
        self.timeList = ['сек', 'minute', 'хвилин', 'минут', 'second']

    def GetPageNewSubscribers(self, count=0):
        self.subs = {}
        while True:
            self.driver.get(self.data.urls['notif_subs'])
            if self.driver.current_url == self.data.urls['notif_subs']:
                break

        self.__counter = 0
        while self.__counter <= 30:
            time.sleep(1)
            subs = self.driver.find_elements(
                By.XPATH, self.data.xpath['nickSubs'])

            for sub in subs:
                user = [sub.get_attribute("href"), sub.text]
                self.__counter += 1

                if user[0] not in self.subs.keys() and user[1] != "":
                    date = sub.find_element(
                        By.XPATH, self.data.xpath['dateSubs'])

                    if count == 0:
                        for t in self.timeList:
                            if t in date.text:
                                self.__counter = 0
                                self.subs[user[0]] = [
                                    user[1], user[0], date.text]
                                break
                    else:
                        self.__counter = 0
                        self.subs[user[0]] = [user[1], user[0], date.text]

                    if count != 0 and len(list(self.subs.keys())) >= count:
                        self.__counter = 100
                        break
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
