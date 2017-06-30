import allure
import pytest

pytest_plugins = 'allure.pytest_plugin'

from param_locator import *
from test_conf import CALCULATOR_LINK, WAIT_TIME, Parameters, import_test_configs


# class Driver:
#     __instance = None
#
#     @classmethod
#     def get(cls):
#         if not cls.__instance:
#             cls.__instance = Chrome()
#         return cls.__instance
#


configs = import_test_configs()


def test_conversion_result(expect, real):
    assert expect == real_result


for params, expecting_result in configs:
    for param, value in params.items():
        with pytest.a
        enum_param = Parameters.by_str(param)
        element = enum_param.cls(driver)
        element.set_value(value)

    element = Submit(driver)
    element.set_value()
    real_result = element.get_value()
    test_conversion_result(expecting_result, real_result)

    driver.quit()



