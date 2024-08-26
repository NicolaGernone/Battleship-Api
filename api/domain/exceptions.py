# custom_exceptions.py
class GameAlreadyStarted(Exception):
    pass

class GameNotStarted(Exception):
    pass

class InvalidShipPosition(Exception):
    pass

class InvalidAttackCoordinates(Exception):
    pass
