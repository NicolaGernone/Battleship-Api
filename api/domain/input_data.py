from dataclasses import dataclass
from typing import Dict, List, Tuple

from api.domain.exceptions import InvalidDirectionError, InvalidShipError
from api.domain.choices import Directions, Ships


@dataclass
class PositionVector:
    ship: str
    direction: str
    coordinates: Tuple[int, int]

    def __post_init__(self):
        self.direction = self.direction.upper()
        self.ship = self.ship.upper()

    def validate(self):
        if self.direction not in Directions.values:
            raise InvalidDirectionError
        if self.ship not in Ships.names:
            raise InvalidShipError


@dataclass
class PositionData:
    player: str
    positions: List[PositionVector]

    def validate(self):
        for position in self.positions:
            position.validate()


@dataclass
class AttackInput:
    player: str
    coordinates: Tuple[int, int]
