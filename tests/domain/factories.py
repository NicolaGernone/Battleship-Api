# factories.py
import factory
from api.domain.entities import Coin
from api.domain.choices import Coins
import uuid
from datetime import datetime
from decimal import Decimal


class CoinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coin

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    symbol = factory.Iterator(Coins.choices, getter=lambda c: c[0])
    date = factory.Faker("date_time")
    high = factory.Faker("pydecimal", left_digits=10, right_digits=8)
    low = factory.Faker("pydecimal", left_digits=10, right_digits=8)
    open = factory.Faker("pydecimal", left_digits=10, right_digits=8)
    close = factory.Faker("pydecimal", left_digits=10, right_digits=8)
