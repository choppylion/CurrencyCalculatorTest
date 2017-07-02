from aenum import AutoNumberEnum
import csv
import os
import pytest
from selenium.webdriver import Chrome

from element import *
from page_object import CalculatorPage

DRIVER = "chrome"
TEST_CONFIG_PATH = "test_config.csv"
SLEEP_TIME = 0.1
WAIT_TIME = 15


@pytest.yield_fixture()
def webdriver(request):
    driver = Chrome()
    driver.implicitly_wait(WAIT_TIME)
    driver.maximize_window()
    yield driver
    driver.quit()


def import_test_data(path=None):
    if path is None:
        path = TEST_CONFIG_PATH

    if os.path.exists(path):
        configs = []
        try:
            with open(path, 'r', encoding='utf-8') as fr:
                reader = csv.DictReader(fr)
                for cfg_dict in reader:
                    result = cfg_dict["result"]
                    del cfg_dict["result"]
                    configs.append((cfg_dict, result))
            return configs
        except Exception as e:
            raise IOError("Impossible to read test data:\n{}".format(e))

    else:
        raise FileNotFoundError("Test parameters not found in \'{}\'".format(path))


@pytest.mark.parametrize('params, expected', import_test_data())
def test_currency_conversion_result(params, expected):
    page = CalculatorPage()
    page.set_params(params)
    page.submit()
    real_result = page.get_result()
    assert expected == real_result
