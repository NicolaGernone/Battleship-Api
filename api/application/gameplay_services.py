import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from api.domain.entities import CustomUser, Gameplay, Player
from api.domain.exceptions import (
    GameNotActiveError,
    InvalidPlayerError,
    PlayerAlreadyJoinedError,
)

from api.application.user_services import UserServices


class GameplayServices:
    @staticmethod
    def create_gameplay(player_1: CustomUser, data: dict) -> Gameplay:
        """Creates a new gameplay."""
        gameplay = Gameplay.objects.create()

        # Create player 1
        GameplayServices.create_player(user=player_1, gameplay=gameplay)

        # Create Player 2
        GameplayServices.create_or_get_player_2(
            gameplay=gameplay, username=data.get("username")
        )

        # Start the game
        GameplayServices.start_game(gameplay=gameplay, player_1=player_1)

        # Create a board
        GameBoard.objects.create(gameplay=gameplay)

        return gameplay

    @staticmethod
    def validate_existent_player(user: CustomUser) -> None:
        if Gameplay.objects.filter(player__user=user).exists():
            raise InvalidPlayerError("You are already a player in this game.")

    @staticmethod
    def validate_player_count(gameplay: Gameplay) -> None:
        if gameplay.player_set.count() >= 2:
            raise PlayerAlreadyJoinedError("The game already has two players.")

    @staticmethod
    def create_player(
        user: CustomUser, gameplay: Gameplay, is_automatic: bool = False
    ) -> None:
        GameplayServices.validate_existent_player(user=user)
        Player.objects.create(user=user, gameplay=gameplay, is_automatic=is_automatic)

    @staticmethod
    def create_automatic_player(gameplay: Gameplay) -> None:
        fake_user = UserServices.create_fake_user()
        Player.objects.create(user=fake_user, gameplay=gameplay, is_automatic=True)

    @staticmethod
    def create_or_get_player_2(gameplay: Gameplay, username: str = None) -> None:
        GameplayServices.validate_player_count(gameplay=gameplay)
        if username:
            try:
                # Try to find an existing CustomUser with the given username
                user = CustomUser.objects.get(username=username)
                GameplayServices.create_player(user=user, gameplay=gameplay)
            except CustomUser.DoesNotExist:
                # If the user does not exist, create an automatic user and set the message
                GameplayServices.create_automatic_player(gameplay=gameplay)
        else:
            # Create an automatic (fake) user
            GameplayServices.create_automatic_player(gameplay=gameplay)

    @staticmethod
    def start_game(gameplay: Gameplay, player_1: CustomUser) -> None:
        gameplay.current_turn = player_1  # The game starts with player1's turn
        gameplay.save()
