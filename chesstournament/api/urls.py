from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
	RefereeViewSet,
	PlayerViewSet,
	GameViewSet,
	TournamentViewSet,
	RoundViewSet,
	CustomUserViewSet,

	CreateRoundAPIView,
	SearchTournamentsAPIView,
)

# Define the router and register the viewsets
router = DefaultRouter()
router.register(r'referees', RefereeViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)
router.register(r'tournaments', TournamentViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'users', CustomUserViewSet, basename='user')

# Save the router urls
urlpatterns = [
	# Router URLS
	path('', include(router.urls)),

	# Endpoints
	path('create_round', CreateRoundAPIView.as_view(), name='create-round'),
	path('searchTournaments', SearchTournamentsAPIView.as_view(), name='search-tournaments'),
]
