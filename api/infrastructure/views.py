from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.application.services import CoinService
from api.domain.exceptions import CoinMaxProfitException, CoinNameSymbolException
from api.domain.serializers import CoinSerializer

from .models import Coin


class CoinViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer

    @action(detail=False, methods=["get"])
    def close_values(self, request):
        data = CoinService.CoinClose(
            symbol=request.GET.get("symbol"), date=request.GET.get("date")
        )

        if not data.symbol or not data.date:
            return Response(
                {"error": "Both symbol and date are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not CoinService.check_symbol(symbol=data.symbol):
            return Response(
                {"error": "Invalid Symbol"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        close_values = CoinService.get_coin_close_values(data=data)

        return Response(close_values, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def max_profit(self, request):
        data = CoinService.CoinMaxProfit(
            symbol=request.GET.get("symbol"),
            start_date=request.GET.get("start_date"),
            end_date=request.GET.get("end_date"),
        )

        if not data.symbol or not data.start_date or not data.end_date:
            return Response(
                {"error": "Symbol, start_date, and end_date are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not CoinService.check_symbol(symbol=data.symbol):
            return Response(
                {"error": "Invalid Symbol"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            max_profit_value = CoinService.get_coin_max_profit(data=data)
            return Response(max_profit_value, status=status.HTTP_200_OK)
        except (CoinMaxProfitException, DateFormatException, BuySellException, CoinSymbolException):
            return Response(
                {"error": "An error occurred while getting max profit"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def list_names_symbols(self, request):
        try:
            names_symbols = CoinService.get_coin_names_symbols()
            return Response(names_symbols, status=status.HTTP_200_OK)
        except CoinNameSymbolException as e:
            return Response(
                {"error": "An error occurred while listing coin names and symbols"},
                status=status.HTTP_400_BAD_REQUEST,
            )
