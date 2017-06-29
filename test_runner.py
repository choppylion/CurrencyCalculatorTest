from datetime import datetime
from selenium.webdriver import Chrome

from param_locator import *
from test_conf import Parameters


params = {
    Parameters.value: 100000,
    Parameters.src_currency: "GBP",
    Parameters.dst_currency: "JPY",
    Parameters.source: "cash",
    Parameters.destination: "card",
    Parameters.exchange_type: "office",
    Parameters.service_pack: "empty",
    Parameters.time_conversion: datetime.strptime('14.01.2017 05:55', '%d.%m.%Y %H:%M')
}

result = "12 706 204,38 JPY"


#
# class CalculatorPage:
#
#     LINK = "http://www.sberbank.ru/ru/quotes/converter"
#
#     @classmethod
#     def setup(cls):
#         cls.driver = Chrome()
#         cls.driver.maximize_window()
#         cls.driver.implicitly_wait(15)
#         cls.driver.get(cls.LINK)
#
#     @classmethod
#     def teardown(cls):
#         cls.driver.quit()

#
# class Driver(object):
#     __instance = None
#
#     @classmethod
#     def get(cls, type='ff'):
#         # write driver instance init logic here depending on argument
#         if not cls.__instance:
#             cls.__instance = Chrome()
#         return cls.__instance


driver = Chrome()
driver.implicitly_wait(15)
driver.get("http://www.sberbank.ru/ru/quotes/converter")


for param, value in params.items():
    element = param.cls(driver)
    element.set_value(value)

element = Submit(driver)
element.set_value()
real_result = element.get_value()

assert result == real_result

driver.quit()



