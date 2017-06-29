from aenum import AutoNumberEnum
import os
import pytest
from selenium import webdriver

from param_locator import *

DRIVER = "chrome"
CALCULATOR_LINK = "http://www.sberbank.ru/ru/quotes/converter"
TEST_PARAM_PATH = "CalcTestParams.csv"


class Parameters(AutoNumberEnum):
    value = MoneyValue, 100, "Value in source currency"
    src_currency = SrcCurrency, "RUB", "Source currency"
    dst_currency = DstCurrency, "USD", "Destination currency"
    source = SrcCode, "card", "Source code"
    destination = DstCode, "account", "Destination code"
    exchange_type = ExchangeType, "ibank", "Exchange method"
    service_pack = ServicePack, "empty", "Service pack"
    time_conversion = TimeConversion, "current", "Time of conversion"

    def __init__(self, cls, default, desc):
        self.cls, self.default, self.desc = cls, default, desc


def pytest_addoption(parser):
    parser.addoption("--driver", action="store", default=DRIVER, help="Type in browser type")
    parser.addoption("--url", action="store", default=CALCULATOR_LINK, help="url")

    for param in Parameters:
        parser.addoption("--" + param.name, action="store", default=param.default, help=param.desc)


def import_params(path=None):
    if path is None:
        path = TEST_PARAM_PATH

    if os.path.exists(path):
        pass
    else:
        raise FileNotFoundError("Test parameters not found in \'{}\'".format(path))
