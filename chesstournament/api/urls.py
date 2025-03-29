from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
	RefereeViewSet,
	PlayerViewSet,
	RoundViewSet
)

# Define the router and register the viewsets
router = DefaultRouter()
router.register(r'referees', RefereeViewSet)
router.register(r'players', PlayerViewSet)
# router.register(r'games', GameViewSet)
# router.register(r'tournaments', TournamentViewSet)
router.register(r'rounds', RoundViewSet)
# router.register(r'users', CustomUserViewSet)

# Save the router urls
urlpatterns = [
	path('', include(router.urls)),
]
