from datetime import datetime

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from elements.base_elements import *


class MoneyValue(BaseElement):
    """
    Text field for money value to convert
    """
    locator = "//h6[text()='Конвертация']/../../*/*/form/input"

    def set_value(self, value):
        """
        Selects text in field, deletes it and writes new value
        :param value: money value
        """
        with pytest.allure.step("Writing \"{}\" to element \"{}\"".format(value, self.__class__.__name__)):
            # self.get_element().clear()
            # Workaround to clear input field due problems with different browsers
            self.get_element().send_keys(Keys.CONTROL + "a", Keys.DELETE)
            self.get_element().send_keys(str(value))
            self.get_element().send_keys(" ")


class SrcCurrency(DropDown):
    """Source currency"""
    name = "converterFrom"


class DstCurrency(DropDown):
    """Destination currency"""
    name = "converterTo"


class SrcCode(RadioGroup):
    """Type of source. Possible values: card, account or cash"""
    name = "sourceCode"


class DstCode(RadioGroup):
    """Type of destination. Possible values: card, account or cash"""
    name = "destinationCode"


class ExchangeType(RadioGroup):
    """Location of money receiving. Possible values: ibank, office or atm"""
    name = "exchangeType"


class ServicePack(RadioGroup):
    """Type of service pack level. Possible values: empty, premier or first"""
    name = "servicePack"


class DatePicker(BaseElement):
    """
    Element presents radiogroup and custom datepicker
    """
    locator = None
    open_date_picker_locator = None
    fmt = '%d.%m.%Y'

    year_locator = "select.ui-datepicker-year"
    month_locator = "//div[@id='ui-datepicker-div']/div/a[@data-handler='{}']"
    day_locator = "//div[@id='ui-datepicker-div']//a[contains(text(), '{}')]"

    def set_value(self, value):
        raise NotImplementedError

    def select_date(self, date_time):
        # open date_time picker
        with pytest.allure.step("Clicking custom date picker: \"{}\"".format(self.open_date_picker_locator)):
            self.wait_and_click(self.open_date_picker_locator, By.XPATH)

        # sets year
        with pytest.allure.step("Selecting year: \"{}\"".format(self.year_locator)):
            Select(self.get_element(self.year_locator, By.CSS_SELECTOR)).select_by_visible_text(str(date_time.year))

        # set month
        month_delta = date_time.month - datetime.now().month
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
        with pytest.allure.step("Selecting day: \"{}\"".format(self.day_locator.format(date_time.day))):
            self.wait_and_click(self.day_locator.format(date_time.day))


class TimeConversion(DatePicker):
    """
    Element presents radiogroup and custom datepicker
    """
    locator = "//input[@name='converterDateSelect' and @value='{}']/../span"
    fmt = '%d.%m.%Y %H:%M'

    open_date_picker_locator = "//input[@data-property=\"converterDate\"]" \
                               "/.." \
                               "/button[@class=\"rates-date-picker__trigger\"]"
    time_locator = "//select[@data-unit='{}']"
    accept_date_picker_locator = "span.rates-button.rates-button_converter-datepicker-hide"

    def set_value(self, value):
        if value == "current":
            self.wait_and_click(self.locator.format("current"))
        else:
            self.wait_and_click(self.locator.format("select"))
            date_time = datetime.strptime(value, self.fmt)
            self.select_date(date_time)
            self.select_time(date_time)
            self.accept()

    def select_time(self, date_time):
        # set hours
        with pytest.allure.step("Selecting hour: \"{}\"".format(self.time_locator.format('hour'))):
            Select(self.get_element(self.time_locator.format('hour'))).\
                select_by_visible_text(date_time.strftime("%H"))
        # set minutes
        with pytest.allure.step("Selecting minutes: \"{}\"".format(self.time_locator.format('minute'))):
            Select(self.get_element(self.time_locator.format('minute'))).\
                select_by_visible_text(date_time.strftime("%M"))

    def accept(self):
        # accept time
        with pytest.allure.step("Accepting selected time: \"{}\"".format(self.accept_date_picker_locator)):
            self.wait_and_click(self.accept_date_picker_locator, By.CSS_SELECTOR)


class GraphTime(DatePicker):
    """
    Element presents datepicker for plotting graph rate by time
    """

    open_date_picker_locator = "//input[@data-property=\"{}\"]/../button[@class=\"rates-date-picker__trigger\"]"
    accept_dates_locator = "button.rates-details__filter-button"
    time_period_locator = "div.jqplot-xaxis-tick"
    time_interval_count = 6

    def set_value(self, value):
        if value != "current":
            date_time = datetime.strptime(value, self.fmt)
            self.select_date(date_time)
            self.accept()

    def get_value(self):
        with pytest.allure.step("Waiting for graph to be available: \"{}\"".format(self.locator)):
            sleep(PAUSE_TIME)
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.time_period_locator)))
            sleep(1)
            elements = self.driver.find_elements(By.CSS_SELECTOR, self.time_period_locator)
            periods = []
            for i in range(0, len(elements), self.time_interval_count):
                start, end = elements[i].text, elements[i + self.time_interval_count - 1].text
                periods.append((start, end))
            return periods

    def accept(self):
        self.wait_and_click(self.accept_dates_locator, by=By.CSS_SELECTOR)


class GraphStartTime(GraphTime):
    """
    Element presents start datepicker for plotting graph rate by time
    """
    open_date_picker_locator = GraphTime.open_date_picker_locator.format("fromDate")


class GraphEndTime(GraphTime):
    """
    Element presents end datepicker for plotting graph rate by time
    """
    open_date_picker_locator = GraphTime.open_date_picker_locator.format("toDate")


class Submit(BaseElement):
    """
    Button to submit passed data
    """
    locator = "button.rates-button"

    def set_value(self, value=None):
        self.wait_and_click(by=By.CSS_SELECTOR)


class Result(BaseElement):
    """
    Label with result conversion value
    """

    locator = "span.rates-converter-result__total-to"

    def get_value(self):
        with pytest.allure.step("Waiting for result to be available: \"{}\"".format(self.locator)):
            sleep(PAUSE_TIME)
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.locator), " "))
        return self.get_element(self.locator, By.CSS_SELECTOR).text


class ServicePackError(Label):
    """
    Label with error message if inappropriate options were selected
    """
    locator = "span.rates-aside__error"
    error_text = "Нельзя выбрать пакет для данных типов валют"


class ConversionRate(BaseElement):
    """
    Label with conversion rate for selected currency
    """
    locator = "span.rates-current__rate-value"

    def get_value(self):

        with pytest.allure.step("Waiting for result to be available: \"{}\"".format(self.locator)):
            sleep(PAUSE_TIME)
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locator)))

            elements = self.driver.find_elements(By.CSS_SELECTOR, self.locator)
            return [float(e.text.replace(",", ".")) for e in elements]
