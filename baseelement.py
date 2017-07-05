from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import WAIT_TIME, PAUSE_TIME #, webdriver


class BaseElement:

    """Base page class that is initialized on every page object class."""

    locator = None

    def __init__(self, webdriver):
        self.driver = webdriver

    def get_element(self, locator=None, by=By.XPATH):
        if locator is None:
            locator = self.locator
        return self.driver.find_element(by=by, value=locator)

    def wait_and_click(self, locator=None, by=By.XPATH):
        if locator is None:
            locator = self.locator

        with pytest.allure.step("Waiting element \"{}\" to be clickable".format(self.__class__.__name__)):
            sleep(PAUSE_TIME)
            element = WebDriverWait(self.driver, WAIT_TIME).until(
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
