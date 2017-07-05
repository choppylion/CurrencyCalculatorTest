from aenum import AutoNumberEnum
import pytest

from element import MoneyValue, SrcCurrency, DstCurrency, SrcCode, DstCode, \
    ExchangeType, ServicePack, TimeConversion, Submit, Result


class Parameters(AutoNumberEnum):
    value = MoneyValue, 100, "Value in source currency"
    src_currency = SrcCurrency, "RUB", "Source currency"
    dst_currency = DstCurrency, "USD", "Destination currency"
    source = SrcCode, "card", "Source code"
    destination = DstCode, "account", "Destination code"
    exchange_type = ExchangeType, "ibank", "Exchange method"
    service_pack = ServicePack, "empty", "Service pack"
    time_conversion = TimeConversion, "current", "Time of conversion"

    def __init__(self, cls_element, default, desc):
        self.cls, self.default, self.desc = cls_element, default, desc

    @staticmethod
    def by_name(title):
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
        self.driver = webdriver

    def open(self):
        self.driver.get(self.link)

    def set_params(self, params):
        for param in Parameters:
            param_value = params[param.name]
            with pytest.allure.step("Trying to set \'{}\' with value \'{}\'".format(param.name, param_value)):
                element = param.cls(self.driver)
                element.set_value(param_value)

    def submit(self):
        Submit(self.driver).set_value()

    def get_result(self):
        return Result(self.driver).get_value()
