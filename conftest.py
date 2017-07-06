import csv
import os

import pytest
from selenium.webdriver import Chrome

#: time to pause before acting with element
PAUSE_TIME = 0.1
#: maximal time to wait until element become active
WAIT_TIME = 15
#: default path to file with test data
TEST_CONFIG_PATH = "test_config.csv"


@pytest.fixture()
def webdriver():
    """
    Defines setup and teardown for selenium webdriver
    :yield: driver instance
    """
    driver = Chrome()
    driver.implicitly_wait(WAIT_TIME)
    driver.maximize_window()
    yield driver
    driver.quit()


def import_test_data(path=None):
    """
    Imports data from csv file in list, if parameter is not specified so default value is used
    :param path: path to file to fetch test data
    :return: list of parameters and expected result
    """
    if path is None:
        path = TEST_CONFIG_PATH

    if os.path.exists(path):
        configs = []
        try:
            with open(path, 'r', encoding='utf-8') as fr:
                from page_object import Parameters
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
