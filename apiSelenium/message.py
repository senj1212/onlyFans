from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class MessageManager():
    def __init__(self, driver, data):
        self.driver = driver
        self.data = data

    def CheckLastMessage(self):
        lastFromUser = False
        lastDayCheck = False

        time.sleep(2)
        messages = self.driver.find_elements(
            By.XPATH, self.data.xpath["chatMessage"])
        if len(messages) > 1:
            timeLine = self.driver.find_elements(
                By.XPATH, self.data.xpath["chatTimeLine"])[-1]

            if any(map(str.isdigit, timeLine.text)):
                lastDayCheck = True

            lastMSG = messages[-1]

            date = lastMSG.find_element(
                By.XPATH, self.data.xpath["chatTimeMsg"])

            if "m-from-me" not in lastMSG.get_attribute("class"):
                lastFromUser = True

            if lastFromUser:
                return False
            elif lastDayCheck:
                return True
            else:
                return False

        return True

    def SendMessage(self, pageUrl, message):
        self.driver.get(pageUrl)
        if self.CheckLastMessage():
            try:
                input = self.driver.find_element(
                    By.XPATH, self.data.xpath["chatInput"])
                input.send_keys(message)
                input.send_keys(Keys.RETURN)
                print(f"Send message: {message}")
            except:
                return False
            return True
        return False
