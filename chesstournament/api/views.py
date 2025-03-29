# from django.shortcuts import render
from rest_framework import viewsets, pagination
from rest_framework.permissions import AllowAny

from chess_models.models import (
	Referee,
	Player,
	Tournament,
	Round
)
from chess_models.serializers import (
	RefereeSerializer,
	PlayerSerializer,
	TournamentSerializer,
	RoundSerializer
)

##########################
# NOTE: Pagination class #
##########################

class TournamnetPagination(pagination.PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100


########################
# NOTE: Models Classes #
########################
class RefereeViewSet(viewsets.ModelViewSet):
	queryset = Referee.objects.all()
	serializer_class = RefereeSerializer

class PlayerViewSet(viewsets.ModelViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer

class TournamentViewSet(viewsets.ModelViewSet):
	queryset = Tournament.objects.all()
	serializer_class = TournamentSerializer
	pagination_class = TournamnetPagination

	# Redefined the permissions of the list set
	def get_permissions(self):
		if self.action == 'list':
			return [AllowAny()]
		return super().get_permissions()


class RoundViewSet(viewsets.ModelViewSet):
	queryset = Round.objects.all()
	serializer_class = RoundSerializer