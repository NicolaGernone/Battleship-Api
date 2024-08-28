from rest_framework import serializers

from api.application.gameplay_services import GameplayServices
from django.contrib.auth.models import User
from api.application.user_services import UserServices
from api.domain.entities import GameBoard, Gameplay, Player

from app.settings import LOGGER as lg


class GameplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gameplay
        fields = fields = [
            "id",
            "is_active",
            "player1",
            "player2",
            "current_turn",
            "winner",
        ]

    def create(self, validated_data):
        lg.info(f"Creating gameplay with data: {validated_data}")
        gameplay = GameplayServices.create_gameplay({**validated_data})
        return gameplay


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        # user = CustomUser.objects.create_user(**validated_data)
        user = UserServices.create_user(**validated_data)
        return user


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "user", "gameplay", "board", "is_automatic", "hit_count"]

    def create(self, validated_data):
        player = Player.objects.create(**validated_data)
        return player
