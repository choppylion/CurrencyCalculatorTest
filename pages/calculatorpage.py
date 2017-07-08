from aenum import AutoNumberEnum
from datetime import datetime, timedelta
import pytest

from elements.calcelement import MoneyValue, SrcCurrency, DstCurrency, SrcCode, DstCode, \
    ExchangeType, ServicePack, TimeConversion, GraphTime, GraphStartTime, GraphEndTime,\
    Submit, Result, ServicePackError, ConversionRate


class Parameters(AutoNumberEnum):
    """
    Advanced enum to keep important data about every parameter for conversion
    """

    value = MoneyValue, 100, "Value in source currency"
    src_currency = SrcCurrency, "RUB", "Source currency"
    dst_currency = DstCurrency, "USD", "Destination currency"
    source = SrcCode, "card", "Source code"
    destination = DstCode, "account", "Destination code"
    exchange_type = ExchangeType, "ibank", "Exchange method"
    service_pack = ServicePack, "empty", "Service pack"
    time_conversion = TimeConversion, "current", "Time of conversion"
    start_date = GraphStartTime, "current", "Start date of graph"
    end_date = GraphEndTime, "current", "End date of graph"

    def __init__(self, cls_element, default, desc):
        """
        :param cls_element: class of element with locators
        :param default: default value of element
        :param desc: description of element
        """
        self.cls, self.default, self.desc = cls_element, default, desc

    @staticmethod
    def by_name(title):
        """
        Looks for parameter with title that equals given string
        :param title: string name of parameter
        :return: aenum object
        """
        for param in Parameters:
            if param.name == title:
                return param
        raise KeyError("{} not found in {}".format(title, Parameters))


class CalculatorPage:
    """
    Page Object of main currency calculator page
    """
    link = "http://www.sberbank.ru/ru/quotes/converter"

    def __init__(self, webdriver):
        """
        :param webdriver: selenium webdriver instance
        """
        self.driver = webdriver

    def open(self):
        """
        Opens link of page with driver
        """
        self.driver.get(self.link)

    def set_params(self, params_dict):
        """
        Sets given params for every element in calculator
        :param params_dict: params with values to apply
        """
        with pytest.allure.step("Setting params"):
            for param, value in params_dict.items():
                self.set_param(param, value)

    def set_param(self, param, value):
        with pytest.allure.step("Trying to set \'{}\' with value \'{}\'".format(param, value)):
            element = self.convert_param(param).cls(self.driver)
            element.set_value(value)

    def submit(self):
        """
        Submits form with applied parameters
        """
        with pytest.allure.step("Submitting"):
            Submit(self.driver).set_value()

    def get_conversion_result(self):
        """
        Retrieves result from form
        """
        with pytest.allure.step("Getting result"):
            return Result(self.driver).get_value()

    def is_radio_selected(self, param, value):
        with pytest.allure.step("Trying to get \'{}\'[\'{}\'] selected status".format(param, value)):
            element = self.convert_param(param).cls(self.driver)
            return element.get_value(value)

    def is_servicepack_error(self):
        text = ServicePackError(self.driver).get_value()
        return ServicePackError.error_text in text

    def get_conversion_rate(self):
        return ConversionRate(self.driver).get_value()

    def get_graph_periods(self):
        return GraphTime(self.driver).get_value()

    def convert_param(self, param_string):
        return Parameters.by_name(param_string)

    def convert_to_expected_date(self, date_type, date_string):
        def get_latest_report_date():
            date_time = datetime.now()
            date_time -= timedelta(hours=14)  # minimal time on Earth, 14h = (GMT+3(MSK) + GMT-11(IntlDateLine)
            date_time -= timedelta(days=1)  # It's a date that we have a latest currency report for
            return date_time

        earliest_working_date_time = datetime.strptime("01.03.2004", GraphTime.fmt)
        latest_report_date_time = get_latest_report_date()

        if date_string == "current":
            date_time = latest_report_date_time
        else:
            date_time = min(datetime.strptime(date_string, GraphTime.fmt), latest_report_date_time)

        if date_type == "start_date":
            date_time = max(date_time - timedelta(days=1), earliest_working_date_time)

        return date_time.strftime(GraphTime.fmt)
