from collections import OrderedDict
import csv
import os

import pytest
from selenium.webdriver import Chrome


#: time to pause before acting with element
PAUSE_TIME = 0.1
#: maximal time to wait until element become active
WAIT_TIME = 15


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


def import_test_data(filename):
    """
    Imports data from csv file in list, if parameter is not specified so default value is used
    :param filename: name of file to fetch test data
    :return: list of parameters and expected result
    """
    try:
        project_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(os.path.join(project_dir, "configs", filename))
        with open(path, 'r') as fr:
            reader = csv.DictReader(fr)
            header = reader.fieldnames
            config = []
            for row in reader:
                row_dict = OrderedDict()
                for key in header:
                    row_dict[key] = row[key]

                xfail_value = row_dict.pop("xfail", "")
                if xfail_value:
                    row_dict = pytest.param(row_dict, marks=pytest.mark.xfail(reason=xfail_value))

                config.append(row_dict)
            return config
    except Exception as e:
        raise IOError("Impossible to read test data:\n{}".format(e))
