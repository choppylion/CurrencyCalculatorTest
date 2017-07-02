import csv
import os

from aenum import AutoNumberEnum
import pytest
from selenium.webdriver import Chrome

from element import *

TEST_CONFIG_PATH = "test_config.csv"
SLEEP_TIME = 0.1
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

    def __init__(self, cls_element, default, desc):
        self.cls, self.default, self.desc = cls_element, default, desc

    @staticmethod
    def by_str(title):
        for param in Parameters:
            if param.name == title:
                return param
        raise KeyError("{} not found in {}".format(title, Parameters))


def import_test_data(path=None):
    if path is None:
        path = TEST_CONFIG_PATH

    if os.path.exists(path):
        configs = []
        try:
            with open(path, 'r', encoding='utf-8') as fr:
                reader = csv.DictReader(fr)
                for cfg_dict in reader:
                    test_params = cfg_dict
                    for param in Parameters:
                        if param.name not in test_params:
                            test_params[param.name] = param.default

                    result = test_params["result"]
                    del test_params["result"]
                    configs.append((test_params, result))

            return configs
        except Exception as e:
            raise IOError("Impossible to read test data:\n{}".format(e))

    else:
        raise FileNotFoundError("Test parameters not found in \'{}\'".format(path))


@pytest.yield_fixture()
def webdriver(request):
    driver = Chrome()
    driver.implicitly_wait(WAIT_TIME)
    driver.maximize_window()
    yield driver
    driver.quit()
