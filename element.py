from datetime import datetime
from selenium.webdriver.support.ui import Select

from baseelement import *
from params import SLEEP_TIME, WAIT_TIME


class MoneyValue(BaseElement):

    locator = "//h6[text()='Конвертация']/../../*/*/form/input"

    def set_value(self, value):
        self.get_element().clear()
        self.get_element().send_keys(value)
        self.get_element().send_keys(" ")


class SrcCurrency(CurrencyDropDown):
    name = "converterFrom"


class DstCurrency(CurrencyDropDown):
    name = "converterTo"


class SrcCode(RadioGroup):
    name = "sourceCode"
    # options = ("card", "account", "cash")


class DstCode(RadioGroup):
    name = "destinationCode"
    # options = ("card", "account", "cash")


class ExchangeType(RadioGroup):
    name = "exchangeType"
    # options = ("ibank", "office", "atm")


class ServicePack(RadioGroup):
    name = "servicePack"
    # options = ("empty", "premier", "first")


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

    def set_value(self, value=None):
        pass

    def get_value(self):
        sleep(SLEEP_TIME)
        WebDriverWait(self.page_obj.driver, WAIT_TIME).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.locator), " "))
        return self.get_element(self.locator, By.CSS_SELECTOR).text
