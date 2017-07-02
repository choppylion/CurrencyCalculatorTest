import pytest

from element import *
from params import Parameters, webdriver


@pytest.mark.usefixtures("webdriver")
class CalculatorPage:
    """
    Page Object of main currency calculator page
    """
    link = "http://www.sberbank.ru/ru/quotes/converter"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.link)

    def set_params(self, params):

        for param in Parameters:
            param_value = params[param.name]
            element = param.cls(self.driver)
            element.set_value(param_value)

    def submit(self):
        Submit(self.driver).set_value()

    def get_result(self):
        return Result(self.driver).get_value()
