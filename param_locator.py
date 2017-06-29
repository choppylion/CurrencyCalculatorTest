from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class ParamLocator:

    locator = None

    def __init__(self, driver):
        self.driver = driver

    def get_element(self, by=By.XPATH, locator=None):
        if locator is None:
            locator = self.locator
        return self.driver.find_element(by=by, value=locator)

    def get_value(self):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError


class MoneyValue(ParamLocator):

    locator = "//h6[text()='Конвертация']/../../*/*/form/input"

    def set_value(self, value):
        self.get_element().clear()
        self.get_element().send_keys(value)
        self.get_element().submit()

    def get_value(self):
        self.get_element().getAttribute("value")


class SrcCurrency(ParamLocator):  # RUB CHF EUR GBP JPY USD

    common_locator = "//select[@name='converterFrom']/../div/"
    locator = common_locator + "*/em"
    option_locator = common_locator + "div/span[contains(text(),'{}')]"

    def set_value(self, value):
        self.get_element().click()
        self.get_element(self.option_locator.format(value)).click()


class DstCurrency(ParamLocator):  # RUB CHF EUR GBP JPY USD

    common_locator = "//select[@name='converterTo']/../div/"
    locator = common_locator + "*/em"
    option_locator = common_locator + "div/span[contains(text(),'{}')]"

    def set_value(self, value):
        self.get_element().click()
        self.get_element(self.option_locator.format(value)).click()


class SrcCode(ParamLocator):

    locator = "//input[@name='sourceCode' and @value='{}']/../span"
    # options = ("card", "account", "cash")

    def set_value(self, value):
        self.get_element(self.locator.format(value)).click()


class DstCode(ParamLocator):

    locator = "//input[@name='destinationCode' and @value='{}']/../span"
    # options = ("card", "account", "cash")

    def set_value(self, value):
        self.get_element(self.locator.format(value)).click()


class ExchangeType(ParamLocator):

    locator = "//input[@name='exchangeType' and @value='{}']/../span"
    # options = ("ibank", "office", "atm")

    def set_value(self, value):
        self.get_element(self.locator.format(value)).click()


class ServicePack(ParamLocator):

    locator = "//input[@name='servicePack' and @value='{}']/../span"
    # options = ("empty", "premier", "first")

    def set_value(self, value):
        self.get_element(self.locator.format(value)).click()


class TimeConversion(ParamLocator):

    locator = "//input[@name='converterDateSelect' and @value='{}']/../span"

    open_date_picker_locator = "css=button.rates-date-picker__trigger"
    year_locator = "css=select.ui-datepicker-year"
    month_locator = "//div[@id='ui-datepicker-div']/div/a[@data-handler='{}']"
    day_locator = "//div[@id='ui-datepicker-div']//a[contains(text(), '{}')]"
    time_locator = "//select[@data-unit='{}']"
    accept_date_picker_locator = "css=span.rates-button.rates-button_converter-datepicker-hide"

    def set_value(self, value):
        time = value

        if time == "current":
            self.get_element(self.locator.format("current")).click()
        else:
            self.get_element(self.locator.format("select")).click()

            # open time picker
            self.get_element(By.CSS_SELECTOR, self.open_date_picker_locator).click()

            # set year
            Select(self.get_element(By.CSS_SELECTOR, self.year_locator).select_by_visible_text(time.year))

            # set month
            month_delta = time.month - datetime.now().month
            if month_delta != 0:
                if month_delta > 0:
                    shift_month_button = self.get_element(By.CSS_SELECTOR, self.month_locator.format("prev"))
                else:
                    shift_month_button = self.get_element(By.CSS_SELECTOR, self.month_locator.format("next"))
                    month_delta = abs(month_delta)

                while month_delta:
                    shift_month_button.click()
                    month_delta -= 1

            # set day
            self.get_element(self.day_locator.format(time.day)).click()

            # set hours
            Select(self.get_element(self.time_locator.format('hour')).
                   select_by_visible_text(time.hour))
            # set minutes
            Select(self.get_element(self.time_locator.format('minute')).
                   select_by_visible_text(time.minute))

            # accept time
            self.driver.find_element_by_css_selector(self.accept_date_picker_locator).click()


class Submit(ParamLocator):

    locator = "css=button.rates-button"
    result_locator = "css=span.rates-converter-result__total-to"

    def set_value(self, value=None):
        self.driver.find_element_by_css_selector(self.locator).click()

    def get_value(self):
        self.driver.find_element_by_css_selector(self.result_locator).text()

