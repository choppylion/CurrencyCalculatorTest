
import allure
from datetime import datetime
import os
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import csv

TEST_PARAM_PATH = "CalcTestParams.csv"


class Driver:
    __instance = None

    @classmethod
    def get(cls):
        # write driver instance init logic here depending on argument
        if not cls.__instance:
            cls.__instance = Chrome()
        return cls.__instance






money_value = 100500
source_currency = "GBP"
destination_currency = "JPY"
source_code = "card"
destination_code = "card"
exchange_type = "ibank"
service_pack = "empty"
time = datetime.strptime('01.06.2017 13:35', '%d.%m.%Y %H:%M')





#driver.quit()


def import_params(path=None):
    if path is None:
        path = TEST_PARAM_PATH

    if os.path.exists(path):
        pass
    else:
        raise FileNotFoundError("Test parameters not found in \'{}\'".format(path))

