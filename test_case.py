from page_object import CalculatorPage
import pytest


CALC_LINK = r"http://www.sberbank.ru/ru/quotes/converter"


class CaseBase:
    pass


class TestCaseFirst(CaseBase):

    def test_something(self):
        pass


class TestCaseSecond(CaseBase):
    pass


class TestCaseThird(CaseBase):
    pass
