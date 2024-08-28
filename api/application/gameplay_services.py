from api.domain.entities import Gameplay, Player, GameBoard
from api.domain.exceptions import InvalidPlayerError


class GameplayServices:
    @staticmethod
    def create_gameplay(data: dict) -> Gameplay:
        """Creates a new gameplay."""
        try:
            player1 = Player.objects.get(user=data.get("player1"))
            player2 = Player.objects.get(user=data.get("player2"))
        except Player.DoesNotExist:
            raise InvalidPlayerError("Invalid player.")

        gameplay = Gameplay.objects.create(
            player1=player1, player2=player2, is_active=True, current_turn=player1
        )

        # Create a board
        GameBoard.objects.create(gameplay=gameplay)

        return gameplay

    @staticmethod
    def get_or_create_player(username: str, is_automatic: bool = False) -> Player:
        player, created = Player.objects.get_or_create(
            username=username, gameplay=null, is_automatic=is_automatic
        )
        return player

    @staticmethod
    def start_game(gameplay: Gameplay, player_1: Player) -> None:
        gameplay.current_turn = player_1  # The game starts with player1's turn
        gameplay.save()
