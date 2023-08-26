# test_services.py
from datetime import datetime

import pytest
from django.db.models.query import QuerySet

from api.application.services import CoinService
from api.domain.exceptions import *
from tests.domain.factories import CoinFactory


@pytest.mark.django_db
def test_get_coin_close_values_valid():
    coin = CoinFactory()
    data = CoinService.CoinClose(
        symbol=coin.symbol, date=coin.date.strftime("%Y-%m-%d")
    )
    close_values = CoinService.get_coin_close_values(data=data)
    print("Close values:", close_values)
    assert isinstance(close_values, QuerySet)


@pytest.mark.django_db
def test_get_coin_max_profit_valid():
    coin = CoinFactory()
    data = CoinService.CoinMaxProfit(
        symbol=coin.symbol,
        start_date=coin.date.strftime("%Y-%m-%d"),
        end_date=coin.date.strftime("%Y-%m-%d"),
    )
    max_profit_value = CoinService.get_coin_max_profit(data=data)
    assert isinstance(max_profit_value, dict)
    assert "Buy Day" in max_profit_value
    assert "Sell Day" in max_profit_value


@pytest.mark.django_db
def test_get_coin_names_symbols_valid():
    names_symbols = CoinService.get_coin_names_symbols()
    assert isinstance(names_symbols, QuerySet)

@pytest.mark.django_db
def test_check_coin_exist_failure():
    symbol = 'INVALID'
    with pytest.raises(CoinSymbolException):
        CoinService.check_symbol(symbol)

@pytest.mark.django_db
def test_get_coin_close_values_failure():
    data = CoinService.CoinClose(symbol='INVALID', date='INVALID')
    with pytest.raises(DateFormatException):
        CoinService.get_coin_close_values(data=data)

@pytest.mark.django_db
def test_get_coin_max_profit_failure():
    data = CoinService.CoinMaxProfit(symbol='INVALID', start_date='2023-08-25', end_date='2023-08-26')
    with pytest.raises(BuySellException):
        CoinService.get_coin_max_profit(data=data)

def test_days_range_failure():
    start = '2023-08-25 00:00:00'
    end = '2023-08-25'
    with pytest.raises(DateFormatException):
        CoinService.days_range(start=start, end=end)

def test_stock_buy_sell_failure():
    price = [100.0]
    n = 5
    with pytest.raises(BuySellException):
        CoinService.stockBuySell(price=price, n=n)


def test_check_symbol_invalid():
    symbol = "INVALID"
    with pytest.raises(CoinSymbolException):
        CoinService.check_symbol(symbol)
        
def test_validate_date_format_valid():
    date = "2023-08-25"
    assert CoinService.validate_date_format(date) is None

def test_validate_date_format_invalid():
    date = "2023-08-25 00:00:00"
    with pytest.raises(DateFormatException):
        CoinService.validate_date_format(date)

def test_validate_days_valid():
    days = 5
    assert CoinService.validate_days(days) is None

def test_validate_days_negative():
    days = -5
    with pytest.raises(DateFormatException):
        CoinService.validate_days(days)

def test_days_range_valid():
    start = "2023-08-01"
    end = "2023-08-25"
    assert CoinService.days_range(start, end) == 24

def test_days_range_end_before_start():
    start = "2023-08-25"
    end = "2023-08-01"
    with pytest.raises(DateFormatException):
        CoinService.days_range(start, end)

def test_days_range_invalid_format():
    start = "2023-08-25 00:00:00"
    end = "2023-08-01"
    with pytest.raises(DateFormatException):
        CoinService.days_range(start, end)

def test_stock_buy_sell_valid():
    price = [100, 200, 150, 300, 50]
    n = 5
    assert CoinService.stockBuySell(price, n) == {"Buy Day": 2, "Sell Day": 3}

def test_stock_buy_sell_invalid_days():
    price = [100, 200, 150, 300, 50]
    n = 6
    with pytest.raises(BuySellException):
        CoinService.stockBuySell(price, n)

def test_stock_buy_sell_one_day():
    price = [100]
    n = 1
    with pytest.raises(BuySellException):
        CoinService.stockBuySell(price, n)
