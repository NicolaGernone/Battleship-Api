from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from api.domain.entities import Coin

from api.domain.choices import Coins
from api.domain.exceptions import (
    BuySellException,
    CoinCloseValuesException,
    CoinMaxProfitException,
    CoinNameSymbolException,
    CoinNotFound,
    DateFormatException,
    CoinSymbolException
)
from app.settings import LOGGER as lg


class CoinService:
    @dataclass
    class CoinClose:
        symbol: str
        date: str

    @dataclass
    class CoinMaxProfit:
        symbol: str
        start_date: str
        end_date: str

    DATE_FORMAT = "%Y-%m-%d"

    @staticmethod
    def check_symbol(symbol: str) -> bool:
        """Check if a symbol is valid and exists."""
        lg.info(f"Checking if {symbol} exists")
        if symbol not in dict(Coins.choices).keys():
            raise CoinSymbolException("Invalid Symbol")
        return Coin.objects.filter(symbol=symbol).exists()

    @staticmethod
    def get_coin_names_symbols() -> list:
        """Get all coin names and symbols."""
        try:
            lg.info("Listing names and symbols")
            return Coin.objects.all().values("name", "symbol").distinct()
        except CoinNameSymbolException as e:
            lg.error(f"Error listing names and symbols: {str(e)}")
            raise e
    
    @staticmethod
    def validate_date_format(date: str) -> None:
        """Validate the date format."""
        try:
            datetime.strptime(date, CoinService.DATE_FORMAT).date()
        except ValueError:
            raise DateFormatException("Invalid date format")
    
    @staticmethod
    def validate_days(days: int) -> None:
        """Validate the days."""
        if days < 0:
            raise DateFormatException("End date must be after start date")

    @staticmethod
    def get_coin_close_values(data: CoinClose) -> list:
        """Get all close values for a coin."""
        try:
            lg.info(f"Listing close values for {data.symbol} on {data.date}")
            CoinService.validate_date_format(data.date)
            return Coin.objects.filter(date__date=data.date, symbol=data.symbol).values(
                "name", "symbol", "close"
            )
        except ValueError:
            lg.error(
                f"Error listing close values for {data.symbol} on {data.date}: {str(e)}"
            )
            raise CoinCloseValuesException("Invalid date format")

    @staticmethod
    def get_coin_max_profit(data: CoinMaxProfit) -> dict:
        """Get the max profit for a coin."""
        try:
            lg.info(
                f"Getting max profit for {data.symbol} between {data.start_date} and {data.end_date}"
            )
            days = CoinService.days_range(data.start_date, data.end_date)
            lg.info(f"Days between {data.start_date} and {data.end_date}: {days}")
            data = Coin.objects.filter(symbol=data.symbol).filter(
                date__range=[data.start_date, data.end_date]
            )
            prices = data.values_list("close", flat=True)
            return CoinService.stockBuySell(prices, days)
        except CoinMaxProfitException as e:
            lg.error(
                f"Error getting max profit for {data.symbol} between {data.start_date} and {data.end_date}: {str(e)}"
            )
            raise e

    @staticmethod
    def days_range(start: str, end: str) -> int:
        """Calulate the day between the start date and the end date"""
        CoinService.validate_date_format(start)  # Validate date format here
        CoinService.validate_date_format(end) 
        partial_start = datetime.strptime(start, "%Y-%m-%d").date()
        partial_end = datetime.strptime(end, "%Y-%m-%d").date()
        delta = partial_end - partial_start
        CoinService.validate_days(delta.days)  # Validate days here
        return delta.days

    @staticmethod
    def stockBuySell(price: list[Decimal], n: int) -> dict:
        # Prices must be given for at
        # least two days and not be more than the price array
        try:
            lg.info(f"Calculating buy and sell days for {price} and {n}")
            if n == 1 or n > len(price):
                raise BuySellException("Invalid number of days")

            # Traverse through given price array
            buy = 0
            sell = 0
            i = 0
            while i < (n - 1):
                # Find Local Minima
                # Note that the limit is (n-2) as
                # we are comparing present element
                # to the next element
                while (i < (n - 1)) and (price[i + 1] <= price[i]):
                    i += 1

                # If we reached the end, break
                # as no further solution possible
                if i == n - 1:
                    break

                # Store the index of minima
                buy = i
                i += 1

                # Find Local Maxima
                # Note that the limit is (n-1) as we are
                # comparing to previous element
                while (i < n) and (price[i] >= price[i - 1]):
                    i += 1

                # Store the index of maxima
                sell = i - 1

            return {"Buy Day": buy, "Sell Day": sell}
        except BuySellException as e:
            lg.error(f"Error calculating buy and sell days: {str(e)}")
            raise e
