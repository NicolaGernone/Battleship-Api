# models.py in battlefield_app

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Gameplay(models.Model):
    is_active = models.BooleanField(default=True)
    players = models.ManyToManyField(CustomUser, through='Player')
    winner = models.ForeignKey('Player', related_name='won_games', null=True, blank=True, on_delete=models.SET_NULL)

class GameBoard(models.Model):
    board_state = models.JSONField(default=dict)
    gameplay = models.OneToOneField(Gameplay, related_name='board', on_delete=models.CASCADE)

class Player(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gameplay = models.ForeignKey(Gameplay, on_delete=models.CASCADE)
    is_automatic = models.BooleanField(default=False)
