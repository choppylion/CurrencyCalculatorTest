from collections import OrderedDict
import pytest

from conftest import import_test_data
from pages.calculatorpage import CalculatorPage, Parameters


@pytest.mark.usefixtures("webdriver")
@pytest.allure.story("Sberbank currency calculator testing")
class TestCalculator:
    """
    Main class to test currency calculator using configs with test data
    """

    page = CalculatorPage

    @pytest.mark.parametrize("config", import_test_data("conversion_result.csv"))
    def test_conversion_result(self, webdriver, config):
        """
        Sets all params from config and asserts expected result with obtained
        :param webdriver: selenium driver instance
        :param config: test data for calculator
        """
        expected_result = config.pop("result")
        page = self.init_page(webdriver)
        page.set_params(config)
        page.submit()
        real_result = page.get_conversion_result()
        assert expected_result == real_result

    @pytest.mark.parametrize("config", import_test_data("unselectable_exchange.csv"))
    def test_unselectable_exchange(self, webdriver, config):
        """
        Sets all params from config and asserts that disabled radiobuttons were not selected by config value
        :param webdriver: selenium driver instance
        :param config: test data for calculator
        """
        page = self.init_page(webdriver)
        page.set_params(config)

        exchange_type = config["exchange_type"]
        is_selected = page.is_radio_selected("exchange_type", exchange_type)
        assert is_selected is False

    @pytest.mark.parametrize("config", import_test_data("incompatible_servicepack.csv"))
    def test_incompatible_servicepack(self, webdriver, config):
        """
        Sets all params from config and asserts that error message of selected servicepack was shown
        :param webdriver: selenium driver instance
        :param config: test data for calculator
        """
        page = self.init_page(webdriver)
        page.set_params(config)
        error_shown = page.is_servicepack_error()
        assert error_shown is True

    @pytest.mark.parametrize("config", import_test_data("sale_above_purchase.csv"))
    def test_cost_sale_above_purchase(self, webdriver, config):
        """
        Sets all params from config and asserts that cost of buying currency more than selling
        :param webdriver: selenium driver instance
        :param config: test data for calculator
        """
        page = self.init_page(webdriver)
        page.set_params(config)
        rates = page.get_conversion_rate()
        for index in range(0, len(rates), 2):
            buy_rate, sell_rate = rates[index:index+2]
            assert buy_rate < sell_rate

    @pytest.mark.parametrize("config", import_test_data("graph_date_display.csv"))
    def test_graph_dates_display(self, webdriver, config):
        page = self.init_page(webdriver)
        page.set_params(config)

        expected_start = page.convert_to_expected_date("start_date", config["start_date"])
        expected_end = page.convert_to_expected_date("end_date", config["end_date"])
        graph_periods = page.get_graph_periods()

        for graph_start, graph_end in graph_periods:
            assert expected_start == graph_start
            assert expected_end == graph_end

    def init_page(self, webdriver):
        page = self.page(webdriver)
        with pytest.allure.step("Open page"):
            page.open()
        return page
