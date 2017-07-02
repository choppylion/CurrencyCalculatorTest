from time import sleep

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from params import SLEEP_TIME, WAIT_TIME


class BaseElement:

    """Base page class that is initialized on every page object class."""

    locator = None

    def __init__(self, page_obj):
        self.page_obj = page_obj

    def get_element(self, locator=None, by=By.XPATH):
        if locator is None:
            locator = self.locator
        return self.driver.find_element(by=by, value=locator)

    def wait_and_click(self, locator=None, by=By.XPATH):
        if locator is None:
            locator = self.locator

        sleep(SLEEP_TIME)
        element = WebDriverWait(self.page_obj.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((by, locator)))
        element.click()

    def set_value(self, value):
        """Sets the text to the value supplied"""
        raise NotImplementedError


class CurrencyDropDown(BaseElement):  # RUB CHF EUR GBP JPY USD

    name = ""
    locator = "//select[@name='{}']/../div/*/em"
    option_locator = "//select[@name='{}']/../div/div/span[contains(text(), '{}')]"

    def set_value(self, value):
        self.wait_and_click(self.locator.format(self.name, value))
        self.wait_and_click(self.option_locator.format(self.name, value))


class RadioGroup(BaseElement):

    locator = "//input[@name='{}' and @value='{}']/../span"
    name = ""

    def set_value(self, value):
        self.wait_and_click(self.locator.format(self.name, value))
