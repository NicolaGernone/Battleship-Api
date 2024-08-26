from django.core.exceptions import ValidationError
from .models import Player

def create_real_player(user, gameplay):
    Player.objects.create(user=user, gameplay=gameplay, is_automatic=False)

def create_automatic_player(gameplay):
    Player.objects.create(user=None, gameplay=gameplay, is_automatic=True)

def join_game(user, gameplay):
    # Check if the game already has two players
    if gameplay.players.count() >= 2:
        raise ValidationError("The game already has two players.")

    # Check if the joining user is already a player
    if gameplay.players.filter(id=user.id).exists():
        raise ValidationError("You are already a player in this game.")

    Player.objects.create(user=user, gameplay=gameplay, is_automatic=False)


def check_winner(gameplay):
    for player in gameplay.player_set.all():
        total_ship_positions = sum(len(positions) for positions in gameplay.board.ship_positions.values())
        if player.hit_count >= total_ship_positions:
            gameplay.is_active = False
            gameplay.winner = player
            gameplay.save()
            return player
    return