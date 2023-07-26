from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class UserManager:
    def __init__(self, driver, data):
        self.driver = driver
        self.data = data
        self.counter = 0
        self.href = None

    def GetUserChatUrl(self, urlUser):
        self.href = None
        self.counter = 0
        while self.counter < 3:
            self.driver.get(urlUser)
            try:
                subBtn = self.driver.find_element(
                    By.XPATH, self.data.xpath["btnSubscribe"])
                if "$" in subBtn.text:
                    return self.data.status_users["paid_subs"]
                subBtn.click()
            except:
                try:
                    chatBtn = self.driver.find_element(
                        By.XPATH, self.data.xpath["chatBtn"])
                    self.href = chatBtn.get_attribute("href")
                    break
                except:
                    pass

            self.counter += 1

            time.sleep(0.5)
        return self.href
