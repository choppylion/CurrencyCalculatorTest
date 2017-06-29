import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--url", action="store", default="http://www.sberbank.ru/ru/quotes/converter", help="url")
    parser.addoption("--value", action="store", default="100", help="value in source currency")
    parser.addoption("--src_currency", action="store", default="RUB", help="source currency")
    parser.addoption("--dst_currency", action="store", default="USD", help="destination currency")
    parser.addoption("--src_code", action="store", default="card", help="source code")
    parser.addoption("--dst_code", action="store", default="account", help="destination code")
    parser.addoption("--exchange_type", action="store", default="ibank", help="value in source currency")
    parser.addoption("--service_pack", action="store", default="empty", help="service pack ")
    parser.addoption("--time_conversion", action="store", default="current", help="time of conversion")
