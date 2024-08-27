from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from api.application.attack_services import AttackServices
from api.application.gameplay_services import GameplayServices
from api.application.positioning_services import PositioningServices
from api.domain.exceptions import (
    BothPlayersPositionedError,
    CoordinatesAlreadyHaveShipError,
    GameNotActiveError,
    IncompleteShipsPositioningError,
    InvalidAttackPositionError,
    InvalidAutomaticAttackError,
    InvalidBoardCoordinatesError,
    InvalidPlayerError,
    InvalidShipPositionError,
    InvalidTurnError,
    PlayerAlreadyJoinedError,
    TurnToPositionShipsError,
)
from api.domain.input_data import AttackInput, PositionData, PositionVector
from api.domain.serializers import CustomUserSerializer, GameplaySerializer
from api.infrastructure.models import CustomUser, GameBoard, Gameplay, Player

from app.settings import LOGGER as lg


class CustomUserViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = []
    authentication_classes = []
    
    def create(self, request, *args, **kwargs) -> Response:
        try:
            lg.info(f"Creating user with data: {request.data}")
            return super(CustomUserViewSet, self).create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    @action(detail=False, methods=['POST'])
    def login(self, request):
        lg.info(f"Logging in user with data: {request.data}")
        username = request.data.get('username')
        password = request.data.get('password')
        lg.info(f"Username: {username}, Password: {password}")

        # Try to authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # User exists and is authenticated
            django_login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': CustomUserSerializer(user).data
            })

        # User does not exist, return a warning message
        return Response({'warning': 'User does not exist. Please create a new account.'}, status=status.HTTP_404_NOT_FOUND)


class GameplayViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    queryset = Gameplay.objects.all()
    serializer_class = GameplaySerializer

    def create(self, request, *args, **kwargs) -> Response:
        try:
            return super(GameplayViewSet, self).create(request, *args, **kwargs)
        except (
            PlayerAlreadyJoinedError,
            InvalidPlayerError,
            CustomUser.DoesNotExist,
        ) as e:
            status_code = status.HTTP_400_BAD_REQUEST
            if isinstance(e, CustomUser.DoesNotExist):
                status_code = status.HTTP_404_NOT_FOUND  # Not Found
            return Response({"error": str(e)}, status=status_code)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["POST"])
    def position_ships(self, request, pk=None) -> Response:
        try:
            gameplay = self.get_object()

            player = request.data.get("player")
            positions_raw = request.data.get("positions", [])

            # Instantiate PositionData and PositionVector
            positions = [PositionVector(**pos) for pos in positions_raw]
            position_data = PositionData(player=player, positions=positions)

            # Position ships and get board state
            board_state = PositioningServices.position_ships(
                gameplay=gameplay, data=position_data
            )

            return Response(
                {"message": "Ships positioned successfully", "board": board_state},
                status=status.HTTP_200_OK,
            )
        except (
            GameNotActiveError,
            InvalidTurnError,
            InvalidShipPositionError,
            InvalidBoardCoordinatesError,
            CoordinatesAlreadyHaveShipError,
            IncompleteShipsPositioningError,
        ) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except BothPlayersPositionedError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except TurnToPositionShipsError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["GET"])
    def attack(self, request, pk=None) -> Response:
        try:
            gameplay = self.get_object()
            attack_data = AttackInput(**request.data)

            player = attack_data.player
            x, y = attack_data.coordinates

            message, winner = AttackServices.handle_attack(gameplay, player, x, y)

            return Response(
                {"message": message},
                status=status.HTTP_200_OK if not winner else status.HTTP_201_CREATED,
            )
        except InvalidAttackPositionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidAutomaticAttackError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except InvalidPlayerError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
