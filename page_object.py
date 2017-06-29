from aenum import AutoNumberEnum
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
# from webium import BasePage, Find
# from common import Driver


class Parameters(AutoNumberEnum):

    value = "input.value" #.rates-aside__filter-block-line-right
    src_currency = ".converterFrom"
    dst_currency = ".converterTo"
    source = ".sourceCode"
    destination = ".destinationCode"
    exchange_method = ".exchangeType"
    service = ".servicePack"
    time = ".converterDateSelect"

    button = "css=button.rates-button"
    result = "css=rates-converter-result__total-to"

    def __init__(self, locator):
        self.locator = locator


class CalculatorPage:

    LINK =

    @classmethod
    def setup(cls):
        cls.driver = Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(15)
        cls.driver.get(cls.LINK)

    @classmethod
    def teardown(cls):
        cls.driver.quit()



#
# class AbstractBasePage(BasePage):
#
#     def __init__(self, url):
#         BasePage.__init__(self, Driver.get(), url)
#
#     def get_title(self):
#         return Driver.get().title
#
#
# class DashboardPage(AbstractBasePage):
#
#     _first_lesson = Find(
#         by=By.XPATH, value="(//div[contains(@class, 'lesson-block')])[1]/a")
#
#     def __init__(self):
#         AbstractBasePage.__init__(self, "http://lessons2.ru")
#
#     def open_first_lesson(self):
#         self._first_lesson.click()
#         return LessonPage()


