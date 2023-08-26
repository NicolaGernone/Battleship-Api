import uuid

from django.db import models

from api.domain.choices import Coins


class Coin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    symbol = models.CharField(
        max_length=5, choices=Coins.choices, default=Coins.AAVE, blank=False, null=False
    )
    date = models.DateTimeField(blank=False, null=False)
    high = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    low = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    open = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    close = models.DecimalField(max_digits=18, decimal_places=8, default=0)

    class Meta:
        unique_together = ("symbol", "date")
        verbose_name = "Coin"

    def __str__(self):
        return self.name
