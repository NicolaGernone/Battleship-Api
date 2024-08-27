from itertools import product
from typing import Dict, List, Tuple

from api.domain.choices import Directions, PlayerRoles, Ships, ShipSymbols
from api.domain.entities import GameBoard, Gameplay
from api.domain.exceptions import (
    GameNotActiveError,
    InvalidBoardCoordinatesError,
    CoordinatesAlreadyHaveShipError,
    MaxPlacementAttemptsExceeded,
    BothPlayersPositionedError,
    TurnToPositionShipsError,
    IncompleteShipsPositioningError,
)

from api.domain.input_data import PositionData, PositionVector


class PositioningServices:
    @staticmethod
    def position_ships(gameplay: Gameplay, data: PositionData) -> Dict[str, str]:
        """Service to position ships on the board."""
        player_board = PositioningServices.get_player_board(
            gameplay=gameplay, player=data.player
        )
        PositioningServices.validate_game_status(gameplay=gameplay)
        PositioningServices.validate_ships_in_payload(ship_positions=data.positions)
        # Validate if ships are already positioned
        PositioningServices.validate_ships_positioned(
            gameplay=gameplay, player=data.player
        )

        if gameplay.current_turn.is_automatic:
            return PositioningServices.auto_position_ships(player_board=player_board)

        return PositioningServices.manual_position_ships(
            data=data, player_board=player_board
        )

    @staticmethod
    def get_player_board(gameplay: Gameplay, player: str) -> GameBoard:
        """Getting the player's board."""
        return (
            gameplay.player1.board
            if player == PlayerRoles.PLAYER1.value
            else gameplay.player2.board
        )

    @staticmethod
    def validate_game_status(gameplay: Gameplay) -> None:
        """Validates if the game is active."""
        if not gameplay.is_active:
            raise GameNotActiveError("The game is not active")

    @staticmethod
    def manual_position_ships(
        data: PositionData, player_board: GameBoard
    ) -> Dict[str, str]:
        """Manually position ships on the board."""
        for position in data.positions:
            ship = Ships[position.ship]
            x, *y = position.coordinates
            PositioningServices.place_ship_on_board(
                board=player_board, ship=ship, x=x, y=y, direction=position.direction
            )
        return player_board.state

    @staticmethod
    def auto_position_ships(player_board: GameBoard) -> Dict[str, str]:
        max_attempts = settings.MAX_ATTEMPTS
        for ship in Ships:
            for _ in product(range(max_attempts), Directions):
                attempts, direction = _
                try:
                    x, y = PositioningServices.get_random_coordinates(
                        player_board=player_board
                    )
                    PositioningServices.place_ship_on_board(
                        board=player_board,
                        ship=ship,
                        x=x,
                        y=y,
                        direction=direction.name,
                    )
                    break
                except (InvalidBoardCoordinatesError, CoordinatesAlreadyHaveShipError):
                    if attempts >= max_attempts:
                        raise MaxPlacementAttemptsExceeded(
                            "Maximum number of placement attempts exceeded."
                        )
        return player_board.state

    @staticmethod
    def get_random_coordinates(player_board: GameBoard) -> Tuple[int, int]:
        return random.randint(0, player_board.width - 1), random.randint(
            0, player_board.height - 1
        )

    @staticmethod
    def place_ship_on_board(
        board: GameBoard, ship: Ships, x: int, y: int, direction: str
    ) -> None:
        """Positions a ship on the board."""
        coords = PositioningServices.generate_coordinates(
            ship_len=ship.value, direction_str=direction, x=x, y=y
        )
        PositioningServices.validate_coordinates(coords=coords, board=board)
        PositioningServices.update_board_state(
            board=board, coords=coords, ship_name=ship.name
        )

    @staticmethod
    def generate_coordinates(
        ship_len: int, direction_str: str, x: int, y: int
    ) -> List[Tuple[int, int]]:
        """Generates coordinates for a ship."""
        dx, dy = Directions[direction_str.upper()].value
        return [(x + i * dx, y + i * dy) for i in range(ship_len)]

    @staticmethod
    def validate_coordinates(coords: List[Tuple[int, int]], board: GameBoard) -> None:
        for x, y in coords:
            if x < 0 or x >= board.width or y < 0 or y >= board.height:
                raise InvalidBoardCoordinatesError(
                    "Invalid coordinates: Outside board boundaries"
                )
            if board.state.get(f"{x},{y}") is not None:
                raise CoordinatesAlreadyHaveShipError(
                    "Invalid coordinates: Position already has a ship"
                )

    @staticmethod
    def validate_ships_in_payload(ship_positions: List[PositionVector]) -> None:
        ship_names_from_payload = [position.ship for position in ship_positions]

        # Convert to set for unique names and compare with the enum
        if set(ship_names_from_payload) != set(Ships.names()):
            raise IncompleteShipsPositioningError(
                "All ships must be positioned without duplicates."
            )

    @staticmethod
    def update_board_state(
        board: GameBoard, coords: List[Tuple[int, int]], ship_name: str
    ) -> None:
        for x, y in coords:
            board.state[f"{x},{y}"] = ShipSymbols[ship_name.upper()].value
        board.save()

    @staticmethod
    def validate_ships_positioned(gameplay: Gameplay, player: str) -> None:
        player_board, opponent_board = PositioningServices.get_boards(
            gameplay=gameplay, player=player
        )

        if PositioningServices.board_has_ships(board=player_board):
            if PositioningServices.board_has_ships(board=opponent_board):
                raise BothPlayersPositionedError(
                    "Both players have positioned their ships."
                )
            else:
                raise TurnToPositionShipsError(
                    f"It's the turn of {gameplay.get_opponent(player)} to position their ships."
                )

    @staticmethod
    def get_boards(gameplay: Gameplay, player: str) -> Tuple[GameBoard, GameBoard]:
        if player == PlayerRoles.PLAYER1.value:
            return gameplay.player1.board, gameplay.player2.board
        else:
            return gameplay.player2.board, gameplay.player1.board

    @staticmethod
    def board_has_ships(board: GameBoard) -> bool:
        return bool(board.state)
