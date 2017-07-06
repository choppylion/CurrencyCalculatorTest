from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import WAIT_TIME, PAUSE_TIME #, webdriver


class BaseElement:

    """
    Base page class that is initialized on every page object class.
    """

    #: base locator
    locator = None

    def __init__(self, webdriver):
        """
        :param webdriver: selenium webdriver instance
        """
        self.driver = webdriver

    def get_element(self, locator=None, by=By.XPATH):
        """
        Finds element on form by specific locator
        :param locator: path to element
        :param by: type of locator
        :return: found element
        """

        if locator is None:
            locator = self.locator
        return self.driver.find_element(by=by, value=locator)

    def wait_and_click(self, locator=None, by=By.XPATH):
        """
        Waits specific time until element to be clickable and click it
        :param locator: path to element
        :param by: type of locator
        """
        if locator is None:
            locator = self.locator

        with pytest.allure.step("Waiting element \"{}\" to be clickable".format(self.__class__.__name__)):
            sleep(PAUSE_TIME)
            element = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.element_to_be_clickable((by, locator)))
            element.click()

    def set_value(self, value):
        """
        Sets the given value
        """
        raise NotImplementedError


class CurrencyDropDown(BaseElement):

    """
    Element presents dropdown list with following item: RUB CHF EUR GBP JPY USD
    """

    name = None
    locator = "//select[@name='{}']/../div/*/em"
    option_locator = "//select[@name='{}']/../div/div/span[contains(text(), '{}')]"

    def set_value(self, value):
        """
        Clicks on main dropdown element and selects given item
        :param value: value of item that has to be selected
        """
        self.wait_and_click(self.locator.format(self.name, value))
        self.wait_and_click(self.option_locator.format(self.name, value))


class RadioGroup(BaseElement):

    """
    Element presents group of radiobuttons
    """

    name = None
    locator = "//input[@name='{}' and @value='{}']/../span"

    def set_value(self, value):
        """
        Clicks on radiobutton
        :param value: value of item that has to be selected
        """
        self.wait_and_click(self.locator.format(self.name, value))
