from aenum import AutoNumberEnum
import csv
import os
import pytest
from selenium.webdriver import Chrome

from param_locator import *

DRIVER = "chrome"
CALCULATOR_LINK = "http://www.sberbank.ru/ru/quotes/converter"
TEST_CONFIG_PATH = "test_config.csv"
WAIT_TIME = 15


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

    @classmethod
    def by_str(cls, title):
        for param in cls:
            if param.name == title:
                return param
        raise KeyError("{} not found in {}".format(title, cls))


@pytest.yield_fixture()
def driver():
    _driver = Chrome()
    _driver.implicitly_wait(WAIT_TIME)
    _driver.maximize_window()
    _driver.get(CALCULATOR_LINK)
    yield _driver
    _driver.quit()


def pytest_addoption(parser):
    parser.addoption("--driver", action="store", default=DRIVER, help="Type in browser type")
    parser.addoption("--url", action="store", default=CALCULATOR_LINK, help="url")

    for param in Parameters:
        parser.addoption("--" + param.name, action="store", default=param.default, help=param.desc)


def import_test_configs(path=None):
    if path is None:
        path = TEST_CONFIG_PATH

    if os.path.exists(path):
        configs = []
        with open(path, 'r', encoding='utf-8') as fr:
            reader = csv.DictReader(fr)
            for cfg_dict in reader:
                result = cfg_dict["result"]
                del cfg_dict["result"]
                configs.append((cfg_dict, result))
        return configs

    else:
        raise FileNotFoundError("Test parameters not found in \'{}\'".format(path))
