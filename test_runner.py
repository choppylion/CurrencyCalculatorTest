import pytest

from page_object import CalculatorPage
from params import import_test_data


@pytest.mark.parametrize('params, expected', import_test_data())
def test_currency_conversion_result(params, expected):
    page = CalculatorPage()
    page.set_params(params)
    page.submit()
    real_result = page.get_result()
    assert expected == real_result
