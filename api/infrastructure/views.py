# views.py in battlefield_app

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import GameBoard, Gameplay, Player
from .serializers import GameBoardSerializer, GameplaySerializer, PlayerSerializer
from users.models import CustomUser

class GameplayViewSet(viewsets.ModelViewSet):
    queryset = Gameplay.objects.all()
    serializer_class = GameplaySerializer

    def create(self, request, *args, **kwargs):
        try:
            # Using the inherited create method
            return super(GameplayViewSet, self).create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['POST'])
    def join_game(self, request, pk=None):
        user = request.user
        gameplay = self.get_object()

        # Check if the game already has two players
        if gameplay.players.count() >= 2:
            raise ValidationError("The game already has two players.")

        # Check if the joining user is already a player
        if gameplay.players.filter(id=user.id).exists():
            raise ValidationError("You are already a player in this game.")

        Player.objects.create(user=user, gameplay=gameplay, is_automatic=False)

        serializer = GameplaySerializer(gameplay)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def attack(self, request, pk=None):
        x = request.query_params.get('x', None)
        y = request.query_params.get('y', None)
        gameplay = self.get_object()
        board = gameplay.board
        # Add your attack logic here
        message = "Hit or Miss based on your logic"
        return Response({"message": message}, status=status.HTTP_200_OK)
