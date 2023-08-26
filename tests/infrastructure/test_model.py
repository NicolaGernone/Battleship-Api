# test_models.py
import uuid
from datetime import datetime
from decimal import Decimal

import pytest

from api.domain.choices import Coins
from tests.domain.factories import CoinFactory


@pytest.mark.django_db
def test_coin_creation():
    coin = CoinFactory()
    assert isinstance(coin.id, uuid.UUID)
    assert isinstance(coin.name, str)
    assert coin.symbol in dict(Coins.choices).keys()
    assert isinstance(coin.date, datetime)
    assert isinstance(coin.high, Decimal)
    assert isinstance(coin.low, Decimal)
    assert isinstance(coin.open, Decimal)
    assert isinstance(coin.close, Decimal)
