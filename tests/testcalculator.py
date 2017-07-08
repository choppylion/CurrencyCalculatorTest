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

    @pytest.mark.skip
    @pytest.mark.parametrize("config", import_test_data("config_conversion_result.csv"))
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
        with pytest.allure.step("Asserting result"):
            assert expected_result == real_result

    @pytest.mark.skip
    @pytest.mark.parametrize("config", import_test_data("config_unselectable_exchange.csv"))
    def test_unselectable_exchange(self, webdriver, config):
        """
        Sets all params from config and asserts that disabled radiobuttons were not selected by config value
        :param webdriver: selenium driver instance
        :param config: test data for calculator
        """
        page = self.init_page(webdriver)
        page.set_params(config)

        exchange_type = config[Parameters.exchange_type]
        is_selected = page.is_radio_selected(Parameters.exchange_type, exchange_type)
        assert is_selected is False

    @pytest.mark.parametrize("config", import_test_data("config_incompatible_servicepack.csv"))
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

    # @pytest.mark.parametrize("config", import_test_data("config_conversion_result.csv"))
    # def test_cost_sale_above_purchase(self, webdriver, config):
    #     params, expected_result = self.process(config)
    #     page = self.page(webdriver)
    #
    # @pytest.mark.parametrize("config", import_test_data("config_graph_date_applying.csv"))
    # def test_graph_dates_displaying(self, webdriver, config):
    #     params, expected_result = self.process(config)
    #     page = self.page(webdriver)

    def init_page(self, webdriver,):
        page = self.page(webdriver)
        with pytest.allure.step("Open page"):
            page.open()
        return page
