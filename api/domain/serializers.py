# serializers.py in battlefield_app

from rest_framework import serializers
from .models import GameBoard, Gameplay, Player
from users.models import CustomUser

class GameBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBoard
        fields = ['board_state']
        
    def create(self, validated_data):
        user = self.context['request'].user
        gameplay = Gameplay.objects.create()

        # Create a real player
        services.create_real_player(user, gameplay)

        # Optionally create an automatic player based on user input
        create_automatic_player = self.context['request'].data.get('create_automatic_player', False)
        if create_automatic_player:
            services.create_automatic_player(gameplay)

        # Create a board
        GameBoard.objects.create(gameplay=gameplay)

        return gameplay

class PlayerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = ['user', 'is_automatic']

class GameplaySerializer(serializers.ModelSerializer):
    board = GameBoardSerializer()
    players = PlayerSerializer(many=True)

    class Meta:
        model = Gameplay
        fields = ['is_active', 'board', 'players', 'winner']
