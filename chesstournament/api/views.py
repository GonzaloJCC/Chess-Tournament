# from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
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

	create_rounds
)
from chess_models.serializers import (
	RefereeSerializer,
	PlayerSerializer,
	GameSerializer,
	TournamentSerializer,
	RoundSerializer
)

##########################
# NOTE: Pagination class #
##########################

class TournamnetPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
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
		if self.action == 'update':
			return [AllowAny()]
		return super().get_permissions()

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		if not instance.finished:
			response = super().update(request, *args, **kwargs)
			instance.finished = True
			instance.save()
			return response
		else:
			raise PermissionDenied("This game has already finished and cannot be updated.")

class TournamentViewSet(ModelViewSet):
	queryset = Tournament.objects.all()
	serializer_class = TournamentSerializer
	pagination_class = TournamnetPagination

	# Redefined the permissions of the list set
	def get_permissions(self):
		if self.action == 'list':
			return [AllowAny()]
		return super().get_permissions()

class RoundViewSet(ModelViewSet):
	queryset = Round.objects.all()
	serializer_class = RoundSerializer

class CustomUserViewSet(UserViewSet):
	def create(self, request, *args, **kwargs):
		return Response(
			{'error': 'Method not allowed'},
			status=status.HTTP_405_METHOD_NOT_ALLOWED
		)


###################
# NOTE: Endpoints #
###################
class CreateRoundAPIView(APIView):
	permission_classes = [IsAuthenticated]
	
	def post(self, request):

		# Get the tournament id
		tournament_id = request.data.get('tournament_id')
		if not tournament_id:
			return Response(
				{
					'result': False,
					'message': 'Tournament ID is required'
				}, status=status.HTTP_400_BAD_REQUEST
			)
		tournament_id = int(tournament_id)

		# Search the tournament
		tournament = Tournament.objects.get(id=tournament_id)
		if not tournament:
			return Response(
				{
					'result': False,
					'message': 'Tournament not found'
				}, status=status.HTTP_400_BAD_REQUEST
			)
		
		# Check the are enought players on the tournament
		if tournament.players.count() == 0:
			return Response(
				{
					'result': False,
					'message': 'Tournament has no players'
				}, status=status.HTTP_400_BAD_REQUEST
			)

		# Create the rounds
		rounds = create_rounds(tournament, [])
		if len(rounds) == 0:
			return Response(
				{
					'result': False,
					'message': 'No rounds created'
				}, status=status.HTTP_400_BAD_REQUEST
			)
		
		# TODO: Insert the rounds
		
		# Return a corerct response
		return Response(
			{'result': True},
			status=status.HTTP_201_CREATED
		)
	
class SearchTournamentsAPIView(APIView):
	permission_classes = []

	def post(self, request):
		search_string = request.data.get('search_string')
		if not search_string:
			return Response(
				{
					'result': False,
					'message': 'search_string is required'
				}, status=status.HTTP_400_BAD_REQUEST
			)
		
		# Get all the tournaments
		tournaments = Tournament.objects.filter(name__icontains=search_string)

		# Serialize the tournaments
		serializer = TournamentSerializer(tournaments, many=True)
		return Response(
			serializer.data,
			status=status.HTTP_200_OK
		)