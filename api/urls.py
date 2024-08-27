from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.infrastructure import views

app_name = "api"

router = DefaultRouter()
router.register(r"games", views.GameplayViewSet, basename="gameplay")
router.register(r"users", views.CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
