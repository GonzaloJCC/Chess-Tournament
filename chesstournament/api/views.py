# from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from djoser.views import UserViewSet

from chess_models.models import (
	Referee,
	Player,
	Game,
	Tournament,
	Round
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
