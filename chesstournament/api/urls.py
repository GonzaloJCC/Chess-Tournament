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
    TournamentCreateAPIView,
    GetRanking,
    GetPlayers,
    GetRoundResults,
    UpdateLichessGameAPIView,
    UpdateOTBGameAPIView,
    AdminUpdateGameAPIView,
)

# Define the router and register the viewsets
router = DefaultRouter()
router.register(r"referees", RefereeViewSet)
router.register(r"players", PlayerViewSet)
router.register(r"games", GameViewSet)
router.register(r"tournaments", TournamentViewSet)
router.register(r"rounds", RoundViewSet)
router.register(r"users", CustomUserViewSet, basename="user")

# Save the router urls
urlpatterns = [
    # Router URLS
    path("", include(router.urls)),
    # Endpoints
    path("create_round/", CreateRoundAPIView.as_view(), name="create-round"),
    path(
        "searchTournaments/",
        SearchTournamentsAPIView.as_view(),
        name="search-tournaments",
    ),
    path(
        "tournament_create/",
        TournamentCreateAPIView.as_view(),
        name="tournament-create",
    ),
    path(
        "get_ranking/<int:tournament_id>/", GetRanking.as_view(),
        name="get-ranking"
    ),
    path(
        "get_players/<int:tournament_id>/", GetPlayers.as_view(),
        name="get-players"
    ),
    path(
        "get_round_results/<int:tournament_id>/", GetRoundResults.as_view(),
        name="get-round-results",
    ),
    path(
        "update_lichess_game/",
        UpdateLichessGameAPIView.as_view(),
        name="update-lichess-game",
    ),
    path(
        "update_otb_game/", UpdateOTBGameAPIView.as_view(),
        name="update-otb-game"
    ),
    path(
        "admin_update_game/", AdminUpdateGameAPIView.as_view(),
        name="admin-update-game"
    ),
]
