# models.py in battlefield_app

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Gameplay(models.Model):
    is_active = models.BooleanField(default=True)
    player1 = models.ForeignKey(
        "Player", related_name="player1", on_delete=models.CASCADE
    )
    player2 = models.ForeignKey(
        "Player", related_name="player2", on_delete=models.CASCADE
    )
    winner = models.ForeignKey(
        "Player",
        related_name="won_games",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    current_turn = models.ForeignKey(
        "Player",
        related_name="current_turns",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


class GameBoard(models.Model):
    width = models.IntegerField(default=settings.BOARD_WIDTH)
    height = models.IntegerField(default=settings.BOARD_HEIGHT)
    state = models.JSONField(default=dict)


class Player(models.Model):
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    gameplay = models.ForeignKey(
        "Gameplay",
        related_name="gameplay",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    board = models.OneToOneField(
        "GameBoard",
        related_name="board",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_automatic = models.BooleanField(default=False)
    hit_count = models.PositiveIntegerField(default=0)
