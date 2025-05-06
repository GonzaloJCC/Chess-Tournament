# from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework.views import APIView

from chess_models.models import (
    Referee,
    Player,
    Game,
    Tournament,
    Round,
    create_rounds,
    getRanking,
    LichessAPIError,
    Scores,
)
from chess_models.serializers import (
    RefereeSerializer,
    PlayerSerializer,
    GameSerializer,
    TournamentSerializer,
    RoundSerializer,
)

##########################
# NOTE: Pagination class #
##########################


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


########################
# NOTE: Models Classes #
########################
class RefereeViewSet(ModelViewSet):
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return []
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user
        tournament = instance.round.tournament

        if instance.finished and user != tournament.administrativeUser:
            raise PermissionDenied(
                "This game has already finished and cannot be updated."
            )

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            instance.finished = True
            instance.save(update_fields=["finished"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all().order_by("-start_date", "-id")
    serializer_class = TournamentSerializer
    pagination_class = CustomPagination

    # Redefined the permissions of the list set
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return []
        return super().get_permissions()


class RoundViewSet(ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer


class CustomUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


###################
# NOTE: Endpoints #
###################
class CreateRoundAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Get the tournament id
        tournament_id = request.data.get("tournament_id")
        if not tournament_id:
            return Response(
                {"result": False, "message": "Tournament ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tournament_id = int(tournament_id)

        # Search the tournament
        tournament = Tournament.objects.filter(id=tournament_id).first()
        if not tournament:
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check the are enought players on the tournament
        if tournament.players.count() == 0:
            return Response(
                {"result": False, "message": "Tournament has no players"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the rounds
        rounds = create_rounds(tournament, [])
        if len(rounds) == 0:
            return Response(
                {"result": False, "message": "No rounds created"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return a corerct response
        return Response({"result": True}, status=status.HTTP_201_CREATED)


class SearchTournamentsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        search_string = request.data.get("search_string")
        if not search_string:
            return Response(
                {"result": False, "message": "search_string is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get all the tournaments
        tournaments = Tournament.objects.filter(
            name__icontains=search_string
        ).order_by("-name")

        # Serialize the tournaments
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TournamentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Save the request params and check if there are any error
        serializer = TournamentSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save the tournament
        try:
            tournament = serializer.save()
            create_rounds(tournament)
            tournament.administrativeUser = request.user
            tournament.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {
                    "result": False,
                    "message": f"Error creating tournament:" f" {str(e)}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetRanking(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, tournament_id):
        tournament = Tournament.objects.filter(id=tournament_id).first()
        if not tournament:
            return Response(
                {"result": False, "message": "Error: tournament not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ranking = getRanking(tournament)
        if not ranking:
            return Response(
                {
                    "result": False,
                    "message": "Error while "
                    "getting the ranking"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = {}
        count = 0
        for player, data in ranking.items():
            count += 1
            current = str(count)

            result[current] = {}
            result[current]["id"] = player.id
            if player.lichess_username:
                result[current]["username"] = player.lichess_username
            else:
                result[current]["username"] = player.name
            result[current]["score"] = data["PS"]
            result[current]["rank"] = data["rank"]

            if "WI" in data:
                result[current]["WI"] = data["WI"]

            if "BT" in data:
                result[current]["BT"] = data["BT"]

        return Response(result, status=status.HTTP_200_OK)


class GetPlayers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_id):
        tournament = Tournament.objects.filter(id=tournament_id).first()
        if not tournament:
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        players = tournament.players.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetRoundResults(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, tournament_id):
        tournament = Tournament.objects.filter(id=tournament_id).first()
        if not tournament:
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rounds = Round.objects.filter(tournament=tournament).all()
        round_results = []

        for round_obj in rounds:
            games = Game.objects.filter(round=round_obj).order_by('id').all()
            games_data = []

            for game in games:
                games_data.append({
                    "id": game.id,
                    "finished": game.finished,
                    "start_date": game.start_date,
                    "update_date": game.update_date,
                    "result": game.result,
                    "rankingOrder": game.rankingOrder,
                    "white_player_name": game.white.name if game.white else "Unknown",
                    "white_player_email": game.white.email if game.white else "Unknown",
                    "black_player_name": game.black.name if game.black else "Unknown",
                    "black_player_email": game.black.email if game.black else "Unknown",
                    "white_lichess_username": game.white.lichess_username if game.white else "Unknown",
                    "black_lichess_username": game.black.lichess_username if game.black else "Unknown",
                    "round": game.round.id,
                })

            round_results.append({
                "id": round_obj.id,
                "name": round_obj.name,
                "start_date": round_obj.start_date,
                "end_date": round_obj.end_date,
                "finish": round_obj.finish,
                "games": games_data
            })

        return Response(round_results, status=status.HTTP_200_OK)


class UpdateLichessGameAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        # Get the game
        game_id = request.data.get("game_id")
        if not game_id:
            return Response(
                {"result": False, "message": "game_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        game = Game.objects.filter(id=game_id).first()
        if not game:
            return Response(
                {"result": False, "message": "Game does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if game.finished is True:
            return Response(
                {
                    "result": False,
                    "message": "Game is blocked,"
                               " only administrator can update it",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the lichess game id
        lichess_game_id = request.data.get("lichess_game_id")
        if not lichess_game_id:
            return Response(
                {"result": False, "message": "lichess_game_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            game_result, _, _ = game.get_lichess_game_result(lichess_game_id)
        except LichessAPIError as e:
            return Response(
                {"result": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        game.result = game_result
        game.finished = True
        game.save()
        return Response(
            {
                "result": True,
            },
            status=status.HTTP_200_OK,
        )


class UpdateOTBGameAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        # Get the params
        game_id = request.data.get("game_id")
        otb_result = request.data.get("otb_result")
        email = request.data.get("email")
        if None in [game_id, otb_result, email]:
            return Response(
                {
                    "result": False,
                    "message": "game_id, otb_result and email are required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse the result
        try:
            otb_result = Scores(otb_result)
        except ValueError:
            return Response(
                {"result": False, "message": "Invalid otb_result"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Search the game
        game = Game.objects.filter(id=game_id).first()
        if not game:
            return Response(
                {"result": False, "message": "Game does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if game.finished:
            return Response(
                {
                    "result": False,
                    "message": "Game is blocked, only"
                               " administrator can update it",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the email is valid
        player = Player.objects.filter(email=email).first()
        if not player:
            return Response(
                {"result": False, "message": "Player does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the game
        game.result = otb_result
        game.finished = True
        game.save()
        return Response(
            {"result": True, "message": "Game updated by player"},
            status=status.HTTP_200_OK,
        )


class AdminUpdateGameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        game_id = request.data.get("game_id")
        otb_result = request.data.get("otb_result")

        if None in [game_id, otb_result]:
            return Response(
                {
                    "result": False, "message":
                    "game_id and otb_result" " are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse the result and search the game
        try:
            otb_result = Scores(otb_result)
        except ValueError:
            return Response(
                {"result": False, "message": "Invalid otb_result"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        game = Game.objects.filter(id=game_id).first()
        if not game:
            return Response(
                {"result": False, "message": "Game does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user is an administrative user
        tournament = game.round.tournament        
        if tournament.only_administrative and not request.user == tournament.administrativeUser:
            return Response(
                {
                    "result": False,
                    "message": "Only the user that created"
                               " the tournament can update it",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Update the game
        game.result = otb_result
        game.finished = True
        game.save()
        return Response(
            {"result": True, "message": "Game updated by administrator"},
            status=status.HTTP_200_OK,
        )
