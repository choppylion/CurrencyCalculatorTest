import pytest

from conftest import import_test_data
from page_object import CalculatorPage


@pytest.allure.story("Sberbank currency calculator testing")
class TestCalculator:
    """
    Main class to test currency calculator
    """

    @pytest.mark.usefixtures("webdriver")
    @pytest.mark.parametrize('params, expected', import_test_data())
    def test_conversion_result(self, webdriver, params, expected):
        """
        Imports test data from file, sets it up and asserts with obtained result
        :param webdriver: selenium driver instance
        :param params: input params for calculator
        :param expected: expected result of conversion
        """
        page = CalculatorPage(webdriver)

        with pytest.allure.step("Open page"):
            page.open()
        with pytest.allure.step("Setting params"):
            page.set_params(params)
        with pytest.allure.step("Submitting"):
            page.submit()
        with pytest.allure.step("Getting result"):
            real_result = page.get_result()

        with pytest.allure.step("Asserting result"):
            assert expected == real_result
