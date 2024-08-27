import random
from typing import Optional, Tuple

from api.domain.choices import AttackSymbols, ShipSymbols
from api.domain.entities import GameBoard, Gameplay, Player
from api.domain.exceptions import (
    GameNotActiveError,
    IncompleteBoardError,
    InvalidAttackPositionError,
    InvalidAutomaticAttackError,
    InvalidPlayerError,
    InvalidTurnError,
)
from api.domain.input_data import AttackInput


class AttackServices:
    @staticmethod
    def handle_attack(
        gameplay: Gameplay, data: AttackInput
    ) -> Tuple[str, Optional[Player]]:
        """Handles an attack attempt."""
        AttackServices.is_game_active(gameplay=gameplay)
        AttackServices.is_valid_player(gameplay=gameplay, player=player)
        AttackServices.is_player_turn(gameplay=gameplay, player=player)
        AttackServices.is_second_player_board_complete(gameplay=gameplay)
        AttackServices.is_board_with_ships(gameplay.current_turn.board)

        if gameplay.current_turn.is_automatic:
            x, y = AttackServices.generate_random_coordinates(
                board=gameplay.current_turn.board
            )

        # Existing validations and attack logic
        AttackServices.validate_attack_position(gameplay=gameplay, x=x, y=y)
        hit_or_miss = AttackServices.perform_attack(
            board=gameplay.board, player=player, x=x, y=y
        )

        winner = AttackServices.check_winner(gameplay=gameplay)
        if winner:
            gameplay.is_active = False
            gameplay.save()
            return f"Player {winner.user.username} wins!", winner

        AttackServices.switch_turn(gameplay=gameplay)
        return "Hit" if hit_or_miss else "Miss", None

    @staticmethod
    def switch_turn(gameplay: Gameplay) -> None:
        gameplay.current_turn = (
            gameplay.player1
            if gameplay.current_turn == gameplay.player2
            else gameplay.player2
        )
        gameplay.save()

    @staticmethod
    def validate_attack_position(gameplay: Gameplay, x: int, y: int) -> None:
        board = gameplay.board
        if x < 0 or x >= board.width or y < 0 or y >= board.height:
            raise InvalidAttackPositionError(
                "Invalid coordinates: Outside board boundaries"
            )

        coordinate_key = f"{x},{y}"
        if board.board_state.get(coordinate_key) in [
            AttackSymbols.HIT.value,
            AttackSymbols.MISS.value,
        ]:
            raise InvalidAttackPositionError(
                "Invalid coordinates: Position already attacked"
            )

    @staticmethod
    def perform_attack(board: GameBoard, player: Player, x: int, y: int) -> bool:
        coordinate_key = f"{x},{y}"
        hit_or_miss = board.board_state.get(coordinate_key) in [
            e.value for e in ShipSymbols
        ]

        if hit_or_miss:
            board.board_state[coordinate_key] = AttackSymbols.HIT.value
            player.hit_count += 1
            player.save()
        else:
            board.board_state[coordinate_key] = AttackSymbols.MISS.value

        board.save()
        return hit_or_miss

    @staticmethod
    def is_game_active(gameplay: Gameplay) -> None:
        """Checks if the game is active."""
        if not gameplay.is_active:
            raise GameNotActiveError("The game is not active")

    @staticmethod
    def is_valid_player(gameplay: Gameplay, player: str) -> None:
        """Checks if the player exists in this game."""
        if player not in [gameplay.player1, gameplay.player2]:
            raise InvalidPlayerError("Player does not exist in this game")

    @staticmethod
    def is_player_turn(gameplay: Gameplay, player: str) -> None:
        """Checks if it's the player's turn."""
        if gameplay.current_turn != player:
            raise InvalidTurnError("It's not your turn")

    @staticmethod
    def is_second_player_board_complete(gameplay: Gameplay) -> None:
        """Checks if the second player's board is complete."""
        if not BoardServices.is_board_complete(gameplay.player2.board):
            raise IncompleteBoardError("The second player's board is not complete")

    @staticmethod
    def validate_automatic_attack(gameplay: Gameplay) -> None:
        """Validates if the current turn is an automatic player."""
        if not gameplay.current_turn.is_automatic:
            raise InvalidAutomaticAttackError("Current turn is not an automatic player")

    @staticmethod
    def generate_random_coordinates(board: GameBoard) -> Tuple[int, int]:
        """Generates random coordinates for an automatic attack."""
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        return x, y

    @staticmethod
    def check_winner(gameplay: Gameplay) -> Optional[Player]:
        """Checks if there is a winner."""
        for player in gameplay.player_set.all():
            total_ship_positions = sum(
                len(positions) for positions in gameplay.board.ship_positions.values()
            )
            if player.hit_count >= total_ship_positions:
                gameplay.is_active = False
                gameplay.winner = player
                gameplay.save()
                return player
        return None
