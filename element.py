from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from baseelement import *


class MoneyValue(BaseElement):

    """Text field for money value to convert"""
    locator = "//h6[text()='Конвертация']/../../*/*/form/input"

    def set_value(self, value):
        """
        Selects text in field, deletes it and writes new value
        :param value: money value
        """
        # self.get_element().clear()
        # Workaround to clear input field due problems with different browsers
        self.get_element().send_keys(Keys.CONTROL + "a", Keys.DELETE)
        self.get_element().send_keys(value)
        self.get_element().send_keys(" ")


class SrcCurrency(CurrencyDropDown):
    """Source currency"""
    name = "converterFrom"


class DstCurrency(CurrencyDropDown):
    """Destination currency"""
    name = "converterTo"


class SrcCode(RadioGroup):
    """Type of source. Possible values: card, account or cash"""
    name = "sourceCode"
    # options = ()


class DstCode(RadioGroup):
    """Type of destination. Possible values: card, account or cash"""
    name = "destinationCode"


class ExchangeType(RadioGroup):
    """Location of money receiving. Possible values: ibank, office or atm"""
    name = "exchangeType"


class ServicePack(RadioGroup):
    """Type of service pack level. Possible values: empty, premier or first"""
    name = "servicePack"


class TimeConversion(BaseElement):
    """
    Element presents radiogroup and custom datepicker
    """

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
            with pytest.allure.step("Clicking custom date picker: \"{}\"".format(self.open_date_picker_locator)):
                self.wait_and_click(self.open_date_picker_locator, By.CSS_SELECTOR)

            # sets year
            with pytest.allure.step("Selecting year: \"{}\"".format(self.year_locator)):
                Select(self.get_element(self.year_locator, By.CSS_SELECTOR)).select_by_visible_text(str(time.year))

            # set month
            month_delta = time.month - datetime.now().month
            if month_delta != 0:
                if month_delta < 0:
                    locator = self.month_locator.format("prev")
                    month_delta = abs(month_delta)
                else:
                    locator = self.month_locator.format("next")

                with pytest.allure.step("Selecting month: \"{}\"".format(locator)):
                    while month_delta:
                        self.wait_and_click(locator)
                        month_delta -= 1

            # set day
            with pytest.allure.step("Selecting day: \"{}\"".format(self.day_locator.format(time.day))):
                self.wait_and_click(self.day_locator.format(time.day))

            # set hours
            with pytest.allure.step("Selecting hour: \"{}\"".format(self.time_locator.format('hour'))):
                Select(self.get_element(self.time_locator.format('hour'))).\
                    select_by_visible_text(time.strftime("%H"))
            # set minutes
            with pytest.allure.step("Selecting minutes: \"{}\"".format(self.time_locator.format('minute'))):
                Select(self.get_element(self.time_locator.format('minute'))).\
                    select_by_visible_text(time.strftime("%M"))

            # accept time
            with pytest.allure.step("Accepting selected time: \"{}\"".format(self.accept_date_picker_locator)):
                self.wait_and_click(self.accept_date_picker_locator, By.CSS_SELECTOR)


class Submit(BaseElement):
    """Button to submit passed data"""

    locator = "button.rates-button"

    def set_value(self, value=None):
        self.wait_and_click(by=By.CSS_SELECTOR)


class Result(BaseElement):
    """Label with result conversion value"""

    locator = "span.rates-converter-result__total-to"

    def set_value(self, value=None):
        pass

    def get_value(self):
        with pytest.allure.step("Waiting for result to be available: \"{}\"".format(self.locator)):
            sleep(PAUSE_TIME)
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.locator), " "))
        return self.get_element(self.locator, By.CSS_SELECTOR).text
