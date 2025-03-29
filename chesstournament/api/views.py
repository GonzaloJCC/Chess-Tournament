from django.shortcuts import render
from rest_framework import viewsets
from chess_models.models import Referee
from chess_models.serializers import RefereeSerializer

class RefereeViewSet(viewsets.ModelViewSet):
	queryset = Referee.objects.all()
	serializer_class = RefereeSerializer