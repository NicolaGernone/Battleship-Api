# choices.py
from enum import Enum


class Ships(Enum):
    CARRIER = 5
    BATTLESHIP = 6
    CRUISER = 7
    SUBMARINE = 3
    DESTROYER = 8


class Directions(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)


class AttackSymbols(Enum):
    HIT = "X"
    MISS = "O"


class ShipSymbols(Enum):
    CARRIER = "CA"
    BATTLESHIP = "BA"
    CRUISER = "CR"
    SUBMARINE = "SU"
    DESTROYER = "DE"


class PlayerRoles(Enum):
    PLAYER1 = "player1"
    PLAYER2 = "player2"
