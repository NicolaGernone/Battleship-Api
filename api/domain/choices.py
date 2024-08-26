# choices.py
from django.db import models


class Ships(models.TextChoices):
    CARRIER = "5", "Carrier"
    BATTLESHIP = "6", "Battleship"
    CRUISER = "7", "Cruiser"
    SUBMARINE = "3", "Submarine"
    DESTROYER = "8", "Destroyer"
