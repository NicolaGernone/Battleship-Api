from rest_framework import serializers

from api.application.gameplay_services import GameplayServices
from api.domain.entities import CustomUser, GameBoard, Gameplay, Player

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
        user = self.context["request"].user
        gameplay = GameplayServices.create_gameplay(user, {**validated_data})
        return gameplay


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
