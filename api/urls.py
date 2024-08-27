from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.infrastructure import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "api"

router = DefaultRouter()
router.register(r"gameplays", views.GameplayViewSet, basename="gameplays")
router.register(r"users", views.CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
