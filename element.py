from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

import allure

from test_conf import WAIT_TIME


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

        sleep(0.1)
        element = WebDriverWait(self.page_obj.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((by, locator)))
        element.click()

    def set_value(self, value):
        """Sets the text to the value supplied"""
        raise NotImplementedError

    def get_value(self):
        """Gets the text of the specified object"""
        raise NotImplementedError


class MoneyValue(BaseElement):

    locator = "//h6[text()='Конвертация']/../../*/*/form/input"

    def set_value(self, value):
        self.get_element().clear()
        self.get_element().send_keys(value)
        self.get_element().send_keys(" ")

    def get_value(self):
        self.get_element().get_attribute("value")


class SrcCurrency(BaseElement):  # RUB CHF EUR GBP JPY USD

    common_locator = "//select[@name='converterFrom']/../div/"
    locator = common_locator + "*/em"
    option_locator = common_locator + "div/span[contains(text(), '{}')]"

    def set_value(self, value):
        self.wait_and_click(self.locator.format(value))
        self.wait_and_click(self.option_locator.format(value))


class DstCurrency(BaseElement):  # RUB CHF EUR GBP JPY USD

    common_locator = "//select[@name='converterTo']/../div/"
    locator = common_locator + "*/em"
    option_locator = common_locator + "div/span[contains(text(), '{}')]"

    def set_value(self, value):
        self.wait_and_click(self.locator.format(value))
        self.wait_and_click(self.option_locator.format(value))


class SrcCode(BaseElement):

    locator = "//input[@name='sourceCode' and @value='{}']/../span"
    # options = ("card", "account", "cash")

    def set_value(self, value):
        self.wait_and_click(self.locator.format(value))


class DstCode(BaseElement):

    locator = "//input[@name='destinationCode' and @value='{}']/../span"
    # options = ("card", "account", "cash")

    def set_value(self, value):
        self.wait_and_click(self.locator.format(value))


class ExchangeType(BaseElement):

    locator = "//input[@name='exchangeType' and @value='{}']/../span"
    # options = ("ibank", "office", "atm")

    def set_value(self, value):
        self.wait_and_click(self.locator.format(value))


class ServicePack(BaseElement):

    locator = "//input[@name='servicePack' and @value='{}']/../span"
    # options = ("empty", "premier", "first")

    def set_value(self, value):
        self.wait_and_click(self.locator.format(value))


class TimeConversion(BaseElement):

    locator = "//input[@name='converterDateSelect' and @value='{}']/../span"

    open_date_picker_locator = "button.rates-date-picker__trigger"
    year_locator = "select.ui-datepicker-year"
    month_locator = "//div[@id='ui-datepicker-div']/div/a[@data-handler='{}']"
    day_locator = "//div[@id='ui-datepicker-div']//a[contains(text(), '{}')]"
    time_locator = "//select[@data-unit='{}']"
    accept_date_picker_locator = "span.rates-button.rates-button_converter-datepicker-hide"

    def set_value(self, value):
        if value == "current":
            self.wait_and_click(self.locator.format("current"))
        else:
            time = datetime.strptime(value, '%d.%m.%Y %H:%M')
            self.wait_and_click(self.locator.format("select"))

            # open time picker
            self.wait_and_click(self.open_date_picker_locator, By.CSS_SELECTOR)

            # set year
            Select(self.get_element(self.year_locator, By.CSS_SELECTOR)).select_by_visible_text(str(time.year))

            # set month
            month_delta = time.month - datetime.now().month
            if month_delta != 0:
                if month_delta < 0:
                    locator = self.month_locator.format("prev")
                    month_delta = abs(month_delta)
                else:
                    locator = self.month_locator.format("next")

                while month_delta:
                    self.wait_and_click(locator)
                    month_delta -= 1

            # set day
            self.wait_and_click(self.day_locator.format(time.day))

            # set hours
            Select(self.get_element(self.time_locator.format('hour'))).select_by_visible_text(time.strftime("%H"))
            # set minutes
            Select(self.get_element(self.time_locator.format('minute'))).select_by_visible_text(time.strftime("%M"))

            # accept time
            self.wait_and_click(self.accept_date_picker_locator, By.CSS_SELECTOR)


class Submit(BaseElement):

    locator = "button.rates-button"

    def set_value(self, value=None):
        self.wait_and_click(by=By.CSS_SELECTOR)


class Result(BaseElement):

    locator = "span.rates-converter-result__total-to"

    def get_value(self):
        sleep(0.1)
        WebDriverWait(self.page_obj.driver, WAIT_TIME).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.locator), " "))
        return self.get_element(self.locator, By.CSS_SELECTOR).text
