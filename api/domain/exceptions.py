class GameNotActiveError(Exception):
    pass


class InvalidTurnError(Exception):
    pass


class InvalidShipPositionError(Exception):
    pass


class PlayerAlreadyJoinedError(Exception):
    pass


class InvalidAttackPositionError(Exception):
    pass


class InvalidPlayerError(Exception):
    pass


class InvalidAutomaticAttackError(Exception):
    pass


class BothPlayersPositionedError(Exception):
    pass


class TurnToPositionShipsError(Exception):
    pass


class IncompleteBoardError(Exception):
    pass


class InvalidDirectionError(Exception):
    pass


class InvalidShipError(Exception):
    pass


class InvalidBoardCoordinatesError(Exception):
    pass


class CoordinatesAlreadyHaveShipError(Exception):
    pass


class MaxPlacementAttemptsExceeded(Exception):
    pass


class IncompleteShipsPositioningError(Exception):
    pass
