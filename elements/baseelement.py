from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import WAIT_TIME, PAUSE_TIME


class BaseElement:

    """
    Base element on webpage with unique locator
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

            with pytest.allure.step("Clicking element \"{}\"".format(self.__class__.__name__)):
                element.click()

    def set_value(self, value):
        """
        Sets the given value
        """
        pass


class Label(BaseElement):
    """
    Element presents simple text label
    """
    locator = None

    def get_value(self):
        with pytest.allure.step("Waiting for text to be available: \"{}\"".format(self.locator)):
            sleep(PAUSE_TIME)
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.locator), " "))
        return self.get_element(self.locator, By.CSS_SELECTOR).text


class DropDown(BaseElement):
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

    def get_value(self, option_type):
        return self.get_element(self.locator.format(self.name, option_type)).is_selected()
