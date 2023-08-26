from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.infrastructure.views import CoinViewSet

router = DefaultRouter()
router.register(r"coins", CoinViewSet)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
