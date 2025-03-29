from django.shortcuts import render
from rest_framework import viewsets
from chess_models.models import (
	Referee,
	Player,
	Round
)
from chess_models.serializers import (
	RefereeSerializer,
	PlayerSerializer,
	RoundSerializer
)

class RefereeViewSet(viewsets.ModelViewSet):
	queryset = Referee.objects.all()
	serializer_class = RefereeSerializer

class PlayerViewSet(viewsets.ModelViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer

class RoundViewSet(viewsets.ModelViewSet):
	queryset = Round.objects.all()
	serializer_class = RoundSerializer