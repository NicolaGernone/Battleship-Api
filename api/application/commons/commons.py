from api.domain.entities import Gameplay
from api.domain.exceptions import GameNotActiveError


def is_gameplay_active(gameplay: Gameplay) -> bool:
    if not gameplay.is_active:
        raise GameNotActiveError("The game is not active")
    return True
